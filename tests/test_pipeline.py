import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil

import pytest
from pt2_export_core.harness import run_worker

from hf_pt2_tools.artifacts import publish, verify_artifact, write_json
from hf_pt2_tools.cli import check_outcomes, source_key
from hf_pt2_tools.registry import read_manifest


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def bert_artifacts(tmp_path_factory):
    roots = [tmp_path_factory.mktemp('first'), tmp_path_factory.mktemp('second')]
    rows = []
    for output in roots:
        rows.append(run_worker(ROOT / 'scripts/worker.py',
                    ['worker', '--root', ROOT, '--output', output, '--subset', 'bert-tiny'],
                    'bert-tiny', 300))
        assert rows[-1]['status'] == 'ok', rows[-1]
    return roots, rows


def test_offline_fresh_process_and_reproducible_bytes(bert_artifacts):
    roots, rows = bert_artifacts
    for row in rows:
        assert all(stage['status'] == 'ok' for stage in row['stages'].values())
        assert row['fresh_load'] == {'status': 'ok', 'cases': 2, 'transformers_imported': False}
    first, second = [root / 'models' / rows[0]['artifact_id'] for root in roots]
    paths = sorted(p.relative_to(first) for p in first.rglob('*.json'))
    assert len(paths) >= 4
    for relative in paths:
        assert (first / relative).read_bytes() == (second / relative).read_bytes()
        assert b'/workspaces/' not in (first / relative).read_bytes()
        assert b'/tmp/' not in (first / relative).read_bytes()


def test_tampered_graph_and_wrong_call_contract_rejected(bert_artifacts, tmp_path):
    roots, rows = bert_artifacts
    original = roots[0] / 'models' / rows[0]['artifact_id']
    directory = tmp_path / 'artifact'
    shutil.copytree(original, directory)
    contract = verify_artifact(ROOT, directory)
    contract['inputs'][0]['name'] = 'wrong_name'
    write_json(directory / 'contract.json', contract)
    with pytest.raises(ValueError, match='saved call signature'):
        verify_artifact(ROOT, directory)
    contract = json.loads((original / 'contract.json').read_text())
    contract['inputs'][0]['dtype'] = 'float32'
    write_json(directory / 'contract.json', contract)
    with pytest.raises(ValueError, match='dtype/rank'):
        verify_artifact(ROOT, directory)
    shutil.rmtree(directory)
    shutil.copytree(original, directory)
    graph = directory / 'models/model.json'
    graph.write_text(graph.read_text() + ' ')
    with pytest.raises(ValueError, match='hash mismatch'):
        verify_artifact(ROOT, directory)


def test_fixed_slice_arguments_agree_with_saved_graph(bert_artifacts):
    roots, rows = bert_artifacts
    directory = roots[0] / 'models' / rows[0]['artifact_id']
    graph = json.loads((directory / 'models/model.json').read_text())
    node = next(node for node in graph['graph_module']['graph']['nodes']
                if node['target'] == 'torch.ops.aten.slice.Tensor')
    actual = {arg['name']: arg['arg']['as_int'] for arg in node['inputs'] if arg['name'] != 'self'}
    actual.setdefault('step', 1)
    config = next(config for op, config, _ in rows[0]['ops']['func'] if op == 'aten.slice.Tensor')
    assert {name: config[name] for name in actual} == actual
    assert actual == {'dim': 1, 'start': 0, 'end': 16, 'step': 1}
    facts = json.loads((directory / 'models/op_facts.json').read_text())
    assert next(config for op, config, _ in facts['ops'] if op == 'aten.slice.Tensor') == config


def test_interrupted_publish_restores_old_complete_artifact(tmp_path, monkeypatch):
    destination = tmp_path / 'artifact'
    stage = tmp_path / 'stage'
    destination.mkdir()
    stage.mkdir()
    (destination / 'contract.json').write_text('old')
    (stage / 'contract.json').write_text('new')
    original_replace = os.replace

    def interrupt(source, target):
        if Path(source) == stage:
            raise OSError('interrupted directory replacement')
        original_replace(source, target)

    monkeypatch.setattr(os, 'replace', interrupt)
    with pytest.raises(OSError):
        publish(stage, destination)
    assert (destination / 'contract.json').read_text() == 'old'
    assert not destination.with_name('artifact.previous').exists()


