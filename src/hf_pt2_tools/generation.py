import copy
import functools
import json
from pathlib import Path
import subprocess
import sys
import traceback

import torch
from transformers import DynamicCache, EncoderDecoderCache, GenerationConfig
from transformers.modeling_outputs import BaseModelOutputWithPooling
from transformers.exporters.exporter_dynamo import DynamoConfig, DynamoExporter
from pt2_export_core.archive import assert_portable, extract, graph_op_counts, make_portable, selected_pt2_profile
from pt2_export_core.opgraph import collect_ops

from .artifacts import file_hash, publish, verify_artifact, write_json
from .exporting import producer
from .fixtures import cases_document, write_cases
from .inventory import captures_document, inventory, load_graph, program_values
from .recipes import compare, make_inputs, tensor_metadata
from .registry import RANDOM_WEIGHTS, build_model, digest, read_manifest, weight_provenance


class LlamaStep(torch.nn.Module):
    def __init__(self, model, decode=False):
        super().__init__()
        self.model = model
        self.config = model.config
        self.decode = decode

    def forward(self, **inputs):
        if self.decode:
            data = [(inputs[f'past_{i}_key'], inputs[f'past_{i}_value'])
                    for i in range(self.config.get_text_config().num_hidden_layers)]
            cache = DynamicCache(ddp_cache_data=data, config=self.config)
        else:
            cache = DynamicCache(config=self.config)
        forward = {key: value for key, value in inputs.items() if not key.startswith('past_')}
        if 'image_features' in forward:
            forward['mm_encoder_outputs'] = {'image': BaseModelOutputWithPooling(pooler_output=forward.pop('image_features'))}
        output = self.model(**forward, past_key_values=cache, use_cache=True)
        state = tuple(tensor for layer in output.past_key_values.layers for tensor in (layer.keys, layer.values))
        return (output.logits, *state)


class EncoderStep(torch.nn.Module):
    def __init__(self, encoder, config):
        super().__init__()
        self.encoder = encoder
        self.config = config

    def forward(self, **inputs):
        return (self.encoder(**inputs).last_hidden_state,)


class ConnectorStep(torch.nn.Module):
    def __init__(self, connector, config):
        super().__init__()
        self.connector = connector
        self.config = config

    def forward(self, hidden_states):
        return (self.connector(hidden_states),)


class Seq2SeqStep(torch.nn.Module):
    def __init__(self, model, layers, decode=False):
        super().__init__()
        self.model = model
        self.config = model.config
        self.layers = layers
        self.decode = decode

    def forward(self, **inputs):
        if self.decode:
            caches = [DynamicCache(ddp_cache_data=[(inputs[f'past_{i}_{kind}_key'], inputs[f'past_{i}_{kind}_value'])
                                                  for i in range(self.layers)]) for kind in ('self', 'cross')]
        else:
            caches = [DynamicCache(), DynamicCache()]
        cache = EncoderDecoderCache(*caches)
        kwargs = {'decoder_input_ids': inputs['decoder_input_ids'],
                  'decoder_attention_mask': inputs['decoder_attention_mask'],
                  'encoder_outputs': (inputs['encoder_hidden_states'],),
                  'past_key_values': cache, 'use_cache': True}
        if 'encoder_attention_mask' in inputs:
            kwargs['attention_mask'] = inputs['encoder_attention_mask']
        output = self.model(**kwargs)
        state = tuple(tensor for i in range(self.layers)
                      for subcache in (output.past_key_values.self_attention_cache, output.past_key_values.cross_attention_cache)
                      for tensor in (subcache.layers[i].keys, subcache.layers[i].values))
        return (output.logits, *state)


def decode_inputs(token, state, fields, constants, seq2seq):
    ids = 'decoder_input_ids' if seq2seq else 'input_ids'
    mask = 'decoder_attention_mask' if seq2seq else 'attention_mask'
    result = {ids: token, mask: torch.ones(1, state[0].shape[2] + 1, dtype=torch.int64), **constants}
    for field, value in zip(fields[1:], state, strict=True):
        result[field.replace('present_', 'past_', 1)] = value
    return result


