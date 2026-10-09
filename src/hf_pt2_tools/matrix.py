"""Per-artifact checkpoint matrix: export, bind, pack, offline replay, kept apart from consumer admission."""
import json
from pathlib import Path

from .artifacts import write_json
from .fixtures import flat_name, verify_bundle
from .registry import read_manifest

BASE_MODELS = ('bert-tiny', 'smollm2-135m', 't5-small', 'mobilevit-xxs', 'whisper-tiny', 'tinyclip', 'videomae-small',
               'time-series-small', 'yolos-tiny', 'segformer-b0', 'depth-anything-small', 'wav2vec2-base', 'smolvlm-256m')
NOT_MEASURED = 'not measured: needs the consumer (mltorch) admission run'


def _load(path):
    return json.loads(Path(path).read_text()) if Path(path).exists() else None


def _row(model, identity, component, export, source, bundles, maps, replay):
    stem = flat_name(identity) if identity else None
    binding = _load(maps / (stem + '.json')) if stem else None
    manifest = _load(bundles / (stem + '.manifest.json')) if stem else None
    row = {'model': model, 'component': component, 'artifact_id': identity, 'export': export,
           'bind': (binding or {}).get('status', 'not run'),
           'unmapped_captures': len((binding or {}).get('unmapped', [])) if binding else None,
           'pack': 'ok' if manifest and 'pack' in manifest else 'not run',
           'offline_replay': 'not run', 'consumer_admission': NOT_MEASURED,
           'weights': (manifest or {}).get('weight_source', {}).get('kind')}
    if manifest and replay:
        archive = bundles / manifest['archive']['name']
        try:
            row['offline_replay'] = verify_bundle(replay, archive)['status']
        except Exception as error:  # a failed replay is a result, not a crash
            row['offline_replay'] = f'failed: {type(error).__name__}'
    return row


def build_matrix(root, source, output, replay=True):
    """Join result files of one checkpoint run (forward, generation, encoders) with its maps and bundles."""
    source, root = Path(source), Path(root)
    bundles, maps = source / 'bundles', source / 'maps'
    entries = {e['id']: e for e in read_manifest(root)['models']}
    rows = []
    forward = (_load(source / 'results/checkpoint.json') or {}).get('models', {})
    for model in BASE_MODELS:
        reference = entries[model]['reference']
        if not reference['safetensors_files']:
            rows.append({'model': model, 'component': 'forward', 'artifact_id': None, 'export': 'unavailable',
                         'bind': 'unavailable', 'unmapped_captures': None, 'pack': 'unavailable',
                         'offline_replay': 'unavailable', 'consumer_admission': NOT_MEASURED, 'weights': None,
                         'note': 'no upstream safetensors at the pinned revision'})
            continue
        result = forward.get(model)
        if result:
            row = _row(model, result['artifact_id'], 'forward', result['status'], source, bundles, maps, root if replay else None)
            if 'conversion' in reference:
                row['note'] = 'weights converted from ' + reference['conversion']['source']
            rows.append(row)
        else:
            rows.append({'model': model, 'component': 'forward', 'artifact_id': None, 'export': 'not run', 'bind': 'not run',
                         'unmapped_captures': None, 'pack': 'not run', 'offline_replay': 'not run',
                         'consumer_admission': NOT_MEASURED, 'weights': None})
    for folder, key in ((Path(str(source) + '-generation'), 'generation'), (Path(str(source) + '-components'), 'encoders')):
        for path in sorted((folder / 'results' / key).glob('*-reference-checkpoint.json')) if (folder / 'results' / key).exists() else ():
            result = json.loads(path.read_text())
            components = dict(result['components'])
            for history, variant in (result.get('static_variants') or {}).items():
                components[f'decode-static-h{history}'] = variant
            for component, info in sorted(components.items()):
                rows.append(_row(result['model_id'], info['artifact_id'], component, info['status'], source, bundles, maps,
                                 root if replay else None))
    document = {'schema_version': 1, 'scope': 'producer-side status; operator coverage and producer success are not '
                'consumer inference', 'rows': rows}
    write_json(Path(output).with_suffix('.json'), document)
    lines = ['# Checkpoint matrix', '', document['scope'] + '.', '',
             '| model | component | export | bind | pack | offline replay | consumer admission |', '|---|---|---|---|---|---|---|']
    for r in rows:
        lines.append(f"| {r['model']} | {r['component']} | {r['export']} | {r['bind']} | {r['pack']} | {r['offline_replay']} | "
                     f"{'not measured' if r['consumer_admission'] == NOT_MEASURED else r['consumer_admission']} |")
    notes = [f"- {r['model']}: {r['note']}" for r in rows if r.get('note')]
    Path(output).write_text('\n'.join(lines + ([''] + notes if notes else []) + ['']))
    return document
