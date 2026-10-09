import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile

import torch

from .artifacts import file_hash, verify_artifact, write_json
from .registry import RANDOM_WEIGHTS

CASE_FILES = ('inputs.pt', 'outputs.pt')


def tensor_digest(named):
    digest = hashlib.sha256()
    for name, tensor in named.items():
        flat = tensor.detach().cpu().contiguous().reshape(-1)
        digest.update(json.dumps([name, str(tensor.dtype), list(tensor.shape)]).encode() + b'\n')
        digest.update(flat.view(torch.uint8).numpy().tobytes())
    return digest.hexdigest()


def write_cases(directory, output_names, cases):
    """Write flat dict[str, Tensor] case files; names keep call and output order."""
    entries = []
    for index, case in enumerate(cases):
        case_id = f'case-{index:02d}'
        inputs = {name: tensor.detach().cpu().contiguous() for name, tensor in case['inputs'].items()}
        outputs = {name: tensor.detach().cpu().contiguous()
                   for name, tensor in zip(output_names, case['outputs'], strict=True)}
        folder = Path(directory) / 'cases' / case_id
        folder.mkdir(parents=True, exist_ok=True)
        torch.save(inputs, folder / 'inputs.pt')
        torch.save(outputs, folder / 'outputs.pt')
        entries.append({'id': case_id, 'inputs': list(inputs), 'outputs': list(outputs),
                        'inputs_sha256': tensor_digest(inputs), 'outputs_sha256': tensor_digest(outputs)})
    return entries


def cases_document(identity, entries, tolerances, weight_source=None):
    return {'schema_version': 1, 'artifact_id': identity, 'weight_source': weight_source or dict(RANDOM_WEIGHTS),
            'tolerances': {'atol': tolerances[0], 'rtol': tolerances[1]}, 'cases': entries}


def check_cases_document(document, contract):
    """Structural check of a published cases.json against its contract."""
    if document.get('schema_version') != 1 or document.get('artifact_id') != contract['artifact_id']:
        raise ValueError('cases manifest identity mismatch')
    cases = document['cases']
    if len(cases) != contract['verified_cases'] or not cases:
        raise ValueError('cases manifest count differs from contract')
    inputs = [tensor['name'] for tensor in contract['inputs']]
    outputs = [tensor['name'] for tensor in contract['outputs']]
    if document['weight_source'] != contract.get('weights'):
        raise ValueError('cases manifest weight source differs from contract')
    if document['tolerances'] != contract['tolerances']:
        raise ValueError('cases manifest tolerances differ from contract')
    for index, case in enumerate(cases):
        if case['id'] != f'case-{index:02d}' or case['inputs'] != inputs or case['outputs'] != outputs:
            raise ValueError('cases manifest names differ from contract call order')
        for key in ('inputs_sha256', 'outputs_sha256'):
            if len(case[key]) != 64:
                raise ValueError('malformed case digest')


def verify_case_files(directory, document):
    """Reload case tensors (weights_only) and recompare their content digests."""
    for case in document['cases']:
        folder = Path(directory) / 'cases' / case['id']
        for name, names, key in (('inputs.pt', case['inputs'], 'inputs_sha256'),
                                 ('outputs.pt', case['outputs'], 'outputs_sha256')):
            tensors = torch.load(folder / name, weights_only=True)
            if not isinstance(tensors, dict) or list(tensors) != names:
                raise ValueError(f'case {case["id"]} {name} names differ from manifest')
            if tensor_digest(tensors) != case[key]:
                raise ValueError(f'case {case["id"]} {name} content digest mismatch')


def _members(artifact, work, loader_map=None, map_v2=None, slim=False):
    """Deterministic archive layout: published artifact files, model.pt2, case tensors, loader maps."""
    members = {str(p.relative_to(artifact)): p for p in sorted(artifact.rglob('*')) if p.is_file()}
    if not slim:
        members['model.pt2'] = work / 'model.pt2'
    if loader_map:
        members['models/safetensors.json'] = loader_map
    if map_v2:
        members['models/safetensors.v2.json'] = map_v2
    for p in sorted((work / 'cases').rglob('*.pt')):
        members[str(p.relative_to(work))] = p
    return dict(sorted(members.items()))