def test_worker_timeout_and_crash_do_not_destroy_following_result(tmp_path):
    script = tmp_path / 'worker.py'
    script.write_text('import json, os, sys, time\n'
                      'from hf_pt2_tools.registry import digest\n'
                      'if sys.argv[1] == "hang": time.sleep(10)\n'
                      'if sys.argv[1] == "crash": os._exit(23)\n'
                      'assert os.environ["HF_HUB_OFFLINE"] == "1"\n'
                      'assert os.environ["TRANSFORMERS_OFFLINE"] == "1"\n'
                      'print(json.dumps({"status":"ok", "hash":digest({"a":1})}))\n')
    assert run_worker(script, ['hang'], 'bad', 1)['status'] == 'timeout'
    assert run_worker(script, ['crash'], 'bad', 10)['status'] == 'crashed'
    assert run_worker(script, ['good'], 'good', 10)['status'] == 'ok'


def test_resume_key_changes_with_recipe_policy(bert_artifacts):
    entry = read_manifest(ROOT)['models'][0]
    args = argparse.Namespace(population='tiny', dtype='fp32', shape='static')
    baseline = source_key(ROOT, entry, args)
    changed = {**entry, 'output_fields': ['pooler_output']}
    assert source_key(ROOT, changed, args) != baseline
    args.dtype = 'bf16'
    assert source_key(ROOT, entry, args) != baseline


def test_stage_failure_and_stale_version_scoped_exclusion():
    row = {'artifact_id': 'example', 'status': 'ok', 'policy': 'dynamo',
           'producer': {'versions': {'torch': '2.12.0+cpu'}, 'core_revision': 'revision'},
           'stages': {'decomposition': {'status': 'failed'}}}
    exclusion = {'artifact_id': 'example', 'stage': 'decomposition', 'policy': 'dynamo',
                 'versions': {'torch': '2.12.0+cpu'}, 'reason': 'reviewed decomposition failure'}
    assert check_outcomes({'example': row}, [])['unexpected_failures']
    assert not check_outcomes({'example': row}, [exclusion])['unexpected_failures']
    assert check_outcomes({'example': row}, [{**exclusion, 'versions': {'torch': 'old'}}])['stale_exclusions']
    row['stages']['decomposition']['status'] = 'ok'
    assert check_outcomes({'example': row}, [exclusion])['stale_exclusions']


def test_dynamic_shared_inputs_and_second_shape(tmp_path):
    row = run_worker(ROOT / 'scripts/worker.py',
                    ['worker', '--root', ROOT, '--output', tmp_path, '--subset', 'bert-tiny', '--shape', 'dynamic'],
                    'dynamic-bert', 300)
    assert row['status'] == 'ok', row
    assert row['fresh_load']['cases'] == 3
    assert row['dynamic_rejection_verified']
    slices = [config for op, config, _ in row['ops']['func'] if op == 'aten.slice.Tensor']
    assert any(config['end'] == {'$symint': True} for config in slices)
    assert all(config['step'] == 1 for config in slices)
    contract = verify_artifact(ROOT, tmp_path / 'models' / row['artifact_id'])
    assert contract['dynamic_constraints']['shared_inputs'] == ['input_ids', 'attention_mask', 'token_type_ids']


def test_processor_derived_vlm_tensor_boundary(tmp_path):
    row = run_worker(ROOT / 'scripts/worker.py',
                    ['worker', '--root', ROOT, '--output', tmp_path, '--subset', 'smolvlm-256m'],
                    'vlm', 300)
    assert row['status'] == 'ok', row
    contract = verify_artifact(ROOT, tmp_path / 'models' / row['artifact_id'])
    assert row['fresh_load']['cases'] == 2
    assert contract['call']['kwargs'] == ['input_ids', 'attention_mask', 'pixel_values', 'pixel_attention_mask']