def save_component(root, output_root, entry, config, component, program, cases, fields, capacity=8, weights=None,
                   population='tiny', cap_mb=64, variant=None, prefixes=None):
    weights = weights or dict(RANDOM_WEIGHTS)
    shape = variant or ('dynamic' if component == 'decode' else 'static')
    identity = f"{entry['id']}/{entry['category']}/{population}/{component}/fp32/dynamo/{shape}"
    if weights['kind'] == 'checkpoint':
        identity += f"/ckpt-{weights['revision'][:12]}"
    work = Path(output_root) / '.build' / identity
    work.mkdir(parents=True, exist_ok=True)
    make_portable(program)
    archive = work / 'model.pt2'
    torch.export.save(program, archive)
    caps = work / 'caps.yaml'
    write_json(caps, {'selection': {'max_weight_mb': cap_mb, 'release_max_weight_mb': cap_mb}})
    profile = selected_pt2_profile(caps)
    assert_portable(archive, profile)
    case_entries = write_cases(work, fields, cases)
    payload = work / 'examples.pt'
    torch.save({'cases': cases, 'tolerances': (1e-5, 1e-4)}, payload)
    process = subprocess.run([sys.executable, str(Path(__file__).with_name('fresh_load.py')), str(archive), str(payload)],
                             capture_output=True, text=True, timeout=90)
    (work / 'fresh-load.log').write_text(process.stdout + process.stderr)
    if process.returncode:
        raise RuntimeError('fresh generation component load/run failed')
    staging_root = work / 'staging'
    import shutil
    if staging_root.exists():
        shutil.rmtree(staging_root)
    extract(archive, 'artifact', staging_root, profile)
    staging = staging_root / 'artifact'
    graph = staging / 'models/model.json'
    ops, _ = collect_ops(program, exact_symints=True)
    write_json(staging / 'models/op_facts.json', {'schema_version': 1, 'graph_sha256': file_hash(graph),
               'dialect': 'functional', 'counts': graph_op_counts(graph), 'ops': ops})
    mutations = [str(spec.target) for spec in program.graph_signature.output_specs
                 if 'MUTATION' in spec.kind.name]
    if mutations:
        raise ValueError('generation tensor adapter unexpectedly mutates inputs/state')
    state = {'input': [key for key in cases[0]['inputs'] if key.startswith('past_')],
             'output': fields[1:], 'semantics': 'named self/cross-attention K/V tensors; batch x heads x history x head dimension',
             'host': 'feed returned tensors into the next step; host owns sampling and stopping',
             'maximum_input_history': capacity if component == 'decode' else None}
    recipe = {'component': component, 'state': state, 'inputs': tensor_metadata(cases[0]['inputs'])}
    if weights['kind'] == 'checkpoint':
        recipe['weights'] = weights
    if entry.get('processor_fixture'):
        recipe['processor_fixture_sha256'] = file_hash(Path(root) / entry['processor_fixture'])
    contract = {'schema_version': 1, 'artifact_id': identity, 'model_id': entry['id'],
                'population': population, 'model_class': entry['model_class'], 'weights': weights,
                'config_sha256': digest(config.to_dict()),
                'recipe_sha256': digest(recipe),
                'producer': producer(root), 'exporter': {'name': 'DynamoExporter', 'strict': False,
                'attention': 'eager', 'cache': component in ('prefill', 'decode'), 'shape_policy': 'static' if variant else shape},
                'dialect': 'functional', 'graph_sha256': file_hash(graph),
                'inputs': tensor_metadata(cases[0]['inputs']),
                'outputs': tensor_metadata(dict(zip(fields, cases[0]['outputs'], strict=True))),
                'call': {'args': [], 'kwargs': list(cases[0]['inputs']), 'outputs': 'tensor_tuple'},
                'dynamic_constraints': {'history': [1, capacity], 'attention_length': 'history+1'} if shape == 'dynamic' else {},
                'mutations': [], 'load_dependencies': ['torch'], 'verified_cases': len(cases),
                'tolerances': {'atol': 1e-5, 'rtol': 1e-4},
                'files': {str(path.relative_to(staging)): file_hash(path) for path in sorted(staging.rglob('*.json'))
                          if path.name != 'op_facts.json'}}
    if variant:
        contract['variant'] = {'kind': 'static-history', 'history': capacity, 'attention_length': capacity + 1}
    if component in ('prefill', 'decode'):
        contract['state'] = state
    write_json(staging / 'cases.json', cases_document(identity, case_entries, (1e-5, 1e-4), weights))
    contract['files']['cases.json'] = file_hash(staging / 'cases.json')
    write_json(staging / 'captures.json', captures_document(
        identity, contract['graph_sha256'], inventory(*load_graph(staging)), program_values(program), prefixes))
    contract['files']['captures.json'] = file_hash(staging / 'captures.json')
    write_json(staging / 'contract.json', contract)
    verify_artifact(root, staging, identity)
    publish(staging, Path(output_root) / 'models' / identity)
    return {'artifact_id': identity, 'status': 'verified', 'graph_sha256': file_hash(graph) if graph.exists() else contract['graph_sha256'],
            'cases': len(cases), 'fresh_load': json.loads(process.stdout.strip().splitlines()[-1])}