def flat_name(identity):
    return identity.replace('/', '--')


def _find_pack(contract, document, packs):
    """Derived (map, pack) for an artifact from `pack --artifact` outputs; checkpoint-backed ones must have it."""
    stem = flat_name(contract['artifact_id'])
    loader_map, pack = (Path(packs) / (stem + suffix) for suffix in ('.map.json', '.safetensors')) if packs else (None, None)
    present = [path for path in (loader_map, pack) if path and path.exists()]
    if len(present) == 1:
        raise ValueError(f'incomplete derived pack for {stem}: need both map and safetensors')
    if not present:
        if packs and document['weight_source']['kind'] == 'checkpoint':
            raise ValueError(f'no derived pack for checkpoint-backed artifact {stem}')
        return None, None
    return loader_map, pack


def _check_pack_files(map_path, pack, captures):
    from .weights import check_pack
    document = json.loads(Path(map_path).read_text())
    if document['source']['filename'] != Path(pack).name:
        raise ValueError('map source filename differs from the pack file name')
    check_pack(document, pack, captures['captures'])


def _v2_assets(map_path):
    """Release-hosted files a v2 map names (graph-owned pack, converted checkpoint), taken from `maps`."""
    document = json.loads(Path(map_path).read_text())
    sources = [*document['sources']['checkpoint']['files'], *([document['sources']['graph_owned']] if 'graph_owned' in document['sources'] else [])]
    return document, [source for source in sources if 'derived_from' in source or source is document['sources'].get('graph_owned')]


def build_bundle(root, artifact, work, output, packs=None, maps=None, slim=False):
    """Pack one verified artifact with its payload and case tensors into a reproducible tar.gz.

    With `packs`, a derived weight pack is checked against the artifact's captures, its map is bundled as
    `models/safetensors.json` (the loader layout) and the pack is copied beside the archive. With `maps`, the
    v2 map (docs/checkpoint-map-v2.md) is bundled as `models/safetensors.v2.json` and the files it hosts are
    copied beside the archive; `slim` then leaves out `model.pt2` and the full v1 pack.
    """
    artifact, work, output = Path(artifact), Path(work), Path(output)
    contract = verify_artifact(root, artifact)
    document = json.loads((artifact / 'cases.json').read_text())
    verify_case_files(work, document)
    captures = json.loads((artifact / 'captures.json').read_text())
    loader_map, pack = (None, None) if slim else _find_pack(contract, document, packs)
    if pack:
        _check_pack_files(loader_map, pack, captures)
    map_v2, hosted = None, []
    if maps:
        candidate = Path(maps) / (flat_name(contract['artifact_id']) + '.map.v2.json')
        if candidate.exists():
            from .mapv2 import check_structure
            map_v2 = candidate
            map_document, hosted = _v2_assets(map_v2)
            check_structure(map_document, captures['captures'], contract['artifact_id'], contract['graph_sha256'])
            for source in hosted:
                held = Path(maps) / source['name']
                if file_hash(held) != source['sha256'] or held.stat().st_size != source['size']:
                    raise ValueError(f"hosted file differs from the v2 map pin: {source['name']}")
        elif slim and document['weight_source']['kind'] == 'checkpoint':
            raise ValueError(f"no v2 map for checkpoint-backed artifact {contract['artifact_id']}")
    members = _members(artifact, work, loader_map, map_v2, slim)
    output.mkdir(parents=True, exist_ok=True)
    if pack:
        shutil.copyfile(pack, output / pack.name)
    for source in hosted:
        shutil.copyfile(Path(maps) / source['name'], output / source['name'])
    archive = output / (flat_name(contract['artifact_id']) + '.tar.gz')
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode='wb', mtime=0) as compressed:
        with tarfile.open(fileobj=compressed, mode='w', format=tarfile.PAX_FORMAT) as tar:
            for name, path in members.items():
                info = tarfile.TarInfo(name)
                info.size, info.mode, info.mtime = path.stat().st_size, 0o644, 0
                with path.open('rb') as handle:
                    tar.addfile(info, handle)
    archive.write_bytes(buffer.getvalue())
    commit = subprocess.run(['git', '-C', str(root), 'rev-parse', 'HEAD'],
                            capture_output=True, text=True).stdout.strip() or None
    manifest = {'schema_version': 1, 'artifact_id': contract['artifact_id'], 'producer_commit': commit,
                'graph_sha256': contract['graph_sha256'], 'contract_sha256': file_hash(artifact / 'contract.json'),
                'weight_source': document['weight_source'], 'payload': None if slim else 'model.pt2',
                'archive': {'name': archive.name, 'sha256': file_hash(archive), 'size': archive.stat().st_size},
                'members': {name: {'sha256': file_hash(path), 'size': path.stat().st_size}
                            for name, path in members.items()},
                'cases': [case['id'] for case in document['cases']]}
    if pack:
        source = json.loads(loader_map.read_text())['source']
        manifest['pack'] = {'name': pack.name, 'sha256': file_hash(pack), 'size': pack.stat().st_size,
                            'map': 'models/safetensors.json', 'url': source['url']}
    if map_v2:
        manifest['map_v2'] = {'member': 'models/safetensors.v2.json',
                              'assets': [{key: source[key] for key in ('name', 'sha256', 'size', 'url')} for source in hosted]}
    write_json(output / (flat_name(contract['artifact_id']) + '.manifest.json'), manifest)
    return manifest


