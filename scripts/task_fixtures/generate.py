import copy
import importlib.metadata
import json
from pathlib import Path
import platform
import shutil
import subprocess

import numpy as np
from PIL import Image
import torch
import transformers
from transformers.exporters.exporter_dynamo import DynamoConfig, DynamoExporter

from hf_pt2_tools.artifacts import verify_artifact
from hf_pt2_tools.checkpoints import fetch
from hf_pt2_tools.encoders import ImageEncoder, TextEncoder
from hf_pt2_tools.exporting import producer
from hf_pt2_tools.generation import LlamaStep, Seq2SeqStep
from hf_pt2_tools.recipes import TensorOutputs
from hf_pt2_tools.registry import CONFIG_CLASSES, read_manifest, weight_provenance

from .integrity import (check_contract, digest, download, extract, file_pin, pack,
                        read_json, tensor_records, verify_file, write_json)


def environment(root):
    commit = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
    if subprocess.check_output(['git', '-C', str(root), 'status', '--porcelain', '--untracked-files=no'], text=True):
        raise ValueError('fixture generation requires committed producer sources')
    return {**producer(root), 'commit': commit,
            'packages': {name: importlib.metadata.version(name) for name in
                         ('torch', 'torchvision', 'transformers', 'tokenizers', 'pillow', 'numpy', 'safetensors')},
            'generator_sources': {path.name: file_pin(path) for path in sorted(Path(__file__).parent.glob('*.py'))},
            'cpu': {'machine': platform.machine(), 'platform': platform.platform(),
                    'torch_config': torch.__config__.show(), 'parallel': torch.__config__.parallel_info(),
                    'threads': torch.get_num_threads(), 'interop_threads': torch.get_num_interop_threads(),
                    'mkldnn': torch.backends.mkldnn.enabled,
                    'capability': torch.backends.cpu.get_cpu_capability(),
                    'cpuinfo': Path('/proc/cpuinfo').read_text() if Path('/proc/cpuinfo').exists() else ''},
            'routes': ['eager attention, float32 CPU', 'DynamoExporter, strict=False, empty decomposition table'],
            'consumer_execution': 'not_measured'}


def load_references(root, request, task, work):
    publication_path = download(request['reference_publication'], work, 'publication.json')
    publication = read_json(publication_path)
    selected, references = [], []
    for identity in task['artifacts']:
        rows = [row for row in publication['artifacts'] if row['artifact_id'] == identity]
        if len(rows) != 1:
            raise ValueError('requested full artifact ID absent or duplicate in pinned release')
        row = rows[0]
        if row['producer_commit'] != request['reference_producer']:
            raise ValueError('wrong reference-release producer')
        folder = work / ('reference-' + digest(identity)[:16])
        folder.mkdir(parents=True, exist_ok=True)
        path = download(row['assets']['manifest'], work)
        manifest = read_json(path)
        archive = download(row['assets']['archive'], work)
        if manifest['artifact_id'] != identity or manifest['graph_sha256'] != row['graph_sha256'] or manifest['weight_source'] != row['weight_source']:
            raise ValueError('reference manifest/index identity mismatch')
        verify_file(archive, manifest['archive'])
        extract(archive, folder, manifest['members'])
        contract = verify_artifact(root, folder, identity)
        if contract['weights'] != row['weight_source']:
            raise ValueError('reference contract/checkpoint mismatch')
        if contract['producer']['lock_sha256'] != request['lock_sha256']:
            raise ValueError('reference release used a different frozen environment')
        for package, version in contract['producer']['versions'].items():
            if importlib.metadata.version(package) != version:
                raise ValueError('reference package version differs from generator')
        if contract['producer']['architecture'] != platform.machine():
            raise ValueError('reference architecture differs from generator')
        refs = {key: row[key] for key in ('artifact_id', 'model_id', 'component', 'graph_sha256', 'producer_commit', 'weight_source')}
        refs.update({'population': contract['population'], 'assets': row['assets'], 'tolerances': contract['tolerances'],
                     'contract': file_pin(folder / 'contract.json'), 'graph': file_pin(folder / 'models/model.json'),
                     'map': file_pin(folder / 'models/safetensors.v2.json'),
                     'config': {'sha256': row['weight_source']['config_sha256'],
                                'size': (root / 'configs/reference' / (row['model_id'] + '.json')).stat().st_size},
                     'release_environment': contract['producer']})
        references.append(refs)
        selected.append((folder, contract))
    return references, selected


