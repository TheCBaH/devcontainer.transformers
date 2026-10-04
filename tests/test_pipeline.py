import argparse
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