def verify_bundle(root, archive, manifest_path=None):
    """Extract into an empty directory, check every hash, then run all cases with torch only."""
    archive = Path(archive)
    manifest = json.loads(Path(manifest_path or archive.with_name(archive.name.removesuffix('.tar.gz') + '.manifest.json')).read_text())
    if file_hash(archive) != manifest['archive']['sha256'] or archive.stat().st_size != manifest['archive']['size']:
        raise ValueError('archive digest/size mismatch')
    with tempfile.TemporaryDirectory() as scratch:
        target = Path(scratch)
        with tarfile.open(archive) as tar:
            names = tar.getnames()
            if sorted(names) != sorted(manifest['members']) or any(n.startswith(('/', '..')) or '/../' in n for n in names):
                raise ValueError('archive member list differs from manifest')
            tar.extractall(target, filter='data')
        for name, expected in manifest['members'].items():
            path = target / name
            if file_hash(path) != expected['sha256'] or path.stat().st_size != expected['size']:
                raise ValueError(f'member digest mismatch: {name}')
        contract = verify_artifact(root, target, manifest['artifact_id'])
        if file_hash(target / 'contract.json') != manifest['contract_sha256'] or contract['graph_sha256'] != manifest['graph_sha256']:
            raise ValueError('contract/graph digest differs from manifest')
        if 'pack' in manifest:
            pack = archive.with_name(manifest['pack']['name'])
            if not pack.exists() or file_hash(pack) != manifest['pack']['sha256'] or pack.stat().st_size != manifest['pack']['size']:
                raise ValueError('pack file missing or differs from the manifest')
            _check_pack_files(target / manifest['pack']['map'], pack,
                              json.loads((target / 'captures.json').read_text()))
        if 'map_v2' in manifest:
            from .mapv2 import check_structure
            for asset in manifest['map_v2']['assets']:
                held = archive.with_name(asset['name'])
                if not held.exists() or file_hash(held) != asset['sha256'] or held.stat().st_size != asset['size']:
                    raise ValueError(f"v2 hosted file missing or differs from the manifest: {asset['name']}")
            check_structure(json.loads((target / manifest['map_v2']['member']).read_text()),
                            json.loads((target / 'captures.json').read_text())['captures'],
                            manifest['artifact_id'], manifest['graph_sha256'])
        document = json.loads((target / 'cases.json').read_text())
        verify_case_files(target, document)
        if manifest['payload'] is None:
            return {'status': 'ok', 'cases': len(document['cases']), 'replay': 'not included (slim bundle)'}
        payload = target / 'examples.pt'
        torch.save({'cases': [{'inputs': torch.load(target / 'cases' / c['id'] / 'inputs.pt', weights_only=True),
                               'outputs': tuple(torch.load(target / 'cases' / c['id'] / 'outputs.pt', weights_only=True).values())}
                              for c in document['cases']],
                    'tolerances': (document['tolerances']['atol'], document['tolerances']['rtol'])}, payload)
        process = subprocess.run([sys.executable, str(Path(__file__).with_name('fresh_load.py')),
                                  str(target / manifest['payload']), str(payload)],
                                 capture_output=True, text=True, timeout=120,
                                 env={**os.environ, 'HF_HUB_OFFLINE': '1'})
        if process.returncode:
            raise RuntimeError('bundle cases failed torch-only replay: ' + process.stderr[-400:])
        return json.loads(process.stdout.strip().splitlines()[-1])