def run(root, output_root, name='smollm2-135m', population='tiny', snapshot=None, allow_unpinned=False,
        static_histories=()):
    torch.set_num_threads(1)
    manifest = read_manifest(root)
    entry = next(e for e in manifest['models'] if e['id'] == name)
    weights = weight_provenance(entry, snapshot, allow_unpinned)
    cap_mb = 64 if population == 'tiny' else entry.get('reference_max_weight_mb', manifest['selection']['max_weight_mb'])
    save = functools.partial(save_component, weights=weights, population=population, cap_mb=cap_mb)
    model, config = build_model(root, entry, population, 'fp32', snapshot)
    seq2seq = name in ('t5-small', 'whisper-tiny')
    capacity = 16 if name == 'smolvlm-256m' else 8
    if seq2seq:
        layers = config.num_decoder_layers if name == 't5-small' else config.decoder_layers
        fields = ['logits'] + [f'present_{i}_{kind}_{kv}' for i in range(layers) for kind in ('self', 'cross') for kv in ('key', 'value')]
    else:
        layers = config.get_text_config().num_hidden_layers
        fields = ['logits'] + [f'present_{i}_{kind}' for i in range(layers) for kind in ('key', 'value')]
    source = make_inputs(entry, config, population, root=root) if name != 'smollm2-135m' else {
        'input_ids': torch.tensor([[7, 11, 17, 23]]), 'attention_mask': torch.ones(1, 4, dtype=torch.int64)}
    work = Path(output_root) / '.build/generation'
    work.mkdir(parents=True, exist_ok=True)
    result = {'schema_version': 1, 'model_id': entry['id'], 'status': 'failed', 'components': {}, 'producer': producer(root),
              'population': population, 'weights': weights}
    try:
        generate_inputs = {key: value for key, value in source.items() if not key.startswith('decoder_')}
        generated = DynamoExporter().export_for_generation(model, copy.deepcopy(generate_inputs), DynamoConfig(strict=False),
            generation_config=GenerationConfig(max_new_tokens=2, pad_token_id=0, eos_token_id=2,
                                               decoder_start_token_id=getattr(config, 'decoder_start_token_id', None),
                                               use_cache=True, cache_implementation='dynamic'))
        result['upstream_export_for_generation'] = {'status': 'exported', 'components': sorted(generated),
                                                   'scope': 'capability evaluation; tensor-state adapters verified separately'}
    except Exception as error:
        result['upstream_export_for_generation'] = {'status': 'failed', 'error_category': type(error).__name__}
        (work / 'upstream.log').write_text(traceback.format_exc())
    stage = 'prefill'
    try:
        with torch.no_grad():
            constants = {}
            if seq2seq:
                stage = 'encoder'
                encoder = EncoderStep(model.get_encoder(), config).eval()
                encoder_inputs = {key: value for key, value in source.items() if not key.startswith('decoder_')}
                encoded = encoder(**copy.deepcopy(encoder_inputs))
                second_encoder_inputs = make_inputs(entry, config, population, seed=29, root=root)
                second_encoder_inputs = {key: value for key, value in second_encoder_inputs.items() if not key.startswith('decoder_')}
                second_encoded = encoder(**copy.deepcopy(second_encoder_inputs))
                encoder_program = DynamoExporter().export(encoder, copy.deepcopy(encoder_inputs), DynamoConfig(strict=False))
                encoder_program = encoder_program.run_decompositions(decomp_table={})
                compare(encoder_program.module()(**copy.deepcopy(encoder_inputs)), encoded)
                compare(encoder_program.module()(**copy.deepcopy(second_encoder_inputs)), second_encoded)
                result['components']['encoder'] = save(root, output_root, entry, config, 'encoder', encoder_program,
                    [{'inputs': encoder_inputs, 'outputs': encoded}, {'inputs': second_encoder_inputs, 'outputs': second_encoded}], ['encoder_hidden_states'],
                    prefixes={'encoder.': 'model.encoder.' if name == 'whisper-tiny' else 'encoder.'})
                constants = {'encoder_hidden_states': encoded[0]}
                if name == 't5-small':
                    constants['encoder_attention_mask'] = encoder_inputs['attention_mask']
                initial = {'decoder_input_ids': source['decoder_input_ids'],
                           'decoder_attention_mask': source.get('decoder_attention_mask', torch.ones(1, 4, dtype=torch.int64)), **constants}
                reset = {**copy.deepcopy(initial), 'encoder_hidden_states': second_encoded[0]}
                prefill = Seq2SeqStep(model, layers).eval()
                decode = Seq2SeqStep(model, layers, decode=True).eval()
                result['component_edges'] = {'encoder_hidden_states': 'encoder -> prefill/decode',
                                             'self/cross K/V': 'prefill -> decode -> decode'}
                stage = 'prefill'
            else:
                prefill = LlamaStep(model).eval()
                decode = LlamaStep(model, decode=True).eval()
                initial = source
                reset = make_inputs(entry, config, population, seed=29, root=root) if name == 'smolvlm-256m' else {
                    'input_ids': torch.tensor([[31, 19, 13, 5]]), 'attention_mask': source['attention_mask'].clone()}
                if name == 'smolvlm-256m':
                    stage = 'vision'
                    vision = EncoderStep(model.model.vision_model, config.vision_config).eval()
                    patch = config.vision_config.patch_size
                    vision_cases = []
                    for inputs in (initial, reset):
                        pixels = inputs['pixel_values'].flatten(0, 1)
                        mask = inputs['pixel_attention_mask'].flatten(0, 1)
                        patch_mask = mask.unfold(1, patch, patch).unfold(2, patch, patch).any(-1).any(-1)
                        arguments = {'pixel_values': pixels, 'patch_attention_mask': patch_mask}
                        vision_cases.append({'inputs': arguments, 'outputs': vision(**copy.deepcopy(arguments))})
                    program = DynamoExporter().export(vision, copy.deepcopy(vision_cases[0]['inputs']), DynamoConfig(strict=False))
                    program = program.run_decompositions(decomp_table={})
                    for case in vision_cases:
                        compare(program.module()(**copy.deepcopy(case['inputs'])), case['outputs'])
                    result['components']['vision'] = save(root, output_root, entry, config, 'vision', program,
                        vision_cases, ['vision_hidden_states'], prefixes={'encoder.': 'model.vision_model.'})
                    stage = 'connector'
                    connector = ConnectorStep(model.model.connector, config).eval()
                    connector_cases = [{'inputs': {'hidden_states': case['outputs'][0]},
                                        'outputs': connector(case['outputs'][0])} for case in vision_cases]
                    program = DynamoExporter().export(connector, copy.deepcopy(connector_cases[0]['inputs']), DynamoConfig(strict=False))
                    program = program.run_decompositions(decomp_table={})
                    for case in connector_cases:
                        compare(program.module()(**copy.deepcopy(case['inputs'])), case['outputs'])
                    result['components']['connector'] = save(root, output_root, entry, config, 'connector', program,
                        connector_cases, ['image_features'], prefixes={'connector.': 'model.connector.'})
                    for inputs, case in zip((initial, reset), connector_cases, strict=True):
                        original = prefill(**copy.deepcopy(inputs))
                        inputs.pop('pixel_values')
                        inputs.pop('pixel_attention_mask')
                        inputs['image_features'] = case['outputs'][0]
                        compare(prefill(**copy.deepcopy(inputs)), original)
                    result['component_edges'] = {'vision_hidden_states': 'vision -> connector',
                                                 'image_features': 'connector -> language prefill',
                                                 'K/V': 'language prefill -> decode -> decode'}
                    stage = 'prefill'
            first = prefill(**copy.deepcopy(initial))
            reset_output = prefill(**copy.deepcopy(reset))
            prefill_program = DynamoExporter().export(prefill, copy.deepcopy(initial), DynamoConfig(strict=False))
            prefill_program = prefill_program.run_decompositions(decomp_table={})
            compare(prefill_program.module()(**copy.deepcopy(initial)), first)
            compare(prefill_program.module()(**copy.deepcopy(reset)), reset_output)
            compare(prefill(**copy.deepcopy(initial)), first)
            result['components']['prefill'] = save(root, output_root, entry, config, 'prefill', prefill_program,
                [{'inputs': initial, 'outputs': first}, {'inputs': reset, 'outputs': reset_output}], fields)
            stage = 'decode'
            sample = decode_inputs(first[0][:, -1:].argmax(-1), first[1:], fields, constants, seq2seq)
            if population != 'tiny':
                capacity = first[1].shape[2] + (5 if name == 'smolvlm-256m' else 4)
            history = torch.export.Dim('history', min=1, max=capacity)
            mask_name = 'decoder_attention_mask' if seq2seq else 'attention_mask'
            shapes = {key: ({1: history + 1} if key == mask_name else
                           {2: history} if key.startswith('past_') and '_cross_' not in key else {}) for key in sample}
            decode_program = DynamoExporter().export(decode, copy.deepcopy(sample),
                DynamoConfig(strict=False, dynamic_shapes=shapes, prefer_deferred_runtime_asserts_over_guards=True))
            decode_program = decode_program.run_decompositions(decomp_table={})
            cases = []
            eager_state, graph_state = first, prefill_program.module()(**copy.deepcopy(initial))
            while eager_state[1].shape[2] <= capacity:
                eager_token = eager_state[0][:, -1:].argmax(-1)
                graph_token = graph_state[0][:, -1:].argmax(-1)
                assert torch.equal(eager_token, graph_token)
                inputs = decode_inputs(eager_token, eager_state[1:], fields, constants, seq2seq)
                eager_state = decode(**copy.deepcopy(inputs))
                graph_state = decode_program.module()(**copy.deepcopy(decode_inputs(graph_token, graph_state[1:], fields, constants, seq2seq)))
                compare(graph_state, eager_state)
                cases.append({'inputs': inputs, 'outputs': eager_state})
            result['successive_steps'] = len(cases)
            reset_constants = {key: reset[key] for key in constants}
            reset_inputs = decode_inputs(reset_output[0][:, -1:].argmax(-1), reset_output[1:], fields, reset_constants, seq2seq)
            reset_decoded = decode(**copy.deepcopy(reset_inputs))
            compare(decode_program.module()(**copy.deepcopy(reset_inputs)), reset_decoded)
            cases.append({'inputs': reset_inputs, 'outputs': reset_decoded})
            invalid = decode_inputs(eager_state[0][:, -1:].argmax(-1), eager_state[1:], fields, constants, seq2seq)
            try:
                decode_program.module()(**invalid)
            except (RuntimeError, AssertionError):
                result['capacity_rejection_verified'] = True
            else:
                raise ValueError('out-of-capacity generation state was accepted')
            result['components']['decode'] = save(root, output_root, entry, config, 'decode', decode_program, cases, fields, capacity)
            if static_histories:
                result['static_variants'] = {}
                history_key = next(key for key in cases[0]['inputs'] if key.startswith('past_') and '_cross_' not in key)
                by_history = {case['inputs'][history_key].shape[2]: case for case in cases}
                for history in static_histories:
                    if history not in by_history:
                        raise ValueError(f'no verified decode step with history {history}')
                    case = by_history[history]
                    static = DynamoExporter().export(decode, copy.deepcopy(case['inputs']), DynamoConfig(strict=False))
                    static = static.run_decompositions(decomp_table={})
                    compare(static.module()(**copy.deepcopy(case['inputs'])), case['outputs'])
                    others = [other for key, other in by_history.items() if key != history]
                    rejected = 0
                    for other in others:
                        try:
                            static.module()(**copy.deepcopy(other['inputs']))
                        except (RuntimeError, AssertionError):
                            rejected += 1
                    if not others or rejected != len(others):
                        raise ValueError('static variant accepted a different history')
                    component = save(root, output_root, entry, config, 'decode', static, [case], fields, history,
                                     variant=f'static-h{history}')
                    result['static_variants'][str(history)] = {**component, 'rejected_other_histories': rejected}
            result['cache_reset_verified'] = True
            result['status'] = 'verified'
    except Exception as error:
        result['failed_stage'] = stage
        result['error_category'] = type(error).__name__
        (work / (stage + '.log')).write_text(traceback.format_exc())
    suffix = '' if population == 'tiny' and snapshot is None else f"-{population}{'-checkpoint' if snapshot else ''}"
    write_json(Path(output_root) / 'results/generation' / (name + suffix + '.json'), result)
    return result