def load_model(root, task, references, work):
    entry = next(entry for entry in read_manifest(root)['models'] if entry['id'] == task['model_id'])
    reference = entry['reference']
    if references[0]['weight_source']['revision'] != reference['revision']:
        raise ValueError('source registry/checkpoint revision mismatch')
    snapshot = Path(fetch(root, entry['id']))
    if weight_provenance(entry, snapshot) != references[0]['weight_source']:
        raise ValueError('loaded checkpoint bytes differ from reference release')
    config = getattr(transformers, CONFIG_CLASSES[entry['model_class']]).from_dict(read_json(snapshot / 'config.json'))
    config.return_dict = True
    config.output_attentions = False
    config.output_hidden_states = False
    config.use_cache = False
    if hasattr(config, 'text_config'):
        config.text_config.use_cache = False
    config._attn_implementation = 'eager'
    model, info = getattr(transformers, entry['model_class']).from_pretrained(
        snapshot, config=config, local_files_only=True, use_safetensors=True, dtype=torch.float32,
        attn_implementation='eager', output_loading_info=True)
    allowed_unused = ('cls.', 'bert.embeddings.position_ids') if entry['id'] == 'bert-tiny' else ()
    if info.get('missing_keys') or info.get('mismatched_keys') or info.get('error_msgs') or any(
            not key.startswith(allowed_unused) for key in info.get('unexpected_keys', [])):
        raise ValueError(f'incomplete or unexpected checkpoint loading: {info}')
    model.eval()
    assets = work / 'assets'
    assets.mkdir(parents=True, exist_ok=True)
    for name, pin in task['recipe']['assets'].items():
        download(pin, assets, name)
    verify_file(assets / 'config.json', references[0]['config'])
    return model, assets, info


def named(outputs, fields):
    if isinstance(outputs, torch.Tensor):
        outputs = (outputs,)
    if not isinstance(outputs, tuple) or len(outputs) != len(fields):
        raise ValueError('incomplete named outputs')
    return dict(zip(fields, outputs, strict=True))


def compare(actual, expected, tolerance):
    if list(actual) != list(expected):
        raise ValueError('output names or ordering mismatch')
    rows = []
    for name, reference in expected.items():
        value = actual[name]
        if value.dtype != reference.dtype or value.shape != reference.shape:
            raise ValueError('output dtype/shape mismatch')
        if not torch.isfinite(value).all() or not torch.isfinite(reference).all():
            raise ValueError('nonfinite output')
        difference = (value - reference).abs()
        bad = difference > tolerance['atol'] + tolerance['rtol'] * reference.abs()
        rows.append({'name': name, 'elements': reference.numel(), 'over_tolerance': bad.sum().item(),
                     'max_absolute_error': difference.max().item() if difference.numel() else 0,
                     'bitwise': torch.equal(value, reference)})
    return {'status': 'mismatch' if any(row['over_tolerance'] for row in rows) else 'pass', 'outputs': rows}


def exported(step, inputs, contract):
    shapes = None
    if contract['exporter']['shape_policy'] == 'dynamic':
        capacity = contract['state']['maximum_input_history']
        history = torch.export.Dim('history', min=1, max=capacity)
        mask = 'decoder_attention_mask' if 'decoder_input_ids' in inputs else 'attention_mask'
        shapes = {key: ({1: history + 1} if key == mask else
                        {2: history} if key.startswith('past_') and '_cross_' not in key else {}) for key in inputs}
    program = DynamoExporter().export(step, copy.deepcopy(inputs), DynamoConfig(
        strict=False, dynamic_shapes=shapes, prefer_deferred_runtime_asserts_over_guards=True))
    return program.run_decompositions(decomp_table={}).module()


