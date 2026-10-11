import copy

import pytest
import torch

from hf_pt2_tools.artifacts import file_hash, write_json
from hf_pt2_tools.fixtures import reference_outputs, tensor_digest


@pytest.fixture
def reference(tmp_path):
    inputs = {'waveform': torch.tensor([[0.4, 1.8]])}
    expected = {'logits': torch.tensor([[1., 2.]])}
    row = {'artifact_id': 'test/audio/tiny/forward/fp32/dynamo/static', 'dtype': 'fp32',
           'config_sha256': 'c' * 64, 'recipe_sha256': 'd' * 64,
           'weights': {'kind': 'random', 'model_seed': 0},
           'producer': {'architecture': 'aarch64', 'versions': {'torch': 'test', 'transformers': 'test'}}}
    document = {'schema_version': 1, 'artifact_id': row['artifact_id'], 'architecture': 'aarch64',
                'model_class': 'TestModel', 'config_sha256': row['config_sha256'],
                'recipe_sha256': row['recipe_sha256'], 'weight_source': row['weights'],
                'versions': row['producer']['versions'],
                'cases': [{'inputs_sha256': tensor_digest(inputs), 'outputs_sha256': tensor_digest(expected),
                           'outputs': {'logits': {'dtype': 'float32', 'shape': [1, 2], 'values': [1., 2.]}}}]}
    path = tmp_path / 'reference.json'
    write_json(path, document)
    entry = {'model_class': 'TestModel', 'output_fields': ['logits'],
             'golden_outputs': {'path': path.name, 'sha256': file_hash(path)}}
    return tmp_path, entry, row, inputs, expected


def test_reference_preserves_exact_values_after_numeric_agreement(reference):
    root, entry, row, inputs, expected = reference
    observed = (torch.tensor([[1.000001, 2.]]),)
    result = reference_outputs(root, entry, row, [inputs], [observed])
    assert torch.equal(result[0][0], expected['logits'])
    assert tensor_digest({'logits': result[0][0]}) == tensor_digest(expected)
    assert not torch.equal(observed[0], result[0][0])


def test_reference_rejects_output_drift_outside_tolerance(reference):
    root, entry, row, inputs, expected = reference
    with pytest.raises(AssertionError):
        reference_outputs(root, entry, row, [inputs], [(torch.tensor([[1.01, 2.]]),)])


@pytest.mark.parametrize('key', ['config_sha256', 'recipe_sha256'])
def test_reference_rejects_changed_model_recipe(reference, key):
    root, entry, row, inputs, expected = reference
    row[key] = 'e' * 64
    with pytest.raises(ValueError, match=key):
        reference_outputs(root, entry, row, [inputs], [tuple(expected.values())])


def test_reference_rejects_changed_inputs_and_corruption(reference):
    root, entry, row, inputs, expected = reference
    changed = copy.deepcopy(inputs)
    changed['waveform'][0, 0] += 0.1
    with pytest.raises(ValueError, match='inputs mismatch'):
        reference_outputs(root, entry, row, [changed], [tuple(expected.values())])
    entry['golden_outputs']['sha256'] = '0' * 64
    with pytest.raises(ValueError, match='hash mismatch'):
        reference_outputs(root, entry, row, [inputs], [tuple(expected.values())])


def test_other_architecture_or_profile_keeps_its_own_outputs(reference):
    root, entry, row, inputs, expected = reference
    observed = [(torch.tensor([[3., 4.]]),)]
    row['producer']['architecture'] = 'x86_64'
    assert reference_outputs(root, entry, row, [inputs], observed) is observed
    row['producer']['architecture'] = 'aarch64'
    row['artifact_id'] = 'test/audio/reference/forward/fp32/dynamo/static'
    assert reference_outputs(root, entry, row, [inputs], observed) is observed