@pytest.mark.parametrize('name,steps,components', [
    ('smollm2-135m', 5, {'prefill', 'decode'}),
    ('t5-small', 5, {'encoder', 'prefill', 'decode'}),
    ('whisper-tiny', 5, {'encoder', 'prefill', 'decode'}),
    ('smolvlm-256m', 6, {'vision', 'connector', 'prefill', 'decode'}),
])
def test_generation_successive_state_reset_capacity_and_fresh_load(tmp_path, name, steps, components):
    result = run_worker(ROOT / 'scripts/worker.py',
                        ['generation-worker', '--root', ROOT, '--output', tmp_path, '--subset', name], name, 300)
    assert result['status'] == 'verified', result
    assert result['successive_steps'] == steps
    assert set(result['components']) == components
    assert result['cache_reset_verified'] and result['capacity_rejection_verified']
    assert result['upstream_export_for_generation']['status'] == 'exported'
    for component in result['components'].values():
        assert not component['fresh_load']['transformers_imported']
        verify_artifact(ROOT, tmp_path / 'models' / component['artifact_id'])


def diagnostics(row, output):
    logs = {str(p.relative_to(output)): p.read_text()[-1500:] for p in sorted(Path(output).rglob('*.log'))}
    return {'failed_stage': row.get('failed_stage'), 'error_category': row.get('error_category'), 'logs': logs}


def _bundle(root, row, output):
    from hf_pt2_tools.fixtures import build_bundle
    identity = row['artifact_id']
    return build_bundle(ROOT, root / 'models' / identity, root / '.build' / identity, output)


def test_bundle_replays_flat_cases_with_torch_only_and_is_reproducible(bert_artifacts, tmp_path):
    from hf_pt2_tools.fixtures import verify_bundle
    roots, rows = bert_artifacts
    manifests = [_bundle(root, row, tmp_path / str(i)) for i, (root, row) in enumerate(zip(roots, rows, strict=True))]
    stable = [{k: v for k, v in m['members'].items() if not k.endswith(('.pt', '.pt2'))} for m in manifests]
    assert stable[0] == stable[1] and 'cases.json' in stable[0]
    assert manifests[0]['cases'] == ['case-00', 'case-01']
    assert manifests[0]['weight_source']['kind'] == 'random'
    assert {'model.pt2', 'cases.json', 'cases/case-00/inputs.pt', 'cases/case-01/outputs.pt'} <= set(manifests[0]['members'])
    archive = tmp_path / '0' / manifests[0]['archive']['name']
    assert verify_bundle(ROOT, archive) == {'status': 'ok', 'cases': 2, 'transformers_imported': False}


@pytest.mark.parametrize('member', ['models/model.json', 'model.pt2', 'cases/case-00/inputs.pt', 'cases/case-01/outputs.pt'])
def test_corrupt_bundle_member_rejected_before_use(bert_artifacts, tmp_path, member):
    import gzip
    import io
    import tarfile
    from hf_pt2_tools.fixtures import verify_bundle
    roots, rows = bert_artifacts
    manifest = _bundle(roots[0], rows[0], tmp_path / 'good')
    good = tmp_path / 'good' / manifest['archive']['name']
    bad = tmp_path / 'bad.tar.gz'
    buffer = io.BytesIO()
    with tarfile.open(good) as source, gzip.GzipFile(fileobj=buffer, mode='wb', mtime=0) as compressed, \
            tarfile.open(fileobj=compressed, mode='w') as target:
        for info in source.getmembers():
            data = source.extractfile(info).read()
            if info.name == member:
                data = data[:-1] + bytes([data[-1] ^ 1])
            info.size = len(data)
            target.addfile(info, io.BytesIO(data))
    bad.write_bytes(buffer.getvalue())
    shutil.copy(tmp_path / 'good' / (good.name.removesuffix('.tar.gz') + '.manifest.json'),
                tmp_path / 'bad.manifest.json')
    with pytest.raises(ValueError):
        verify_bundle(ROOT, bad)
    # the manifest hash check must hold even when the archive digest is re-pinned
    pinned = json.loads((tmp_path / 'bad.manifest.json').read_text())
    pinned['archive'] = {'name': bad.name, 'sha256': hashlib.sha256(bad.read_bytes()).hexdigest(), 'size': bad.stat().st_size}
    (tmp_path / 'bad.manifest.json').write_text(json.dumps(pinned))
    with pytest.raises(ValueError, match='digest'):
        verify_bundle(ROOT, bad, tmp_path / 'bad.manifest.json')


