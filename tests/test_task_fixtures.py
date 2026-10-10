import copy
import importlib.util
import io
import json
from pathlib import Path
import tarfile
import sys

import pytest
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from task_fixtures.integrity import (build_index, check_contract, check_request, digest, extract,
                                     file_pin, pack, read_json, tensor_records, verify_bundle,
                                     verify_index, write_json)


def contract(directory):
    value = torch.tensor([[1, 2]], dtype=torch.int64)
    (directory / 'inputs.pt').parent.mkdir(parents=True, exist_ok=True)
    torch.save({'input_ids': value}, directory / 'inputs.pt')
    output = torch.tensor([[0.125, -0.25]])
    for role in ('outputs', 'exported'):
        torch.save({'hidden': output}, directory / (role + '.pt'))
    (directory / 'text.txt').write_bytes(b'hello')
    reference = {'artifact_id': 'bert-tiny/text-encoder/reference/forward/fp32/dynamo/static/ckpt-123456789abc',
                 'weight_source': {'revision': '1' * 40}, 'producer_commit': '2' * 40,
                 'graph_sha256': '3' * 64, 'tolerances': {'atol': 1e-5, 'rtol': 1e-4},
                 'contract': {'sha256': '4' * 64, 'size': 10}, 'graph': {'sha256': '3' * 64, 'size': 10},
                 'map': {'sha256': '5' * 64, 'size': 10}, 'config': {'sha256': '6' * 64, 'size': 10},
                 'inputs': [{'name': 'input_ids', 'dtype': 'int64', 'shape': [1, 2]}],
                 'outputs': [{'name': 'hidden', 'dtype': 'float32', 'shape': [1, 2]}]}
    recipe = {'text': 'hello'}
    result = {'schema_version': 1, 'tensor_format': 'torch-flat-tensor-map-v1', 'kind': 'acceptance',
              'artifact_id': reference['artifact_id'], 'references': [reference], 'recipe_id': 'text-v1',
              'recipe': recipe, 'recipe_sha256': digest(recipe), 'generator': {'commit': '7' * 40, 'lock_sha256': '8' * 64},
              'request_sha256': '9' * 64, 'tolerances': reference['tolerances'],
              'expected_cases': ['case-00'], 'reference_publication': {'sha256': 'a' * 64, 'size': 10},
              'cases': [{'id': 'case-00', 'raw': [{'path': 'text.txt', **file_pin(directory / 'text.txt')}],
                         'files': {'inputs.pt': {'tensors': tensor_records({'input_ids': value})},
                                   'outputs.pt': {'tensors': tensor_records({'hidden': output})},
                                   'exported.pt': {'tensors': tensor_records({'hidden': output})}}}]}
    result['fixture_id'] = f"{result['artifact_id']}/task/text-v1/{digest(recipe)}/generator/{'7' * 40}/request/{'9' * 64}"
    return result


def test_task_bundle_data_and_reproducible_archive(tmp_path):
    payload, output = tmp_path / 'payload', tmp_path / 'output'
    document = contract(payload)
    manifest = pack(payload, output, document)
    first = read_json(manifest)
    assert verify_bundle(manifest, output, tensors=True) == document
    pack(payload, output, document)
    assert read_json(manifest) == first
    with tarfile.open(output / first['archive']['name']) as tar:
        assert all(info.isfile() for info in tar)
        assert 'model.pt2' not in tar.getnames()


@pytest.mark.parametrize('mutation', ['recipe', 'artifact', 'case', 'missing_case', 'tolerance', 'checkpoint', 'dtype'])
def test_wrong_recipe_revision_or_coverage_fails(tmp_path, mutation):
    value = contract(tmp_path)
    if mutation == 'recipe':
        value['recipe']['text'] = 'changed'
    elif mutation == 'artifact':
        value['artifact_id'] += '-wrong'
    elif mutation == 'case':
        value['expected_cases'].append('case-01')
    elif mutation == 'missing_case':
        value['cases'] = []
    elif mutation == 'tolerance':
        value['tolerances'] = {'atol': 1, 'rtol': 1}
    elif mutation == 'checkpoint':
        value['references'].append(copy.deepcopy(value['references'][0]))
        value['references'][1]['weight_source']['revision'] = 'b' * 40
    else:
        value['references'][0]['artifact_id'] = value['references'][0]['artifact_id'].replace('/fp32/', '/bf16/')
    with pytest.raises(ValueError):
        check_contract(value)


def test_missing_corrupt_and_tensor_content_fail(tmp_path):
    payload, output = tmp_path / 'payload', tmp_path / 'output'
    document = contract(payload)
    manifest = pack(payload, output, document)
    record = read_json(manifest)
    archive = output / record['archive']['name']
    original = archive.read_bytes()
    archive.write_bytes(original[:-1])
    with pytest.raises(ValueError, match='byte pin'):
        verify_bundle(manifest, output)
    archive.unlink()
    with pytest.raises(FileNotFoundError):
        verify_bundle(manifest, output)
    archive.write_bytes(original)
    document['cases'][0]['files']['inputs.pt']['tensors'][0]['sha256'] = 'b' * 64
    with pytest.raises(ValueError, match='tensor names, content'):
        pack(payload, output, document)


