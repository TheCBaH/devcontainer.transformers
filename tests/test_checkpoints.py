import copy
import json
from pathlib import Path
import shutil

import pytest
import torch
import transformers

from hf_pt2_tools import checkpoints
from hf_pt2_tools.artifacts import file_hash, write_json
from hf_pt2_tools.exporting import run
from hf_pt2_tools.registry import build_model, read_manifest

ROOT = Path(__file__).resolve().parents[1]


def test_sharded_tied_checkpoint_binding_and_value_mismatch(tmp_path, monkeypatch):
    entry = copy.deepcopy(next(e for e in read_manifest(ROOT)['models'] if e['id'] == 't5-small'))
    model, _ = build_model(ROOT, entry)
    model.to(torch.bfloat16)
    snapshot = tmp_path / 'checkpoint'
    model.save_pretrained(snapshot, max_shard_size='20KB', safe_serialization=True)
    files = sorted(p.name for p in snapshot.glob('*.safetensors'))
    assert len(files) > 1
    root = tmp_path / 'repo'
    (root / 'configs/reference').mkdir(parents=True)
    shutil.copy(snapshot / 'config.json', root / 'configs/reference/t5-small.json')
    shutil.copy(ROOT / 'uv.lock', root / 'uv.lock')
    shutil.copy(ROOT / 'pyproject.toml', root / 'pyproject.toml')
    (root / 'modules').symlink_to(ROOT / 'modules')
    shutil.copytree(ROOT / 'schemas', root / 'schemas')
    entry['reference'].update(config_sha256=file_hash(snapshot / 'config.json'), safetensors_files=files)
    write_json(root / 'model-candidates.yaml', {'schema_version': 1, 'models': [entry],
                                              'selection': {'max_weight_mb': 64}})
    monkeypatch.setattr(checkpoints, 'snapshot_download', lambda *args, **kwargs: snapshot)
    output = tmp_path / 'output'
    row = run(root, 't5-small', output, population='reference')
    assert row['status'] == 'ok', row
    graph = output / 'models' / row['artifact_id'] / 'models/model.json'
    mapped = checkpoints.bind(root, 't5-small', graph, tmp_path / 'bindings.json')
    assert mapped['status'] == 'verified'
    assert 'model.safetensors.index.json' in mapped['checkpoint_sha256']
    assert any(binding['tied_aliases'] for binding in mapped['bindings'])
    assert all(binding['source_dtype'] == 'torch.bfloat16' for binding in mapped['bindings'])
    assert all(binding['loaded_dtype'] == 'torch.float32' for binding in mapped['bindings'])
    original_load = transformers.T5ForConditionalGeneration.from_pretrained

    def wrong_library_load(*args, **kwargs):
        loaded = original_load(*args, **kwargs)
        with torch.no_grad():
            next(loaded.parameters()).add_(1)
        return loaded

    monkeypatch.setattr(transformers.T5ForConditionalGeneration, 'from_pretrained', wrong_library_load)
    with pytest.raises(ValueError, match='differs from library load'):
        checkpoints.bind(root, 't5-small', graph, tmp_path / 'wrong.json')