def test_case_digest_is_content_based_and_order_sensitive():
    import torch
    from hf_pt2_tools.fixtures import tensor_digest
    a, b = torch.arange(4), torch.ones(2, 2)
    assert tensor_digest({'a': a, 'b': b}) == tensor_digest({'a': a.clone(), 'b': b.clone()})
    assert tensor_digest({'a': a, 'b': b}) != tensor_digest({'b': b, 'a': a})
    assert tensor_digest({'a': a}) != tensor_digest({'a': a.to(torch.int32)})


def test_catalogue_lists_artifacts_with_weight_source(bert_artifacts, tmp_path):
    from hf_pt2_tools.fixtures import catalogue
    roots, rows = bert_artifacts
    shutil.copytree(ROOT / 'schemas', tmp_path / 'schemas')
    shutil.copytree(roots[0] / 'models', tmp_path / 'models')
    entries = catalogue(tmp_path)['artifacts']
    assert [e['artifact_id'] for e in entries] == [rows[0]['artifact_id']]
    assert entries[0]['weight_source']['kind'] == 'random' and entries[0]['cases']['ids'] == ['case-00', 'case-01']
    assert 'cases.json' in entries[0]['files']


def test_binding_accounts_for_every_capture_by_source(bert_artifacts, tmp_path):
    import torch
    from hf_pt2_tools.artifacts import file_hash
    from hf_pt2_tools.checkpoints import bind_snapshot
    from hf_pt2_tools.registry import build_model
    roots, rows = bert_artifacts
    entry = next(e for e in read_manifest(ROOT)['models'] if e['id'] == 'bert-tiny')
    model, _ = build_model(ROOT, entry)
    with torch.no_grad():
        for parameter in model.parameters():
            parameter.add_(1.0)
    snapshot = tmp_path / 'snapshot'
    model.save_pretrained(snapshot, safe_serialization=True)
    reference = {'repo': 'local/bert-tiny', 'revision': '0' * 40, 'safetensors_files': ['model.safetensors'],
                 'config_sha256': file_hash(snapshot / 'config.json')}
    identity = rows[0]['artifact_id']
    artifact = roots[0] / 'models' / identity
    binding = bind_snapshot(ROOT, entry, reference, snapshot, artifact / 'models/model.json', tmp_path / 'binding.json',
                            population='tiny')
    kinds = {}
    for capture in binding['captures']:
        kinds.setdefault((capture['kind'], capture['source']['kind']), []).append(capture)
    assert set(kinds) == {('PARAMETER', 'checkpoint'), ('BUFFER', 'payload'), ('CONSTANT_TENSOR', 'payload')}
    assert all(c['source']['library_verified'] for c in kinds[('BUFFER', 'payload')])
    assert not any(c['source']['library_verified'] for c in kinds[('CONSTANT_TENSOR', 'payload')])
    assert binding['unmapped'] == []
    with pytest.raises(ValueError, match='cached config'):
        bind_snapshot(ROOT, entry, {**reference, 'config_sha256': '0' * 64}, snapshot,
                      artifact / 'models/model.json', tmp_path / 'x.json', population='tiny')


