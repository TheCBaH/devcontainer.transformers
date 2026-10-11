import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
SPEC = importlib.util.spec_from_file_location('rank_hub', ROOT / 'scripts/rank_hub.py')
RANK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RANK)


def test_global_ranking_retains_multiple_checkpoints_per_architecture():
    rows = [dict(repo='a/small', downloads=20, architecture='bert', status='eligible'),
            dict(repo='b/small', downloads=30, architecture='bert', status='eligible'),
            dict(repo='a/big', downloads=40, architecture='llama', status='too-large'),
            dict(repo='a/custom', downloads=50, architecture='custom', status='unsupported-architecture')]
    result = RANK.rankings(rows, 2)
    assert [row['repo'] for row in result['eligible']] == ['b/small', 'a/small']
    assert [row['repo'] for row in result['overall']] == ['a/big', 'b/small']


def test_metadata_errors_cannot_enter_rankings():
    result = RANK.rankings([dict(repo='a/error', downloads=100, architecture='bert',
                                status='metadata-error')], 100)
    assert result == {'eligible': [], 'overall': []}


@pytest.mark.parametrize('complete', [True, False])
def test_inspect_downloads_pinned_json_and_requires_all_shards(tmp_path, complete):
    candidate = SimpleNamespace(id='test/bert', sha='a' * 40, downloads=10,
                                private=False, gated=False)
    filenames = ['model-00001.safetensors', 'model.safetensors.index.json']
    if complete:
        filenames.append('model-00002.safetensors')
    files = [SimpleNamespace(rfilename=name, size=100, blob_id='b' * 40, lfs=None)
             for name in filenames]

    class Api:
        def model_info(self, repo, **kwargs):
            assert repo == candidate.id and kwargs['revision'] == candidate.sha
            assert kwargs['files_metadata']
            return SimpleNamespace(siblings=files, pipeline_tag='fill-mask')

    calls = []

    def download(repo, filename, **kwargs):
        assert repo == candidate.id and kwargs['revision'] == candidate.sha
        assert kwargs['token'] is False
        calls.append(filename)
        path = tmp_path / filename
        path.write_text('{"model_type":"bert"}' if filename == 'config.json' else
                        '{"weight_map":{"a":"model-00001.safetensors","b":"model-00002.safetensors"}}')
        return path

    row = RANK.inspect(candidate, Api(), download, {'bert': 'BertConfig'}, tmp_path)
    assert calls == ['config.json', 'model.safetensors.index.json']
    assert row['status'] == ('eligible' if complete else 'incomplete-shards')
    assert row['safetensors_total_bytes'] == (200 if complete else 100)


def test_main_queries_global_download_order_and_keeps_duplicate_architectures(tmp_path, monkeypatch):
    import huggingface_hub
    import json

    candidates = [SimpleNamespace(id=f'test/{name}', sha='a' * 40, downloads=downloads)
                  for name, downloads in [('large', 100), ('small1', 90), ('small2', 80), ('later', 70)]]

    class Api:
        def __init__(self, token):
            assert token is False

        def list_models(self, **kwargs):
            assert kwargs['filter'] == 'transformers'
            assert kwargs['sort'] == 'downloads'
            return candidates

    def inspect(candidate, *args):
        return dict(repo=candidate.id, revision=candidate.sha, downloads=candidate.downloads,
                    architecture='bert', status='too-large' if candidate.downloads == 100 else 'eligible')

    monkeypatch.setattr(huggingface_hub, 'HfApi', Api)
    monkeypatch.setattr(RANK, 'inspect', inspect)
    monkeypatch.setattr(RANK, 'pinned_architectures', lambda root: ('5.18.0', {'bert': 'BertConfig'}))
    output = tmp_path / 'ranking.json'
    monkeypatch.setattr(sys, 'argv', ['rank', '--count', '2', '--candidates', '4', '--output', str(output)])
    assert RANK.main() == 0
    document = json.loads(output.read_text())
    assert len(document['checked']) == 3 and document['status'] == 'complete'
    assert [r['repo'] for r in document['rankings']['eligible']] == ['test/small1', 'test/small2']
    assert [r['repo'] for r in document['rankings']['overall']] == ['test/large', 'test/small1']
