#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
import subprocess

from task_fixtures.integrity import build_index, check_request, digest, read_json, verify_bundle, verify_index


def main():
    parser = argparse.ArgumentParser(description='Generate producer references or verify data-only task releases')
    parser.add_argument('command', choices=('plan', 'generate', 'index', 'verify', 'verify-bundle'))
    parser.add_argument('--root', default='.')
    parser.add_argument('--request', default='task-fixture-request.json')
    parser.add_argument('--recipe')
    parser.add_argument('--output', default='.build/task-fixtures')
    parser.add_argument('--repository')
    parser.add_argument('--tag')
    parser.add_argument('--manifest')
    parser.add_argument('--index-pin')
    parser.add_argument('--tensors', action='store_true')
    args = parser.parse_args()
    if args.command in ('plan', 'generate', 'index'):
        request = read_json(args.request)
        check_request(request, read_json(Path(args.root) / 'task-recipes.json'))
    if args.command == 'plan':
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
        rows = [{'recipe': task['recipe_id']} for task in request['tasks']]
        import json
        outputs = {'recipes': json.dumps(rows, separators=(',', ':')),
                   'fixture_tag': f'task-fixtures-{commit[:12]}-{digest(request)[:12]}',
                   'publish': str(request['publish']).lower()}
        with open(os.environ['GITHUB_OUTPUT'], 'a') as stream:
            for key, value in outputs.items():
                stream.write(f'{key}={value}\n')
    elif args.command == 'generate':
        if not args.recipe:
            parser.error('generate requires an explicit --recipe')
        from task_fixtures.generate import generate
        generate(Path(args.root).resolve(), args.request, args.recipe, args.output)
    elif args.command == 'index':
        if not args.repository or not args.tag:
            parser.error('index requires --repository and --tag')
        build_index(args.output, args.repository, args.tag, request)
    elif args.command == 'verify':
        if not args.index_pin:
            parser.error('verify requires --index-pin from a trusted consumer manifest')
        document = verify_index(Path(args.output) / 'task-fixtures.json', read_json(args.index_pin), args.output, args.tensors)
        print(f"verified {len(document['fixtures'])} task bundles")
    else:
        if not args.manifest:
            parser.error('verify-bundle requires --manifest')
        verify_bundle(args.manifest, args.output, tensors=args.tensors)


if __name__ == '__main__':
    main()