def test_checkpoint_backed_export_has_distinct_identity_and_swapped_payload_fails(tmp_path):
    import torch
    from hf_pt2_tools.artifacts import file_hash
    from hf_pt2_tools.fixtures import build_bundle, verify_bundle
    from hf_pt2_tools.registry import build_model
    entry = next(e for e in read_manifest(ROOT)['models'] if e['id'] == 'tinyclip')
    model, _ = build_model(ROOT, entry)
    with torch.no_grad():
        for parameter in model.parameters():
            parameter.add_(0.5)
    snapshot = tmp_path / 'snapshot'
    model.save_pretrained(snapshot, safe_serialization=True)
    rows = {}
    for label, extra in (('random', []), ('checkpoint', ['--snapshot', snapshot, '--allow-unpinned-snapshot'])):
        output = tmp_path / label
        rows[label] = run_worker(ROOT / 'scripts/worker.py',
                                 ['worker', '--root', ROOT, '--output', output, '--subset', 'tinyclip', *extra],
                                 label, 300)
        if rows[label]['status'] != 'ok':
            pytest.fail(json.dumps(diagnostics(rows[label], output)))
    random_id, checkpoint_id = rows['random']['artifact_id'], rows['checkpoint']['artifact_id']
    assert checkpoint_id == random_id + '/ckpt-' + entry['reference']['revision'][:12]
    contracts = {label: verify_artifact(ROOT, tmp_path / label / 'models' / row['artifact_id']) for label, row in rows.items()}
    assert contracts['random']['weights'] == {'kind': 'random', 'model_seed': 0}
    weights = contracts['checkpoint']['weights']
    assert weights['kind'] == 'checkpoint' and not weights['pinned_config_match']
    assert weights['files']['model.safetensors']['sha256'] == file_hash(snapshot / 'model.safetensors')
    assert contracts['random']['recipe_sha256'] != contracts['checkpoint']['recipe_sha256']
    cases = {label: json.loads((tmp_path / label / 'models' / row['artifact_id'] / 'cases.json').read_text())
             for label, row in rows.items()}
    assert cases['checkpoint']['weight_source'] == weights
    assert cases['random']['cases'][0]['outputs_sha256'] != cases['checkpoint']['cases'][0]['outputs_sha256']
    good = build_bundle(ROOT, tmp_path / 'random/models' / random_id, tmp_path / 'random/.build' / random_id, tmp_path / 'bundles')
    assert verify_bundle(ROOT, tmp_path / 'bundles' / good['archive']['name'])['status'] == 'ok'
    with pytest.raises(ValueError, match='no v2 map for checkpoint-backed'):
        build_bundle(ROOT, tmp_path / 'checkpoint/models' / checkpoint_id, tmp_path / 'checkpoint/.build' / checkpoint_id,
                     tmp_path / 'checkpoint-bundles')
    swapped = tmp_path / 'swapped'
    shutil.copytree(tmp_path / 'random/.build' / random_id, swapped)
    shutil.copy(tmp_path / 'checkpoint/.build' / checkpoint_id / 'model.pt2', swapped / 'model.pt2')
    build_bundle(ROOT, tmp_path / 'random/models' / random_id, swapped, tmp_path / 'swapped-bundles')
    with pytest.raises(RuntimeError, match='torch-only replay'):
        verify_bundle(ROOT, tmp_path / 'swapped-bundles' / good['archive']['name'])


def test_static_decode_variants_pin_history_and_reject_others(tmp_path):
    result = run_worker(ROOT / 'scripts/worker.py',
                        ['generation-worker', '--root', ROOT, '--output', tmp_path, '--subset', 'smollm2-135m',
                         '--static-history', '5,7'], 'static', 300)
    if result['status'] != 'verified':
        pytest.fail(json.dumps(diagnostics(result, tmp_path)))
    assert set(result['static_variants']) == {'5', '7'}
    dynamic = verify_artifact(ROOT, tmp_path / 'models' / result['components']['decode']['artifact_id'])
    assert dynamic['dynamic_constraints']['history'] == [1, 8] and 'variant' not in dynamic
    for history, component in result['static_variants'].items():
        assert component['artifact_id'].endswith(f'/decode/fp32/dynamo/static-h{history}')
        assert component['rejected_other_histories'] == 9 and component['case_sequences'] == ['initial', 'reset']
        document = json.loads((tmp_path / 'models' / component['artifact_id'] / 'cases.json').read_text())
        assert len(document['cases']) == 2 and document['cases'][0]['inputs_sha256'] != document['cases'][1]['inputs_sha256']
        contract = verify_artifact(ROOT, tmp_path / 'models' / component['artifact_id'])
        assert contract['variant'] == {'kind': 'static-history', 'history': int(history), 'attention_length': int(history) + 1}
        assert contract['dynamic_constraints'] == {} and contract['exporter']['shape_policy'] == 'static'
        shapes = {t['name']: t['shape'] for t in contract['inputs']}
        assert shapes['past_0_key'][2] == int(history) and shapes['attention_mask'][1] == int(history) + 1


