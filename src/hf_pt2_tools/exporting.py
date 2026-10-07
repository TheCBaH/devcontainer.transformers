import copy
import importlib.metadata
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import traceback

import torch
import pt2_export_core
from transformers.exporters.exporter_dynamo import DynamoConfig, DynamoExporter
from pt2_export_core.archive import assert_portable, extract, graph_op_counts, make_portable, selected_pt2_profile
from pt2_export_core.opgraph import collect_ops, time_budget

from .artifacts import file_hash, publish, verify_artifact, write_json
from .fixtures import cases_document, write_cases
from .recipes import AutocastTensorOutputs, TensorOutputs, compare, make_inputs, tensor_metadata
from .registry import artifact_id, build_model, digest, read_manifest


STAGES = ('construction', 'eager', 'export', 'aten_facts', 'functionalization',
          'functional_facts', 'decomposition', 'core_facts', 'portability',
          'save', 'fresh_load_run', 'extract', 'contract')


def producer(root):
    packages = ('torch', 'torchvision', 'transformers', 'pt2-export-core', 'numpy', 'safetensors')
    sources = {path.name: file_hash(path) for path in sorted(Path(__file__).parent.glob('*.py'))}
    core_dir = Path(pt2_export_core.__file__).parent
    core_sources = {path.name: file_hash(path) for path in sorted(core_dir.glob('*.py'))}
    core_module = Path(root) / 'modules' / 'devcontainer.pytorch-image-models'
    core_revision = subprocess.run(['git', '-C', str(core_module), 'rev-parse', 'HEAD'],
                                   check=True, capture_output=True, text=True).stdout.strip()
    return {'versions': {name: importlib.metadata.version(name) for name in packages},
            'python': platform.python_version(), 'architecture': platform.machine(),
            'device': 'cpu', 'core_revision': core_revision,
            'core_source_sha256': digest(core_sources), 'core_override': core_dir.resolve() != (core_module / 'modules/pt2-export-core/src/pt2_export_core').resolve(),
            'lock_sha256': file_hash(Path(root) / 'uv.lock'), 'tools_sha256': digest(sources)}


