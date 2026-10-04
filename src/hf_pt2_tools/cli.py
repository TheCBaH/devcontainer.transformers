import argparse
import json
from pathlib import Path
import sys

import yaml
from pt2_export_core.harness import run_pool, run_worker
from pt2_export_core.schema_validate import validate_document

from .artifacts import verify_artifact, write_json
from .registry import artifact_id, digest, read_manifest


def source_key(root, entry, args):
    from .exporting import producer
    config = json.loads((root / 'configs' / args.population / (entry['id'] + '.json')).read_text())
    fixture = json.loads((root / entry['processor_fixture']).read_text()) if entry.get('processor_fixture') else None
    return digest({'entry': entry, 'config': config, 'producer': producer(root),
                   'population': args.population, 'dtype': args.dtype, 'shape': args.shape, 'fixture': fixture})


def sweep(args):
    root = Path(args.root).resolve()
    output = Path(args.output or root).resolve()
    manifest = read_manifest(root)
    entries = [e for e in manifest['models'] if (root / 'configs' / args.population / (e['id'] + '.json')).exists()]
    if args.subset:
        requested = args.subset.split(',')
        unknown = set(requested) - {e['id'] for e in entries}
        if unknown:
            raise ValueError(f'unknown subset: {sorted(unknown)}')
        entries = [e for e in entries if e['id'] in requested]
    else:
        entries = [e for e in entries if e['tier'] == 'core']
    if not entries:
        raise ValueError('no reviewed candidates')
    entries = {e['id']: e for e in entries}
    result_path = output / 'results' / ('models.json' if args.population == 'tiny' else 'reference.json')
    previous = json.loads(result_path.read_text())['models'] if args.resume and result_path.exists() else {}
    rows = {}

    def work(name):
        entry = entries[name]
        key = source_key(root, entry, args)
        if name in previous and previous[name]['status'] == 'ok' and previous[name].get('source_key') == key:
            verify_artifact(root, output / 'models' / previous[name]['artifact_id'])
            rows[name] = previous[name]
            return rows[name]
        script = root / 'scripts/worker.py'
        argv = ['worker', '--root', root, '--output', output, '--subset', name,
                '--population', args.population, '--dtype', args.dtype, '--shape', args.shape]
        row = run_worker(script, argv, name, args.timeout, hf_home=root / '.hf-cache')
        if row['status'] in ('timeout', 'crashed'):
            from .exporting import STAGES, producer
            row = {'name': name, 'status': row['status'], 'error_category': row['status'],
                   'category': entry['category'], 'artifact_id': artifact_id(entry, args.population, args.dtype, shape=args.shape),
                   'population': args.population, 'stages': {stage: {'status': 'not_run'} for stage in STAGES},
                   'ops': {}, 'schemas': {}, 'producer': producer(root)}
        row['source_key'] = key
        rows[name] = row
        return row

    failures = run_pool(sorted(entries), work, args.workers, lambda row: ' ' + row.get('failed_stage', ''))
    document = {'schema_version': 1, 'population': args.population, 'attempted': len(rows),
                'verified': sum(r['status'] == 'ok' for r in rows.values()), 'models': dict(sorted(rows.items()))}
    validate_document(document, 'results', str(root / 'schemas'))
    write_json(result_path, document)
    if args.command == 'report':
        from .reporting import render
        render(output, document)
    return 1 if failures else 0


def main():
    parser = argparse.ArgumentParser(description='Offline Transformers PT2 architecture research')
    parser.add_argument('command', choices=['smoke', 'report', 'models', 'worker', 'select', 'verify', 'research'])
    parser.add_argument('--root', default='.')
    parser.add_argument('--output')
    parser.add_argument('--subset')
    parser.add_argument('--population', choices=['tiny', 'reference'], default='tiny')
    parser.add_argument('--dtype', choices=['fp32', 'fp16', 'bf16'], default='fp32')
    parser.add_argument('--shape', choices=['static', 'dynamic'], default='static')
    parser.add_argument('--workers', type=int, default=1)
    parser.add_argument('--timeout', type=int, default=900)
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    if args.workers < 1 or args.timeout < 1:
        parser.error('workers and timeout must be positive')
    root = Path(args.root).resolve()
    if args.command == 'worker':
        def offline(event, arguments):
            if event == 'socket.connect':
                raise RuntimeError('random-weight workers forbid network access')
        sys.addaudithook(offline)
        from .exporting import run
        print(json.dumps(run(root, args.subset, Path(args.output).resolve(), args.population, args.dtype, shape=args.shape)))
        return
    if args.command == 'smoke':
        args.subset = 'bert-tiny'
        args.output = str(root / '.build/smoke')
        sys.exit(sweep(args))
    if args.command in ('report', 'models', 'research'):
        sys.exit(sweep(args))
    if args.command == 'select':
        from .reporting import selection
        selection(root, json.loads((root / 'results/models.json').read_text()))
        return
    selected = yaml.safe_load((root / 'models-selected.yaml').read_text())
    for entry in selected['models'].values():
        verify_artifact(root, root / 'models' / entry['artifact_id'], entry['artifact_id'])
    print(f"verified {len(selected['models'])} artifact contracts and operator facts")