def test_tinyclip_towers_are_independent_components_matching_the_whole_model(tmp_path):
    result = run_worker(ROOT / 'scripts/worker.py',
                        ['encoders-worker', '--root', ROOT, '--output', tmp_path, '--subset', 'tinyclip'], 'towers', 300)
    if result['status'] != 'verified':
        pytest.fail(json.dumps(result)[:2000] + str(sorted((tmp_path / '.build/encoders').glob('*.log'))))
    assert set(result['components']) == {'image-encoder', 'text-encoder'}
    for component, inputs, output in (('image-encoder', ['pixel_values'], 'image_features'),
                                      ('text-encoder', ['input_ids', 'attention_mask'], 'text_features')):
        contract = verify_artifact(ROOT, tmp_path / 'models' / result['components'][component]['artifact_id'])
        assert [t['name'] for t in contract['inputs']] == inputs and [t['name'] for t in contract['outputs']] == [output]
        assert contract['verified_cases'] == 2 and 'state' not in contract
        captures = json.loads((tmp_path / 'models' / contract['artifact_id'] / 'captures.json').read_text())
        other = 'text' if component == 'image-encoder' else 'vision'
        assert not any(row['target'].startswith(other) or row['target'].startswith('visual' if other == 'vision' else 'text')
                       for row in captures['captures'])


def test_matrix_separates_producer_stages_from_consumer_admission(bert_artifacts, tmp_path):
    from hf_pt2_tools.fixtures import build_bundle
    from hf_pt2_tools.matrix import BASE_MODELS, NOT_MEASURED, build_matrix
    roots, rows = bert_artifacts
    identity = rows[0]['artifact_id']
    evidence = tmp_path / 'run'
    write_json(evidence / 'results/checkpoint.json', {'models': {'bert-tiny': {'status': 'ok', 'artifact_id': identity}}})
    build_bundle(ROOT, roots[0] / 'models' / identity, roots[0] / '.build' / identity, evidence / 'bundles')
    document = build_matrix(ROOT, evidence, tmp_path / 'matrix.md')
    by_model = {r['model']: r for r in document['rows']}
    assert [r['model'] for r in document['rows']] == list(BASE_MODELS)
    bert = by_model['bert-tiny']
    assert (bert['export'], bert['bind'], bert['map_v2'], bert['offline_replay']) == ('ok', 'not run', 'not run', 'ok')
    assert all(r['consumer_admission'] == NOT_MEASURED for r in document['rows'])
    assert by_model['yolos-tiny']['export'] == 'not run'
    assert '| bert-tiny | forward | ok |' in (tmp_path / 'matrix.md').read_text()


def _bf16_bert_binding(bert_artifacts, tmp_path):
    import torch
    from hf_pt2_tools.artifacts import file_hash
    from hf_pt2_tools.checkpoints import bind_snapshot
    from hf_pt2_tools.registry import build_model
    roots, rows = bert_artifacts
    entry = next(e for e in read_manifest(ROOT)['models'] if e['id'] == 'bert-tiny')
    model, _ = build_model(ROOT, entry)
    model.to(torch.bfloat16)
    snapshot = tmp_path / 'snapshot'
    model.save_pretrained(snapshot, safe_serialization=True)
    reference = {'repo': 'local/bert-tiny', 'revision': '0' * 40, 'safetensors_files': ['model.safetensors'],
                 'config_sha256': file_hash(snapshot / 'config.json')}
    identity = rows[0]['artifact_id']
    artifact = roots[0] / 'models' / identity
    binding = bind_snapshot(ROOT, entry, reference, snapshot, artifact / 'models/model.json', tmp_path / 'binding.json',
                            population='tiny')
    return binding, snapshot, identity, artifact, roots[0] / '.build' / identity / 'model.pt2'