def run(root, name, output_root, population='tiny', dtype='fp32', policy='dynamo', shape='static'):
    torch.set_num_threads(1)
    manifest = read_manifest(root)
    entry = next(e for e in manifest['models'] if e['id'] == name)
    identity = artifact_id(entry, population, dtype, policy, shape)
    work = Path(output_root) / '.build' / identity
    work.mkdir(parents=True, exist_ok=True)
    row = {'name': name, 'artifact_id': identity, 'category': entry['category'],
           'population': population, 'dtype': dtype, 'policy': policy, 'shape_policy': shape,
           'status': 'failed', 'stages': {s: {'status': 'not_run'} for s in STAGES},
           'ops': {}, 'schemas': {}, 'producer': producer(root), 'flops': {'status': 'not_measured'}}
    stage = 'construction'

    def success(s):
        row['stages'][s] = {'status': 'ok'}

    def failure(s, error):
        row['stages'][s] = {'status': 'failed', 'error_category': type(error).__name__}
        (work / (s + '.log')).write_text(traceback.format_exc())

    def facts(program, dialect, s):
        try:
            with time_budget(60):
                ops, schemas = collect_ops(program, exact_symints=True)
            row['ops'][dialect] = ops
            row['schemas'].update(schemas)
            success(s)
        except Exception as error:
            failure(s, error)

    try:
        with torch.no_grad():
            model, config = build_model(root, entry, population, dtype if policy != 'autocast' else 'fp32')
            if policy == 'autocast' and dtype == 'fp32':
                raise ValueError('CPU autocast requires fp16 or bf16')
            batch = 2 if shape == 'dynamic' else 1
            cases = [make_inputs(entry, config, population, seed=seed, batch=batch, root=root) for seed in (17, 29)]
            tensor_dtype = next(model.parameters()).dtype
            for case in cases:
                for key, value in case.items():
                    if value.is_floating_point():
                        case[key] = value.to(tensor_dtype)
            wrapper = TensorOutputs(model, entry['output_fields']).eval()
            if policy == 'autocast':
                wrapper = AutocastTensorOutputs(model, entry['output_fields'],
                    {'fp16': torch.float16, 'bf16': torch.bfloat16}[dtype]).eval()
            row['config_sha256'] = digest(config.to_dict())
            recipe = {'inputs': tensor_metadata(cases[0]), 'outputs': entry['output_fields'],
                      'seed': [17, 29], 'attention': 'eager', 'cache': False}
            fixture_key = 'processor_fixture' if population == 'tiny' else 'reference_processor_fixture'
            if entry.get(fixture_key):
                recipe['processor_fixture_sha256'] = file_hash(Path(root) / entry[fixture_key])
            row['recipe_sha256'] = digest(recipe)
            row['parameter_count'] = sum(p.numel() for p in model.parameters())
            row['weight_bytes'] = sum(p.numel() * p.element_size() for p in model.parameters())
            row['resume_key'] = digest({'config': row['config_sha256'], 'recipe': row['recipe_sha256'],
                                       'producer': row['producer'], 'id': identity})
            success(stage)
            stage = 'eager'
            expected = [wrapper(**copy.deepcopy(case)) for case in cases]
            compare(expected[0], expected[0], dtype)
            success(stage)
            stage = 'export'
            prepared = copy.deepcopy(cases[0])
            dynamic_shapes = None
            if shape == 'dynamic':
                if name not in ('bert-tiny', 'smollm2-135m'):
                    raise ValueError('dynamic recipe is currently reviewed for BERT/Llama only')
                batch_dim = torch.export.Dim('batch', min=2, max=4)
                sequence_dim = torch.export.Dim('sequence', min=4, max=64)
                dynamic_shapes = {key: {0: batch_dim, 1: sequence_dim} for key in prepared}
            with time_budget(120):
                if policy == 'direct':
                    raw = torch.export.export(wrapper, args=(), kwargs=prepared,
                                              strict=False, dynamic_shapes=dynamic_shapes)
                else:
                    raw = DynamoExporter().export(wrapper, prepared,
                        DynamoConfig(strict=False, dynamic=False, dynamic_shapes=dynamic_shapes))
            if shape == 'dynamic':
                row['dynamic_ranges'] = {'raw': {str(k): str(v) for k, v in raw.range_constraints.items()}}
            for case, output in zip(cases, expected, strict=True):
                compare(raw.module()(**copy.deepcopy(case)), output, dtype)
            success(stage)
            facts(raw, 'aten', 'aten_facts')
            stage = 'functionalization'
            with time_budget(120):
                functional = raw.run_decompositions(decomp_table={})
            if shape == 'dynamic':
                row['dynamic_ranges']['functional'] = {str(k): str(v) for k, v in functional.range_constraints.items()}
            for case, output in zip(cases, expected, strict=True):
                compare(functional.module()(**copy.deepcopy(case)), output, dtype)
            if shape == 'dynamic':
                second = make_inputs(entry, config, population, seed=31, batch=3, length=19, root=root)
                second_output = wrapper(**copy.deepcopy(second))
                compare(functional.module()(**copy.deepcopy(second)), second_output, dtype)
                cases.append(second)
                expected.append(second_output)
                invalid = make_inputs(entry, config, population, batch=3, length=65, root=root)
                try:
                    functional.module()(**invalid)
                except (RuntimeError, AssertionError):
                    row['dynamic_rejection_verified'] = True
                else:
                    raise ValueError('out-of-contract sequence was accepted')
            success(stage)
            facts(functional, 'func', 'functional_facts')
            try:
                with time_budget(120):
                    core = raw.run_decompositions()
                for case, output in zip(cases, expected, strict=True):
                    compare(core.module()(**copy.deepcopy(case)), output, dtype)
                success('decomposition')
                facts(core, 'core-cpu', 'core_facts')
            except Exception as error:
                failure('decomposition', error)
            stage = 'portability'
            make_portable(functional)
            success(stage)
            stage = 'save'
            archive = work / 'model.pt2'
            torch.export.save(functional, archive)
            cap_mb = 64 if population == 'tiny' else entry.get('reference_max_weight_mb', manifest['selection']['max_weight_mb'])
            if row['weight_bytes'] > cap_mb * 2**20:
                raise ValueError('artifact exceeds the declared weight cap')
            caps = work / 'caps.yaml'
            write_json(caps, {'selection': {'max_weight_mb': cap_mb, 'release_max_weight_mb': cap_mb},
                             'models': {name: {'weight_mb': row['weight_bytes'] / 2**20}}})
            profile = selected_pt2_profile(caps)
            assert_portable(archive, profile)
            success(stage)
            stage = 'fresh_load_run'
            tolerances = {'fp32': (1e-5, 1e-4), 'fp16': (5e-3, 5e-3), 'bf16': (5e-2, 5e-2)}[dtype]
            case_entries = write_cases(work, entry['output_fields'],
                                       [{'inputs': case, 'outputs': output} for case, output in zip(cases, expected, strict=True)])
            payload = work / 'examples.pt'
            torch.save({'cases': [{'inputs': case, 'outputs': output} for case, output in zip(cases, expected, strict=True)],
                        'tolerances': tolerances}, payload)
            loader = Path(__file__).with_name('fresh_load.py')
            process = subprocess.run([sys.executable, str(loader), str(archive), str(payload)],
                                     text=True, capture_output=True, timeout=90)
            (work / 'fresh-load.log').write_text(process.stdout + process.stderr)
            if process.returncode:
                raise RuntimeError('fresh load/run failed; see diagnostic')
            row['fresh_load'] = json.loads(process.stdout.strip().splitlines()[-1])
            success(stage)
            stage = 'extract'
            staging = work / 'staging'
            if staging.exists():
                shutil.rmtree(staging)
            extract(archive, 'artifact', staging, profile)
            staging = staging / 'artifact'
            success(stage)
            stage = 'contract'
            graph = staging / 'models/model.json'
            ops = row['ops']['func']
            counts = graph_op_counts(graph)
            graph_hash = file_hash(graph)
            write_json(staging / 'models/op_facts.json', {'schema_version': 1,
                       'graph_sha256': graph_hash, 'dialect': 'functional', 'counts': counts, 'ops': ops})
            contract = {'schema_version': 1, 'artifact_id': identity, 'model_id': name,
                        'population': population, 'model_class': entry['model_class'],
                        'config_sha256': row['config_sha256'], 'recipe_sha256': row['recipe_sha256'],
                        'producer': row['producer'], 'exporter': {'name': 'torch.export' if policy == 'direct' else 'DynamoExporter', 'strict': False,
                        'attention': 'eager', 'cache': False, 'shape_policy': shape},
                        'dialect': 'functional', 'graph_sha256': graph_hash,
                        'inputs': tensor_metadata(prepared),
                        'outputs': tensor_metadata(dict(zip(entry['output_fields'], expected[0], strict=True))),
                        'call': {'args': [], 'kwargs': list(prepared), 'outputs': 'tensor_tuple'},
                        'dynamic_constraints': ({'batch': [2, 4], 'sequence': [4, 64],
                                                'shared_inputs': list(prepared)} if shape == 'dynamic' else {}),
                        'mutations': [], 'load_dependencies': ['torch'],
                        'verified_cases': len(cases), 'tolerances': {'atol': tolerances[0], 'rtol': tolerances[1]},
                        'files': {str(path.relative_to(staging)): file_hash(path) for path in sorted(staging.rglob('*.json'))
                                  if path.name != 'op_facts.json'}}
            write_json(staging / 'cases.json', cases_document(identity, case_entries, tolerances))
            contract['files']['cases.json'] = file_hash(staging / 'cases.json')
            write_json(staging / 'contract.json', contract)
            verify_artifact(root, staging, identity)
            publish(staging, Path(output_root) / 'models' / identity)
            success(stage)
            row['status'] = 'ok'
            row['graph_sha256'] = graph_hash
    except Exception as error:
        failure(stage, error)
        row['error_category'] = type(error).__name__
        row['failed_stage'] = stage
    write_json(work / 'result.json', row)
    return row