def catalogue(root):
    """Graph-only discovery index over every committed artifact; no weights needed."""
    root = Path(root)
    rows = []
    for path in sorted((root / 'models').rglob('contract.json')):
        directory = path.parent
        identity = str(directory.relative_to(root / 'models'))
        contract = verify_artifact(root, directory, identity)
        model, category, population, component, dtype, policy, shape, *revision = identity.split('/')
        document = json.loads((directory / 'cases.json').read_text())
        rows.append({'artifact_id': identity, 'model_id': model, 'category': category, 'population': population,
                     'component': component, 'dtype': dtype, 'policy': policy, 'shape_policy': shape,
                     'weights_revision': revision[0].removeprefix('ckpt-') if revision else None,
                     'path': str(directory.relative_to(root)), 'graph_sha256': contract['graph_sha256'],
                     'contract_sha256': file_hash(path), 'config_sha256': contract['config_sha256'],
                     'weight_source': document['weight_source'],
                     'cases': {'manifest_sha256': file_hash(directory / 'cases.json'),
                               'ids': [c['id'] for c in document['cases']]},
                     'inputs': [t['name'] for t in contract['inputs']],
                     'outputs': [t['name'] for t in contract['outputs']],
                     'files': {str(f.relative_to(directory)): {'sha256': file_hash(f), 'size': f.stat().st_size}
                               for f in sorted(directory.rglob('*')) if f.is_file()}})
    result = {'schema_version': 1, 'artifacts': rows}
    write_json(root / 'catalogue.json', result)
    return result


RELEASE_ASSET_LIMIT = 2 * 1024 ** 3


def publication_index(bundles, repository, tag):
    """Exact download locations and digests for every bundle, from the manifests alone.

    The release tag is the hosting revision; producer commit and upstream checkpoint revision are separate facts.
    """
    bundles = Path(bundles)
    base = f'https://github.com/{repository}/releases/download/{tag}/'
    rows = []
    for path in sorted(bundles.glob('*.manifest.json')):
        manifest = json.loads(path.read_text())
        assets = {'manifest': {'name': path.name, 'sha256': file_hash(path), 'size': path.stat().st_size},
                  'archive': dict(manifest['archive'])}
        pack = manifest.get('pack')
        if pack:
            if pack['url'] != base + pack['name']:
                raise ValueError(f"map location {pack['url']} differs from the release asset {base + pack['name']}")
            assets['pack'] = {key: pack[key] for key in ('name', 'sha256', 'size')}
        for asset in manifest.get('map_v2', {}).get('assets', []):
            if asset['url'] != base + asset['name']:
                raise ValueError(f"v2 map location {asset['url']} differs from the release asset {base + asset['name']}")
            assets['v2:' + asset['name']] = {key: asset[key] for key in ('name', 'sha256', 'size')}
        for asset in assets.values():
            if asset['size'] > RELEASE_ASSET_LIMIT:
                raise ValueError(f"{asset['name']} exceeds the release asset size limit")
            asset['url'] = base + asset['name']
        model, category, population, component, *_ = manifest['artifact_id'].split('/')
        rows.append({'artifact_id': manifest['artifact_id'], 'model_id': model, 'component': component,
                     'graph_sha256': manifest['graph_sha256'], 'producer_commit': manifest['producer_commit'],
                     'weight_source': manifest['weight_source'], 'assets': assets})
    if not rows:
        raise ValueError(f'no bundle manifests in {bundles}')
    document = {'schema_version': 1, 'repository': repository, 'release_tag': tag, 'artifacts': rows}
    write_json(bundles / 'publication.json', document)
    return document