def test_map_v2_declares_conversion_and_reproduces_every_capture(bert_artifacts, tmp_path, monkeypatch):
    import copy
    from pt2_export_core.opgraph import strict_json_loads
    from pt2_export_core.schema_validate import validate_document
    from hf_pt2_tools import mapv2
    binding, snapshot, identity, artifact, program = _bf16_bert_binding(bert_artifacts, tmp_path)
    base = 'https://github.com/o/r/releases/download/t1/'
    output = tmp_path / 'maps'
    document = mapv2.build_map_v2(binding, snapshot, program, output, identity, base)
    validate_document(strict_json_loads(json.dumps(document)), 'checkpoint-map-v2', str(ROOT / 'schemas'))
    origins = {name: entry['origin'] for name, entry in document['tensors'].items()}
    cast = origins['model.embeddings.word_embeddings.weight']
    assert cast['kind'] == 'checkpoint' and cast['convert'] == {'op': 'cast', 'from': 'BF16', 'to': 'F32'}
    assert document['tensors']['model.embeddings.word_embeddings.weight']['dtype'] == 'F32'
    assert origins['model.embeddings.token_type_ids'] == {'kind': 'generated', 'op': 'fill', 'element_hex': '00' * 8}
    assert 'graph_owned' not in document['sources']
    source = document['sources']['checkpoint']['files'][0]
    assert source['url'] == f"https://huggingface.co/local/bert-tiny/resolve/{'0' * 40}/model.safetensors"
    captures = json.loads((artifact / 'captures.json').read_text())['captures']
    graph_sha = json.loads((artifact / 'contract.json').read_text())['graph_sha256']
    mapv2.check_structure(document, captures, identity, graph_sha)
    files = tmp_path / 'files'
    files.mkdir()
    shutil.copy(snapshot / 'model.safetensors', files / 'model.safetensors')
    loaded = mapv2.load_tensors(document, files)
    assert sorted(loaded) == sorted(c['target'] for c in captures)
    # inline and pack origins for graph-owned values, forced by disabling the uniform shortcut
    monkeypatch.setattr(mapv2, '_generator', lambda value: None)
    monkeypatch.setattr(mapv2, 'INLINE_LIMIT', 16)
    forced = mapv2.build_map_v2(binding, snapshot, program, tmp_path / 'forced', identity, base)
    kinds = {entry['origin']['kind'] for entry in forced['tensors'].values()}
    assert {'inline', 'pack', 'checkpoint'} <= kinds and forced['sources']['graph_owned']['url'].startswith(base)
    shutil.copy(tmp_path / 'forced' / forced['sources']['graph_owned']['name'], files / forced['sources']['graph_owned']['name'])
    assert sorted(mapv2.load_tensors(forced, files)) == sorted(loaded)
    # a wrong declaration, digest, structure or source is refused
    for mutate, message in [
            (lambda d: d['tensors']['model.embeddings.word_embeddings.weight']['origin']['convert'].update(**{'from': 'F16'}), 'declared conversion'),
            (lambda d: d['tensors']['model.embeddings.word_embeddings.weight'].update(sha256='0' * 64), 'pinned digest'),
            (lambda d: d['tensors']['model.embeddings.word_embeddings.weight'].update(shape=[1, 1]), 'wrong dtype/shape'),
            (lambda d: d['sources']['checkpoint']['files'][0].update(sha256='0' * 64), 'differs from its pin')]:
        broken = copy.deepcopy(document)
        mutate(broken)
        with pytest.raises(ValueError, match=message):
            mapv2.load_tensors(broken, files)
    for mutate, message in [(lambda d: d['tensors'].pop('model.embeddings.word_embeddings.weight'), 'exactly the captured'),
                            (lambda d: d.update(graph_sha256='0' * 64), 'different artifact or graph')]:
        broken = copy.deepcopy(document)
        mutate(broken)
        with pytest.raises(ValueError, match=message):
            mapv2.check_structure(broken, captures, identity, graph_sha)
    # a slim bundle carries the v2 map, leaves out model.pt2 and the full pack, and verifies without torch replay
    from hf_pt2_tools.fixtures import build_bundle, publication_index, verify_bundle
    build = bert_artifacts[0][0] / '.build' / identity
    slim = build_bundle(ROOT, artifact, build, tmp_path / 'slim', maps=tmp_path / 'forced')
    assert slim['payload'] is None and 'model.pt2' not in slim['members'] and 'pack' not in slim
    assert slim['members']['models/safetensors.v2.json'] and slim['map_v2']['assets'][0]['name'].endswith('.graph-owned.safetensors')
    assert verify_bundle(ROOT, tmp_path / 'slim' / slim['archive']['name']) == {'status': 'ok', 'cases': 2, 'replay': 'not included (slim bundle)'}
    index = publication_index(tmp_path / 'slim', 'o/r', 't1')
    assert any(name.startswith('v2:') for name in index['artifacts'][0]['assets'])
