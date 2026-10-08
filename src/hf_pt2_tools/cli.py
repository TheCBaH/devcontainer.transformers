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
    config = json.loads((root / 'configs' / args.population / (entry.get('config_model_id', entry['id']) + '.json')).read_text())
    fixture_key = 'processor_fixture' if args.population == 'tiny' else 'reference_processor_fixture'
    fixture = json.loads((root / entry[fixture_key]).read_text()) if entry.get(fixture_key) else None
    return digest({'entry': entry, 'config': config, 'producer': producer(root),
                   'population': args.population, 'dtype': args.dtype, 'shape': args.shape,
                   'policy': getattr(args, 'policy', 'dynamo'), 'fixture': fixture,
                   **({'weights': 'checkpoint'} if getattr(args, 'weights', 'random') == 'checkpoint' else {})})


def check_outcomes(rows, exclusions):
    failures = {(row['artifact_id'], stage) for row in rows.values()
                for stage, outcome in row['stages'].items() if outcome['status'] == 'failed'}
    for row in rows.values():
        if row['status'] in ('timeout', 'crashed'):
            failures.add((row['artifact_id'], 'worker'))
    by_id = {row['artifact_id']: row for row in rows.values()}
    matched, stale = set(), set()
    for exclusion in exclusions:
        required = {'artifact_id', 'stage', 'policy', 'versions', 'reason'}
        if not required <= exclusion.keys() or not exclusion['versions'] or not exclusion['reason']:
            raise ValueError('exclusion requires artifact, stage, policy, versions and reason')
        key = (exclusion['artifact_id'], exclusion['stage'])
        if key in matched or key in stale:
            raise ValueError('duplicate exclusion')
        if key[0] not in by_id:
            continue
        row = by_id[key[0]]
        versions = {**row['producer']['versions'], 'core_revision': row['producer']['core_revision']}
        scoped = row['policy'] == exclusion['policy'] and all(versions.get(k) == v for k, v in exclusion['versions'].items())
        (matched if key in failures and scoped else stale).add(key)
    def records(keys):
        return [{'artifact_id': identity, 'stage': stage} for identity, stage in sorted(keys)]
    return {'unexpected_failures': records(failures - matched),
            'matched_exclusions': records(matched), 'stale_exclusions': records(stale)}


def sweep(args):
    root = Path(args.root).resolve()
    output = Path(args.output or root).resolve()
    manifest = read_manifest(root)
    entries = [e for e in manifest['models'] if (root / 'configs' / args.population / (e.get('config_model_id', e['id']) + '.json')).exists()]
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
    checkpoint = args.weights == 'checkpoint'
    if checkpoint and args.population != 'reference':
        raise ValueError('checkpoint weights apply to the original-config (reference) population')
    snapshots = {}
    if checkpoint:
        from .checkpoints import fetch
        snapshots = {name: fetch(root, name) for name in sorted(entries)}
    result_path = output / 'results' / ('checkpoint.json' if checkpoint else
                                        'models.json' if args.population == 'tiny' else 'reference.json')
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
                '--population', args.population, '--dtype', args.dtype, '--shape', args.shape, '--policy', args.policy]
        if name in snapshots:
            argv += ['--snapshot', snapshots[name]]
        row = run_worker(script, argv, name, args.timeout, hf_home=root / '.hf-cache')
        if row['status'] in ('timeout', 'crashed'):
            from .exporting import STAGES, producer
            row = {'name': name, 'status': row['status'], 'error_category': row['status'],
                   'category': entry['category'], 'artifact_id': artifact_id(entry, args.population, args.dtype, args.policy, args.shape,
                                            entry['reference']['revision'] if checkpoint else None),
                   'population': args.population, 'dtype': args.dtype, 'policy': args.policy, 'shape_policy': args.shape,
                   'stages': {stage: {'status': 'not_run'} for stage in STAGES},
                   'ops': {}, 'schemas': {}, 'producer': producer(root)}
        row['source_key'] = key
        rows[name] = row
        return row

    run_pool(sorted(entries), work, args.workers, lambda row: ' ' + row.get('failed_stage', ''))
    exclusions = yaml.safe_load((root / 'export-exclusions.yaml').read_text())['exclusions']
    outcomes = check_outcomes(rows, exclusions)
    document = {'schema_version': 1, 'population': args.population, 'weights': args.weights, 'attempted': len(rows),
                'verified': sum(r['status'] == 'ok' for r in rows.values()), 'models': dict(sorted(rows.items())),
                'outcomes': outcomes}
    validate_document(document, 'results', str(root / 'schemas'))
    write_json(result_path, document)
    if args.command == 'report':
        from .reporting import render
        render(output, document)
    return int(bool(outcomes['unexpected_failures'] or outcomes['stale_exclusions']))