class Writer:
    def __init__(self, directory):
        self.directory, self.cases = directory, []

    def raw_text(self, case_id, value):
        path = self.directory / 'raw' / (case_id + '.txt')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(value.encode('utf-8'))
        return {'path': str(path.relative_to(self.directory)), 'encoding': 'utf-8', **file_pin(path)}

    def case(self, case_id, groups, raw, **metadata):
        files = {}
        for group, tensors in groups.items():
            path = self.directory / 'cases' / case_id / (group + '.pt')
            path.parent.mkdir(parents=True, exist_ok=True)
            tensors = {name: tensor.detach().cpu().contiguous().clone() for name, tensor in tensors.items()}
            torch.save(tensors, path)
            files[str(path.relative_to(self.directory))] = {'tensors': tensor_records(tensors)}
        self.cases.append({'id': case_id, 'raw': raw, 'files': files, **metadata})


def tokenizer(assets, recipe):
    from tokenizers import BertWordPieceTokenizer, Tokenizer
    token = (BertWordPieceTokenizer(str(assets / 'vocab.txt'), lowercase=True) if recipe['tokenizer'] == 'wordpiece'
             else Tokenizer.from_file(str(assets / 'tokenizer.json')))
    token.enable_truncation(max_length=recipe['length'])
    token.enable_padding(length=recipe['length'], pad_id=recipe['pad_id'], pad_token=recipe['pad_token'])
    return token


def tokens(token, text, recipe, bert=False):
    encoded = token.encode(text, add_special_tokens=recipe.get('add_special_tokens', True))
    values = {'input_ids': torch.tensor([encoded.ids]), 'attention_mask': torch.tensor([encoded.attention_mask])}
    if bert:
        values['token_type_ids'] = torch.tensor([encoded.type_ids])
    intermediates = {**values, 'offsets': torch.tensor([encoded.offsets]), 'special_tokens_mask': torch.tensor([encoded.special_tokens_mask])}
    return values, intermediates, {'tokens': encoded.tokens, 'original_text': text}


def text_cases(model, assets, task, selected, writer):
    recipe = task['recipe']
    token = tokenizer(assets, recipe)
    contract = selected[0][1]
    fields = [tensor['name'] for tensor in contract['outputs']]
    step = TensorOutputs(model, fields).eval()
    graph = None
    for index, text in enumerate(recipe['texts']):
        case_id = f'case-{index:02d}'
        inputs, preprocessing, encoding = tokens(token, text, recipe, bert=True)
        validate_inputs(inputs, contract)
        eager = named(step(**copy.deepcopy(inputs)), fields)
        graph = graph or exported(step, inputs, contract)
        output = named(graph(**copy.deepcopy(inputs)), fields)
        result = compare(output, eager, contract['tolerances'])
        if result['status'] != 'pass':
            raise ValueError(f'raw text eager/export mismatch: {result}')
        writer.case(case_id, {'inputs': inputs, 'preprocessing': preprocessing, 'outputs': eager, 'exported': output},
                    [writer.raw_text(case_id, text)], encoding=encoding, producer_comparison=result)


def validate_inputs(inputs, contract):
    if list(inputs) != [tensor['name'] for tensor in contract['inputs']]:
        raise ValueError('recipe input names differ from selected graph')
    for value, spec in zip(inputs.values(), contract['inputs'], strict=True):
        if str(value.dtype).removeprefix('torch.') != spec['dtype'] or len(value.shape) != len(spec['shape']) or any(
                type(size) is int and size != actual for size, actual in zip(spec['shape'], value.shape, strict=True)):
            raise ValueError('recipe input shape/dtype differs from selected graph')


def image_case(assets, recipe, case_id, writer):
    pin = recipe['image']
    source = download(pin, writer.directory / 'raw', 'source.png')
    image = Image.open(source).convert('RGB')
    variant = recipe['image_cases'][int(case_id.removeprefix('case-'))]
    if variant['crop']:
        image = image.crop(variant['crop'])
    if variant.get('size'):
        image = image.resize(tuple(variant['size']), Image.Resampling.BICUBIC)
    path = writer.directory / 'raw' / (case_id + '.ppm')
    image.save(path)
    preprocessing = {'raw_rgb_hwc': torch.from_numpy(np.array(image).copy())}
    if recipe['processor'] == 'mobilevit':
        from transformers.models.mobilevit.image_processing_pil_mobilevit import MobileViTImageProcessorPil
        cls = MobileViTImageProcessorPil if recipe['backend'] == 'pillow' else transformers.MobileViTImageProcessor
    else:
        from transformers.models.clip.image_processing_pil_clip import CLIPImageProcessorPil
        cls = CLIPImageProcessorPil if recipe['backend'] == 'pillow' else transformers.CLIPImageProcessor
    processor = cls.from_pretrained(assets, local_files_only=True)
    for name in ('resize', 'center_crop'):
        original = getattr(processor, name)
        def trace(*args, _method=original, _name=name, **kwargs):
            value = _method(*args, **kwargs)
            preprocessing[_name] = value.detach().clone() if isinstance(value, torch.Tensor) else torch.from_numpy(np.array(value).copy())
            return value
        setattr(processor, name, trace)
    pixels = processor(images=image, return_tensors='pt')['pixel_values']
    preprocessing['pixel_values'] = pixels
    raw = [{'path': str(p.relative_to(writer.directory)), **file_pin(p)} for p in (source, path)]
    return pixels, preprocessing, raw, processor.to_dict()


