import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('catalogue_hub', ROOT / 'scripts/catalogue_hub.py')
SCAN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SCAN)


def file(name, size=None):
    return SimpleNamespace(rfilename=name, size=size, lfs=SimpleNamespace(sha256='a' * 64), blob_id='b' * 40)


def assess(files):
    return SCAN.assess_weights(SimpleNamespace(siblings=files))


def test_all_safetensors_count_including_additional_files():
    result = assess([file('model.safetensors', 600_000_000), file('extra/weights.safetensors', 400_000_000)])
    assert result == {'status': 'too-large', 'safetensors_total_bytes': 1_000_000_000}


@pytest.mark.parametrize('size,status', [(999_999_999, 'eligible'), (1_000_000_000, 'too-large'),
                                       (None, 'unknown-file-sizes'), (0, 'unknown-file-sizes')])
def test_strict_boundary_and_unknown_sizes(size, status):
    assert assess([file('model.safetensors', size)])['status'] == status


def test_adapters_and_bin_only_models_do_not_qualify():
    assert assess([file('adapter_model.safetensors', 100)])['status'] == 'no-full-checkpoint'
    assert assess([file('pytorch_model.bin', 100)])['status'] == 'no-safetensors'


def test_retry_honors_hub_reset_time(monkeypatch):
    delays = []
    monkeypatch.setattr(SCAN.time, 'sleep', delays.append)
    error = RuntimeError('429 Too Many Requests: Retry after 210 seconds')
    error.response = SimpleNamespace(status_code=429, headers={})
    calls = []

    def request():
        calls.append(True)
        if len(calls) == 1:
            raise error
        return 'ok'

    assert SCAN.retry(request) == 'ok'
    assert delays == [212]


def test_sharded_checkpoint_counts_every_shard():
    result = assess([file('model.safetensors.index.json', 100),
                     file('model-00001-of-00002.safetensors', 100),
                     file('model-00002-of-00002.safetensors', 200)])
    assert result['status'] == 'eligible' and result['safetensors_total_bytes'] == 300


def test_size_prefilter_uses_stored_dtypes_and_ignores_unknown_types():
    info = SimpleNamespace(safetensors=SimpleNamespace(parameters={'F16': 300_000_000, 'I8': 10,
                                                                  'unknown': 1_000_000_000}))
    assert SCAN.minimum_weight_bytes(info) == 600_000_010


@pytest.mark.parametrize('has_config', [True, False])
def test_scan_uses_pinned_hub_metadata_and_downloads_only_json(tmp_path, monkeypatch, has_config):
    import huggingface_hub

    candidate = SimpleNamespace(id='test/bert', sha='a' * 40, gated=False, private=False,
                                safetensors=None, downloads=1)
    files = [file('model.safetensors', 100)]
    if has_config:
        files.append(file('config.json', 100))
    info = SimpleNamespace(siblings=files, pipeline_tag='fill-mask')
    calls = []

    class Api:
        def __init__(self, token):
            assert token is False

        def list_models(self, **kwargs):
            assert kwargs['filter'] == ('bert', 'safetensors')
            return [candidate]

        def model_info(self, repo, **kwargs):
            assert repo == candidate.id and kwargs['revision'] == candidate.sha
            assert kwargs['files_metadata']
            return info

    def download(repo, filename, **kwargs):
        calls.append(filename)
        assert filename == 'config.json' and kwargs['revision'] == candidate.sha
        path = tmp_path / filename
        path.write_text('{"model_type":"bert","architectures":["BertForMaskedLM"]}')
        return str(path)

    monkeypatch.setattr(huggingface_hub, 'HfApi', Api)
    monkeypatch.setattr(huggingface_hub, 'hf_hub_download', download)
    args = SimpleNamespace(cache=tmp_path / 'cache', refresh=False, candidates=100)
    row = SCAN.scan_architecture('bert', 'BertConfig', args)
    if not has_config:
        assert row['status'] == 'no-qualifying-checkpoint'
        assert row['checked'][0]['status'] == 'missing-config'
        assert calls == []
        return
    assert row['status'] == 'eligible' and row['checkpoint']['revision'] == candidate.sha
    assert calls == ['config.json']


def test_catalogue_groups_by_task_and_architecture_and_preserves_gaps():
    checkpoint = {'repo': 'test/bert', 'type': 'fill-mask', 'model_classes': ['BertForMaskedLM'],
                  'safetensors_total_bytes': 100, 'weights_url': 'https://huggingface.co/test/bert'}
    rows = {'bert': {'status': 'eligible', 'checkpoint': checkpoint, 'config_class': 'BertConfig', 'checked': []},
            'big': {'status': 'search-limit', 'config_class': 'BigConfig', 'checked': []}}
    document = SCAN.catalogue('5.18.0', {'bert': 'BertConfig', 'big': 'BigConfig'}, rows, 100)
    assert document['types']['fill-mask']['bert'] == checkpoint
    assert document['summary'] == {'eligible': 1, 'search-limit': 1}
    assert document['architectures']['big']['status'] == 'search-limit'
    assert 'not proof' in SCAN.render(document)