def main():
    parser = argparse.ArgumentParser(description='Offline Transformers PT2 architecture research')
    parser.add_argument('command', choices=['smoke', 'report', 'models', 'worker', 'select', 'verify', 'research',
                                          'fetch', 'bind', 'generation', 'generation-worker', 'encoders', 'encoders-worker', 'assets',
                                          'catalogue', 'bundle', 'bundle-verify', 'pack', 'index'])
    parser.add_argument('--root', default='.')
    parser.add_argument('--output')
    parser.add_argument('--subset')
    parser.add_argument('--population', choices=['tiny', 'reference'], default='tiny')
    parser.add_argument('--dtype', choices=['fp32', 'fp16', 'bf16'], default='fp32')
    parser.add_argument('--shape', choices=['static', 'dynamic'], default='static')
    parser.add_argument('--policy', choices=['dynamo', 'direct', 'autocast'], default='dynamo')
    parser.add_argument('--workers', type=int, default=1)
    parser.add_argument('--timeout', type=int, default=900)
    parser.add_argument('--resume', action='store_true')
    parser.add_argument('--graph')
    parser.add_argument('--weights', choices=['random', 'checkpoint'], default='random')
    parser.add_argument('--snapshot')
    parser.add_argument('--static-history')
    parser.add_argument('--allow-unpinned-snapshot', action='store_true')
    parser.add_argument('--program')
    parser.add_argument('--binding')
    parser.add_argument('--source')
    parser.add_argument('--pack-repo')
    parser.add_argument('--pack-revision')
    parser.add_argument('--pack-url')
    parser.add_argument('--artifact')
    parser.add_argument('--pack-tag')
    parser.add_argument('--packs')
    args = parser.parse_args()
    if args.workers < 1 or args.timeout < 1:
        parser.error('workers and timeout must be positive')
    root = Path(args.root).resolve()
    if args.command in ('worker', 'generation-worker', 'encoders-worker'):
        def offline(event, arguments):
            if event == 'socket.connect':
                raise RuntimeError('random-weight workers forbid network access')
        sys.addaudithook(offline)
        if args.command == 'encoders-worker':
            from .encoders import run
            print(json.dumps(run(root, Path(args.output).resolve(), args.subset or 'tinyclip', args.population,
                                 args.snapshot, args.allow_unpinned_snapshot)))
            return
        if args.command == 'generation-worker':
            from .generation import run
            histories = tuple(int(h) for h in args.static_history.split(',')) if args.static_history else ()
            print(json.dumps(run(root, Path(args.output).resolve(), args.subset or 'smollm2-135m', args.population,
                                 args.snapshot, args.allow_unpinned_snapshot, histories)))
            return
        from .exporting import run
        print(json.dumps(run(root, args.subset, Path(args.output).resolve(), args.population,
                             args.dtype, args.policy, args.shape, args.snapshot, args.allow_unpinned_snapshot)))
        return
    if args.command == 'generation':
        if args.subset and args.subset not in ('smollm2-135m', 't5-small', 'whisper-tiny', 'smolvlm-256m'):
            parser.error('generation requires a reviewed decoder or encoder-decoder recipe')
        output = Path(args.output or root / '.build/generation').resolve()
        name = args.subset or 'smollm2-135m'
        argv = ['generation-worker', '--root', root, '--output', output, '--subset', name,
                '--population', args.population]
        if args.static_history:
            argv += ['--static-history', args.static_history]
        if args.weights == 'checkpoint':
            from .checkpoints import fetch
            argv += ['--snapshot', fetch(root, name)]
        result = run_worker(root / 'scripts/worker.py', argv, 'generation-llama', args.timeout, hf_home=root / '.hf-cache')
        print(json.dumps(result))
        sys.exit(0 if result['status'] == 'verified' else 1)
    if args.command == 'assets':
        from .assets import build_assets
        document = build_assets(root, Path(args.output or root / 'task-assets.json'),
                                set(args.subset.split(',')) if args.subset else None)
        failed = [(row['model_id'], kind) for row in document['models'] for kind, example in row['example'].items()
                  if example.get('status') == 'failed']
        print(f"described {len(document['models'])} models; failed examples: {failed}")
        sys.exit(1 if failed else 0)
    if args.command == 'encoders':
        from .encoders import MODELS
        if args.subset and args.subset not in MODELS:
            parser.error(f'encoders requires a reviewed tower split: {MODELS}')
        output = Path(args.output or root / '.build/components').resolve()
        name = args.subset or MODELS[0]
        argv = ['encoders-worker', '--root', root, '--output', output, '--subset', name, '--population', args.population]
        if args.weights == 'checkpoint':
            from .checkpoints import fetch
            argv += ['--snapshot', fetch(root, name)]
        result = run_worker(root / 'scripts/worker.py', argv, 'encoders-' + name, args.timeout, hf_home=root / '.hf-cache')
        print(json.dumps(result))
        sys.exit(0 if result['status'] == 'verified' else 1)
    if args.command == 'catalogue':
        from .fixtures import catalogue
        print(f"catalogued {len(catalogue(root)['artifacts'])} artifacts")
        return
    if args.command == 'pack':
        from .checkpoints import fetch
        from .weights import build_pack, check_pack
        if not args.subset or not args.program:
            parser.error('pack requires --subset model ID and --program original-config model.pt2')
        binding = json.loads(Path(args.binding or root / 'checkpoint-maps' / (args.subset + '.json')).read_text())
        from .fixtures import flat_name
        output = Path(args.output or root / '.build/packs').resolve() / ((flat_name(args.artifact) if args.artifact else args.subset) + '.safetensors')
        document = build_pack(binding, fetch(root, args.subset), Path(args.program).resolve(), output,
                              {'repo_id': args.pack_repo, 'revision': args.pack_revision, 'url': args.pack_url},
                              Path(args.graph).resolve() if args.graph else None)
        check_pack(document, output, binding['captures'])
        print(f"{args.subset}: packed {len(document['tensors'])} captures, sha256 {document['source']['sha256']}")
        return
    if args.command == 'index':
        from .fixtures import publication_index
        if not args.pack_repo or not args.pack_tag:
            parser.error('index requires --pack-repo and --pack-tag')
        document = publication_index(Path(args.output or root / '.build/bundles').resolve(), args.pack_repo, args.pack_tag)
        print(f"indexed {len(document['artifacts'])} bundles under release {args.pack_tag}")
        return
    if args.command in ('bundle', 'bundle-verify'):
        from .fixtures import build_bundle, verify_bundle
        output = Path(args.output or root / '.build/bundles').resolve()
        if args.command == 'bundle-verify':
            archives = sorted(output.glob('*.tar.gz'))
            if not archives:
                parser.error(f'no bundles in {output}')
            for archive in archives:
                print(archive.name, verify_bundle(root, archive))
            return
        names = set(args.subset.split(',')) if args.subset else None
        count = 0
        source = Path(args.source).resolve() if args.source else root
        for contract in sorted((source / 'models').rglob('contract.json')):
            directory = contract.parent
            identity = str(directory.relative_to(source / 'models'))
            if names and identity.split('/')[0] not in names:
                continue
            build_bundle(root, directory, source / '.build' / identity, output, args.packs)
            count += 1
        print(f'bundled {count} artifacts into {output}')
        return
    if args.command in ('fetch', 'bind'):
        from .checkpoints import bind, fetch
        if not args.subset or ',' in args.subset:
            parser.error('fetch/bind require exactly one explicit --subset model ID')
        if args.command == 'fetch':
            print(fetch(root, args.subset))
        else:
            if not args.graph:
                parser.error('bind requires --graph original-config model JSON')
            result = bind(root, args.subset, Path(args.graph).resolve(),
                          Path(args.output or root / 'checkpoint-maps' / (args.subset + '.json')))
            print(f"{args.subset}: {result['status']}")
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
    contracts = sorted((root / 'models').rglob('contract.json'))
    for path in contracts:
        identity = str(path.parent.relative_to(root / 'models'))
        verify_artifact(root, path.parent, identity)
    print(f'verified {len(contracts)} artifact contracts and operator facts')