def image_cases(model, assets, task, selected, writer):
    recipe, contract = task['recipe'], selected[0][1]
    fields = [tensor['name'] for tensor in contract['outputs']]
    step = TensorOutputs(model, fields).eval()
    graph = None
    token = tokenizer(assets, recipe) if recipe['processor'] == 'clip' else None
    for index, variant in enumerate(recipe['image_cases']):
        case_id = f'case-{index:02d}'
        pixels, preprocessing, raw, processor = image_case(assets, recipe, case_id, writer)
        if token:
            inputs, encoded, _ = tokens(token, variant['text'], recipe)
            preprocessing.update(encoded)
            inputs['pixel_values'] = pixels
            raw.append(writer.raw_text(case_id, variant['text']))
        else:
            inputs = {'pixel_values': pixels}
        validate_inputs(inputs, contract)
        eager = named(step(**copy.deepcopy(inputs)), fields)
        graph = graph or exported(step, inputs, contract)
        output = named(graph(**copy.deepcopy(inputs)), fields)
        result = compare(output, eager, contract['tolerances'])
        if result['status'] != 'pass':
            raise ValueError(f'image eager/export mismatch: {result}')
        host = {}
        if token:
            image_features = ImageEncoder(model).eval()(pixel_values=pixels)[0]
            text_features = TextEncoder(model).eval()(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'])[0]
            normalized_image = image_features / image_features.norm(dim=-1, keepdim=True)
            normalized_text = text_features / text_features.norm(dim=-1, keepdim=True)
            scale = model.logit_scale.exp()
            scores = scale * normalized_image @ normalized_text.T
            torch.testing.assert_close(scores, eager['logits_per_image'], **contract['tolerances'])
            host = {'image_features': image_features, 'text_features': text_features, 'image_embeds': normalized_image,
                    'text_embeds': normalized_text, 'logit_scale': scale, 'logits_per_image': scores, 'logits_per_text': scores.T}
            for (_, tower_contract), tower, arguments in zip(selected[1:], (ImageEncoder(model).eval(), TextEncoder(model).eval()),
                    ({'pixel_values': pixels}, {key: inputs[key] for key in ('input_ids', 'attention_mask')}), strict=True):
                validate_inputs(arguments, tower_contract)
                tower_output = exported(tower, arguments, tower_contract)(**copy.deepcopy(arguments))[0]
                key = 'image_features' if 'pixel_values' in arguments else 'text_features'
                torch.testing.assert_close(tower_output, host[key], **tower_contract['tolerances'])
        else:
            logits = eager['logits']
            host = {'top5_ids': logits.topk(5).indices, 'top5_logits': logits.topk(5).values}
            write_json(writer.directory / 'labels.json', model.config.id2label)
        writer.case(case_id, {'inputs': inputs, 'preprocessing': preprocessing, 'outputs': eager, 'exported': output, 'host': host},
                    raw, processor=processor, producer_comparison=result, image_variant=variant)


def next_inputs(outputs, mask):
    values = {'input_ids': outputs['logits'][:, -1:].argmax(-1),
              'attention_mask': torch.cat((mask, torch.ones(1, 1, dtype=torch.int64)), dim=1)}
    values.update({name.replace('present_', 'past_', 1): value for name, value in outputs.items() if name.startswith('present_')})
    return values


def generation_cases(model, assets, task, selected, writer):
    recipe = task['recipe']
    token = tokenizer(assets, recipe)
    prefill_contract, decode_contract = selected[0][1], selected[1][1]
    if decode_contract.get('variant', {}).get('history') != recipe['length'] or recipe['max_new_tokens'] != 2:
        raise ValueError('this bounded recipe requires the matching static first-history decode and exactly two tokens')
    steps = (LlamaStep(model).eval(), LlamaStep(model, decode=True).eval())
    graphs = [None, None]
    for sequence, text in enumerate(recipe['texts']):
        inputs, preprocessing, encoding = tokens(token, text, recipe)
        if not inputs['attention_mask'].all():
            raise ValueError('bounded generation requires four real prompt tokens')
        raw = writer.raw_text(f'prompt-{sequence:02d}', text)
        generated = []
        previous = None
        for index, (step, contract) in enumerate(zip(steps, (prefill_contract, decode_contract), strict=True)):
            validate_inputs(inputs, contract)
            fields = [tensor['name'] for tensor in contract['outputs']]
            before = {name: value.clone() for name, value in inputs.items()}
            eager = named(step(**copy.deepcopy(inputs)), fields)
            graphs[index] = graphs[index] or exported(step, inputs, contract)
            output = named(graphs[index](**copy.deepcopy(inputs)), fields)
            result = compare(output, eager, contract['tolerances'])
            if result['status'] != 'pass':
                raise ValueError(f'generation eager/export mismatch: {result}')
            if any(not torch.equal(value, before[name]) for name, value in inputs.items()):
                raise ValueError('generation mutated caller state')
            generated_token = eager['logits'][:, -1:].argmax(-1)
            generated.append(generated_token)
            position = torch.arange(inputs['attention_mask'].shape[1] - inputs['input_ids'].shape[1],
                                    inputs['attention_mask'].shape[1], dtype=torch.int64).unsqueeze(0)
            current = f'sequence-{sequence:02d}-step-{index:02d}'
            stopped = index + 1 == recipe['max_new_tokens'] or generated_token.item() in recipe['eos_token_ids']
            writer.case(current, {'inputs': inputs, 'preprocessing': {**preprocessing, 'position_ids': position},
                                 'outputs': eager, 'exported': output, 'host': {'generated_token': generated_token,
                                 'generated_tokens': torch.cat(generated, dim=1)}}, [raw], encoding=encoding,
                        artifact_id=contract['artifact_id'], producer_comparison=result,
                        transition={'sequence': sequence, 'reset': index == 0, 'previous_case': previous,
                                    'history_in': position[0, 0].item(), 'history_out': eager[fields[1]].shape[2],
                                    'cache_edges': {name: name.replace('present_', 'past_', 1) for name in fields[1:]},
                                    'stop': 'eos' if generated_token.item() in recipe['eos_token_ids'] else 'max_new_tokens' if stopped else None})
            if stopped:
                break
            previous = current
            inputs = next_inputs(eager, inputs['attention_mask'])
        unsupported = next_inputs(eager, inputs['attention_mask'])
        try:
            graphs[1](**copy.deepcopy(unsupported))
        except (RuntimeError, AssertionError):
            pass
        else:
            raise ValueError('static decode accepted unsupported history')


def diagnostic_cases(model, task, selected, writer):
    for reference_index, (folder, contract) in enumerate(selected):
        if task['model_id'] == 'whisper-tiny':
            step = Seq2SeqStep(model, model.config.decoder_layers, decode=contract['artifact_id'].split('/')[3] == 'decode').eval()
        else:
            step = LlamaStep(model, decode=contract['artifact_id'].split('/')[3] == 'decode').eval()
        fields = [tensor['name'] for tensor in contract['outputs']]
        graph = None
        for case in read_json(folder / 'cases.json')['cases']:
            case_id = f'reference-{reference_index:02d}-{case["id"]}'
            source = folder / 'cases' / case['id']
            inputs = torch.load(source / 'inputs.pt', map_location='cpu', weights_only=True)
            published = torch.load(source / 'outputs.pt', map_location='cpu', weights_only=True)
            if list(published) != fields:
                raise ValueError('published diagnostic outputs incomplete')
            eager = named(step(**copy.deepcopy(inputs)), fields)
            graph = graph or exported(step, inputs, contract)
            output = named(graph(**copy.deepcopy(inputs)), fields)
            raw_path = writer.directory / 'raw' / (case_id + '.json')
            write_json(raw_path, {'artifact_id': contract['artifact_id'], 'case_id': case['id'],
                                 'published_members': {name: file_pin(source / name) for name in ('inputs.pt', 'outputs.pt')}})
            writer.case(case_id, {'inputs': inputs, 'published': published, 'eager': eager, 'exported': output},
                        [{'path': str(raw_path.relative_to(writer.directory)), **file_pin(raw_path)}],
                        artifact_id=contract['artifact_id'], comparisons={
                            'eager_vs_published': compare(eager, published, contract['tolerances']),
                            'reexport_vs_published': compare(output, published, contract['tolerances']),
                            'reexport_vs_eager': compare(output, eager, contract['tolerances'])},
                        route='Controlled re-export of the pinned adapter; released graph/map pins are recorded separately. '
                              'This does not measure an OCaml consumer or execute its numerical policy.')


def generate(root, request_path, recipe_id, output):
    root, output = Path(root), Path(output)
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)
    request = read_json(request_path)
    if file_pin(root / 'uv.lock')['sha256'] != request['lock_sha256'] or platform.machine() != request['architecture']:
        raise ValueError('request requires the exact frozen producer lock and architecture')
    tasks = [task for task in request['tasks'] if task['recipe_id'] == recipe_id]
    if len(tasks) != 1:
        raise ValueError('unknown or duplicate recipe selection')
    task = tasks[0]
    work = output / '.work' / recipe_id
    directory = work / 'payload'
    if work.exists():
        shutil.rmtree(work)
    directory.mkdir(parents=True)
    references, selected = load_references(root, request, task, work)
    model, assets, loading = load_model(root, task, references, work)
    writer = Writer(directory)
    generator = environment(root)
    recipe_hash = digest(task['recipe'])
    contract = {'schema_version': 1, 'tensor_format': 'torch-flat-tensor-map-v1', 'kind': task['kind'],
                'artifact_id': task['artifacts'][0], 'recipe_id': recipe_id, 'recipe': task['recipe'], 'recipe_sha256': recipe_hash,
                'request_sha256': digest(request), 'references': references, 'reference_publication': request['reference_publication'],
                'generator': generator, 'model_loading': loading, 'expected_cases': task['expected_cases'],
                'tolerances': selected[0][1]['tolerances'], 'consumer_status': 'not_measured'}
    contract['fixture_id'] = f"{contract['artifact_id']}/task/{recipe_id}/{recipe_hash}/generator/{generator['commit']}/request/{contract['request_sha256']}"
    with torch.no_grad():
        if task['kind'] == 'diagnostic':
            diagnostic_cases(model, task, selected, writer)
        elif task['model_id'] == 'bert-tiny':
            text_cases(model, assets, task, selected, writer)
        elif task['model_id'] in ('tinyclip', 'mobilevit-xxs'):
            image_cases(model, assets, task, selected, writer)
        elif task['model_id'] == 'smollm2-135m':
            generation_cases(model, assets, task, selected, writer)
        else:
            raise ValueError('no reviewed raw-input generator for this task')
    shutil.copytree(assets, directory / 'assets')
    write_json(directory / 'environment.json', generator)
    contract['cases'] = writer.cases
    contract['producer_status'] = 'diagnostic' if task['kind'] == 'diagnostic' else 'verified'
    check_contract(contract)
    import jsonschema
    jsonschema.validate(contract, read_json(root / 'schemas/task-contract.schema.json'))
    path = pack(directory, output, contract)
    if task['model_id'] == 'bert-tiny':
        examples = []
        for case in writer.cases:
            path_inputs = next(path for path in case['files'] if path.endswith('/inputs.pt'))
            values = torch.load(directory / path_inputs, weights_only=True)
            examples.append({'id': case['id'], 'text': case['encoding']['original_text'],
                             'tensors': {name: tensor.tolist() for name, tensor in values.items()}})
        write_json(output / (recipe_id + '.example.json'), {'schema_version': 1, 'recipe_sha256': recipe_hash,
                                                         'fixture_id': contract['fixture_id'], 'cases': examples})
    print(f'{recipe_id}: {len(writer.cases)} cases verified; {path.name}')
    shutil.rmtree(work)
    return path
