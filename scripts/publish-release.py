#!/usr/bin/env python3
"""Upload once, verify every draft byte, then make the completed release public."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile


def gh(*args):
    return subprocess.check_output(['gh', *map(str, args)], text=True)


def pin(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 ** 2), b''):
            h.update(block)
    return {'sha256': h.hexdigest(), 'size': path.stat().st_size}


def publish(directory, repository, tag, commit, index_name):
    directory = Path(directory)
    index = json.loads((directory / index_name).read_text())
    rows = index.get('fixtures', index.get('artifacts', []))
    pins = {}
    for row in rows:
        for asset in row['assets'].values():
            name = asset['name']
            if asset['url'] != f'https://github.com/{repository}/releases/download/{tag}/{name}':
                raise ValueError('asset URL differs from the new release identity')
            expected = {key: asset[key] for key in ('sha256', 'size')}
            if name in pins and pins[name] != expected:
                raise ValueError('two artifacts disagree on an asset pin')
            pins[name] = expected
    files = sorted(path for path in directory.iterdir() if path.is_file())
    if not rows or any(pin(directory / name) != expected for name, expected in pins.items()):
        raise ValueError('incomplete or corrupt release inputs')
    try:
        release = json.loads(gh('release', 'view', tag, '--repo', repository, '--json', 'isDraft,targetCommitish'))
    except subprocess.CalledProcessError:
        release = None
    if release is not None:
        raise ValueError('release identity already exists; published and draft assets are immutable, use a new request/commit')
    gh('release', 'create', tag, '--repo', repository, '--target', commit, '--draft', '--prerelease',
       '--title', f'Producer fixtures {tag}', '--notes',
       f'Generator commit {commit}. See {index_name} for immutable payload pins and independent reference provenance.')
    gh('release', 'upload', tag, '--repo', repository, *files)
    with tempfile.TemporaryDirectory() as scratch:
        gh('release', 'download', tag, '--repo', repository, '--dir', scratch)
        fresh = Path(scratch)
        if {path.name for path in fresh.iterdir()} != {path.name for path in files}:
            raise ValueError('draft release inventory differs from staged files')
        for path in files:
            if pin(fresh / path.name) != pin(path):
                raise ValueError(f'draft release download mismatch: {path.name}')
    gh('release', 'edit', tag, '--repo', repository, '--draft=false', '--prerelease')
    print(f'Published {tag}: {len(files)} assets verified before publication')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', required=True)
    parser.add_argument('--repository', required=True)
    parser.add_argument('--tag', required=True)
    parser.add_argument('--commit', required=True)
    parser.add_argument('--index', default='publication.json')
    args = parser.parse_args()
    publish(args.directory, args.repository, args.tag, args.commit, args.index)