@pytest.mark.parametrize('mutation', ['route', 'output_name', 'shape'])
def test_complete_named_routes_are_required(tmp_path, mutation):
    value = contract(tmp_path)
    files = value['cases'][0]['files']
    if mutation == 'route':
        del files['exported.pt']
    elif mutation == 'output_name':
        files['outputs.pt']['tensors'][0]['name'] = 'missing-hidden'
    else:
        files['outputs.pt']['tensors'][0]['shape'] = [1, 3]
    with pytest.raises(ValueError, match='incomplete|component contract'):
        check_contract(value)


@pytest.mark.parametrize('name,kind', [('../escape', 'file'), ('x', 'symlink'), ('x', 'duplicate'), ('y', 'file'), ('x', 'missing')])
def test_archive_inventory_and_paths_fail(tmp_path, name, kind):
    archive = tmp_path / 'bad.tar.gz'
    with tarfile.open(archive, 'w:gz') as tar:
        if kind != 'missing':
            info = tarfile.TarInfo(name)
            info.size = 1
            if kind == 'symlink':
                info.type, info.linkname = tarfile.SYMTYPE, '/tmp/outside'
                info.size = 0
            tar.addfile(info, io.BytesIO(b'x'))
            if kind == 'duplicate':
                tar.addfile(info, io.BytesIO(b'x'))
    with pytest.raises(ValueError):
        extract(archive, tmp_path / 'extracted', {'x': {'sha256': __import__('hashlib').sha256(b'x').hexdigest(), 'size': 1}})


def test_index_pin_selection_and_complete_request(tmp_path):
    payload, output = tmp_path / 'payload', tmp_path / 'output'
    value = contract(payload)
    request = {'tasks': [{'recipe_id': 'text-v1'}], 'reference_publication': value['reference_publication']}
    value['request_sha256'] = digest(request)
    value['fixture_id'] = value['fixture_id'].rsplit('/', 1)[0] + '/' + digest(request)
    pack(payload, output, value)
    build_index(output, 'owner/repo', 'task-fixtures-123', request)
    pin = read_json(output / 'task-fixtures.pin.json')
    assert len(verify_index(output / 'task-fixtures.json', pin, output, tensors=True)['fixtures']) == 1
    bad = copy.deepcopy(pin)
    bad['sha256'] = '0' * 64
    with pytest.raises(ValueError, match='byte pin'):
        verify_index(output / 'task-fixtures.json', bad, output)
    request['tasks'].append({'recipe_id': 'absent-v1'})
    with pytest.raises(ValueError, match='missing, duplicate'):
        build_index(output, 'owner/repo', 'task-fixtures-123', request)


def test_source_request_selects_exact_nonrecursive_metadata():
    request = read_json(ROOT / 'task-fixture-request.json')
    recipes = read_json(ROOT / 'task-recipes.json')
    check_request(request, recipes)
    bad = copy.deepcopy(request)
    bad['tasks'][0]['recipe']['length'] = 224
    with pytest.raises(ValueError, match='exact source recipes'):
        check_request(bad, recipes)
    assert read_json(ROOT / 'catalogue.json')['artifacts']


def test_task_schemas_join_shared_registry():
    from pt2_export_core.schema_validate import _registry
    registry = _registry(str(ROOT / 'schemas'))
    for name in ('task-contract', 'task-manifest', 'task-index'):
        schema = read_json(ROOT / 'schemas' / (name + '.schema.json'))
        assert registry.contents(schema['$id']) == schema


def test_flat_map_refuses_custom_objects():
    with pytest.raises(ValueError, match='flat named'):
        tensor_records({'output': {'nested': torch.tensor(1)}})


def test_draft_publication_refuses_existing_identity(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location('publish_release', ROOT / 'scripts/publish-release.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    (tmp_path / 'x').write_bytes(b'x')
    write_json(tmp_path / 'task-fixtures.json', {'fixtures': [{'assets': {'archive': {
        'name': 'x', 'url': 'https://github.com/o/r/releases/download/tag/x', **file_pin(tmp_path / 'x')}}}]})
    calls = []
    def gh(*args):
        calls.append(args)
        return json.dumps({'isDraft': False, 'targetCommitish': 'commit'})
    monkeypatch.setattr(module, 'gh', gh)
    with pytest.raises(ValueError, match='already exists'):
        module.publish(tmp_path, 'o/r', 'tag', 'commit', 'task-fixtures.json')
    assert len(calls) == 1 and calls[0][:2] == ('release', 'view')
