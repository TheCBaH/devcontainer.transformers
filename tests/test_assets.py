import json
from pathlib import Path

from hf_pt2_tools.assets import FAMILIES, input_agreement, raw_audio, raw_image
from hf_pt2_tools.registry import read_manifest

ROOT = Path(__file__).resolve().parents[1]


def test_committed_task_assets_cover_every_base_model_at_its_pinned_revision():
    document = json.loads((ROOT / 'task-assets.json').read_text())
    entries = {e['id']: e for e in read_manifest(ROOT)['models']}
    assert sorted(row['model_id'] for row in document['models']) == sorted(FAMILIES)
    for row in document['models']:
        reference = entries[row['model_id']]['reference']
        assert (row['repo'], row['revision']) == (reference['repo'], reference['revision'])
        for name, asset in row['files'].items():
            assert len(asset['sha256']) == 64 and asset['size'] > 0
            assert asset['url'] == f"https://huggingface.co/{row['repo']}/resolve/{row['revision']}/{name}"
        assert row['example'], row['model_id']
        for example in row['example'].values():
            assert example.get('status') != 'failed'
            assert all(len(t['sha256']) == 64 and t['shape'] for t in example.get('tensors', {}).values())
    config = next(r for r in document['models'] if r['model_id'] == 'bert-tiny')
    assert config['recipe']['text']['special_tokens']['pad_token'] == {'token': '[PAD]', 'id': 0}


def test_raw_inputs_are_deterministic_and_agreement_reports_shape_gaps():
    assert (raw_image() == raw_image()).all() and raw_image().shape == (96, 128, 3)
    assert (raw_audio(16000) == raw_audio(16000)).all() and raw_audio(16000).dtype.name == 'float32'
    record = {'example': {'image': {'tensors': {'pixel_values': {'dtype': 'float32', 'shape': [1, 3, 512, 512]}}},
                          'tokenizer': {'tensors': {'input_ids': {'dtype': 'int64', 'shape': [1, 4]}}}}}
    entry = {'reference_inputs': {'pixel_values': {'dtype': 'float32', 'shape': [1, 3, 224, 224]},
                                  'input_ids': {'dtype': 'int64', 'shape': [1, 4]}}}
    assert input_agreement(record, entry) == {'pixel_values': {
        'dtype_matches': True, 'rank_matches': True, 'shape_matches': False,
        'model_shape': [1, 3, 224, 224], 'processor_shape': [1, 3, 512, 512]}}
