import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import tarfile
import tempfile
import urllib.request


MAX_BYTES = 768 * 1024 ** 2
SHA = re.compile(r'^[0-9a-f]{64}$')
COMMIT = re.compile(r'^[0-9a-f]{40}$')
SAFE = re.compile(r'^[a-zA-Z0-9_.-]+$')


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     ensure_ascii=True, allow_nan=False).encode()).hexdigest()


def file_pin(path):
    path = Path(path)
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 ** 2), b''):
            h.update(block)
    return {'sha256': h.hexdigest(), 'size': path.stat().st_size}


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n')


def read_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate JSON key')
            result[key] = value
        return result
    return json.loads(Path(path).read_text(), object_pairs_hook=pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def check_pin(pin):
    if not SHA.fullmatch(pin['sha256']) or type(pin['size']) is not int or not 0 <= pin['size'] <= MAX_BYTES:
        raise ValueError('invalid or oversized byte pin')


def check_request(request, recipes):
    if request['schema_version'] != 1 or not request['tasks'] or type(request['publish']) is not bool:
        raise ValueError('invalid task request')
    if not COMMIT.fullmatch(request['reference_producer']) or not SHA.fullmatch(request['lock_sha256']):
        raise ValueError('invalid request provenance')
    check_pin(request['reference_publication'])
    known = {task['recipe_id']: task for task in recipes['tasks']}
    seen = set()
    for task in request['tasks']:
        identity = task['recipe_id']
        if identity in seen or task != known.get(identity):
            raise ValueError('request must select unique, exact source recipes')
        seen.add(identity)
        if not SAFE.fullmatch(identity) or not task['expected_cases']:
            raise ValueError('unsafe or incomplete task recipe')


def verify_file(path, pin):
    check_pin(pin)
    if file_pin(path) != {key: pin[key] for key in ('sha256', 'size')}:
        raise ValueError(f'byte pin mismatch: {path}')


def download(pin, directory, name=None):
    check_pin(pin)
    name = name or pin['name']
    if not SAFE.fullmatch(name) or not pin['url'].startswith('https://'):
        raise ValueError('unsafe download name or URL')
    path = Path(directory) / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        verify_file(path, pin)
        return path
    temporary = path.with_suffix(path.suffix + '.partial')
    try:
        with urllib.request.urlopen(pin['url'], timeout=120) as source, temporary.open('wb') as target:
            count = 0
            while block := source.read(1024 ** 2):
                count += len(block)
                if count > pin['size']:
                    raise ValueError('download exceeds its declared size')
                target.write(block)
        verify_file(temporary, pin)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)
    return path


def extract(archive, directory, members):
    """Exact regular-file inventory, bounded before allocating or extracting."""
    total = 0
    for name, pin in members.items():
        path = PurePosixPath(name)
        if path.is_absolute() or '..' in path.parts or str(path) != name or '\\' in name:
            raise ValueError('unsafe member path')
        check_pin(pin)
        total += pin['size']
    if total > MAX_BYTES or len(members) > 4096:
        raise ValueError('bundle exceeds the extraction bound')
    seen = set()
    with tarfile.open(archive, 'r:gz') as tar:
        for info in tar:
            if info.name in seen or info.name not in members or not info.isfile():
                raise ValueError('unexpected, duplicate or non-file member')
            pin = members[info.name]
            if info.size != pin['size']:
                raise ValueError('member size differs from manifest')
            seen.add(info.name)
            path = Path(directory) / info.name
            path.parent.mkdir(parents=True, exist_ok=True)
            with tar.extractfile(info) as source, path.open('wb') as target:
                for block in iter(lambda: source.read(1024 ** 2), b''):
                    target.write(block)
            verify_file(path, pin)
    if seen != set(members):
        raise ValueError('incomplete bundle inventory')


def pack(directory, output, contract):
    directory, output = Path(directory), Path(output)
    write_json(directory / 'task-contract.json', contract)
    members = {str(path.relative_to(directory)): file_pin(path)
               for path in sorted(directory.rglob('*')) if path.is_file()}
    stem = contract['recipe_id'] + '--' + hashlib.sha256(contract['fixture_id'].encode()).hexdigest()[:24]
    output.mkdir(parents=True, exist_ok=True)
    archive = output / (stem + '.tar.gz')
    with archive.open('wb') as raw, gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as compressed:
        with tarfile.open(fileobj=compressed, mode='w', format=tarfile.PAX_FORMAT) as tar:
            for name in members:
                info = tarfile.TarInfo(name)
                info.size, info.mode = members[name]['size'], 0o644
                with (directory / name).open('rb') as stream:
                    tar.addfile(info, stream)
    manifest = {**contract, 'members': members, 'archive': {'name': archive.name, **file_pin(archive)}}
    path = output / (stem + '.manifest.json')
    write_json(path, manifest)
    verify_bundle(path, output, tensors=True)
    return path


def check_contract(contract):
    if contract['schema_version'] != 1 or contract['tensor_format'] != 'torch-flat-tensor-map-v1':
        raise ValueError('unsupported task contract')
    if contract['kind'] not in ('acceptance', 'diagnostic'):
        raise ValueError('unknown fixture kind')
    if contract['recipe_sha256'] != digest(contract['recipe']):
        raise ValueError('recipe identity mismatch')
    generator = contract['generator']
    if not COMMIT.fullmatch(generator['commit']) or not SHA.fullmatch(generator['lock_sha256']):
        raise ValueError('invalid generator provenance')
    identity = f"{contract['artifact_id']}/task/{contract['recipe_id']}/{contract['recipe_sha256']}/generator/{generator['commit']}/request/{contract['request_sha256']}"
    if identity != contract['fixture_id'] or not SHA.fullmatch(contract['request_sha256']):
        raise ValueError('fixture identity mismatch')
    references = contract['references']
    if not references or contract['artifact_id'] != references[0]['artifact_id']:
        raise ValueError('missing or wrong primary artifact')
    checkpoint = references[0]['weight_source']
    for reference in references:
        parts = reference['artifact_id'].split('/')
        if parts[2] != 'reference' or parts[4] != 'fp32' or reference['weight_source'] != checkpoint:
            raise ValueError('mixed artifact population, dtype or checkpoint')
        if not COMMIT.fullmatch(reference['producer_commit']):
            raise ValueError('invalid reference-release producer')
        for pin in (reference['contract'], reference['graph'], reference['map'], reference['config']):
            check_pin(pin)
        if reference['graph']['sha256'] != reference['graph_sha256']:
            raise ValueError('reference graph identity mismatch')
    cases = contract['cases']
    ids = [case['id'] for case in cases]
    if not ids or ids != contract['expected_cases'] or len(ids) != len(set(ids)):
        raise ValueError('case coverage mismatch')
    if contract['tolerances'] != references[0]['tolerances']:
        raise ValueError('original tolerances changed')
    for case in cases:
        if not SAFE.fullmatch(case['id']) or not case['files'] or not case['raw']:
            raise ValueError('missing case data')
        for group in case['files'].values():
            names = [tensor['name'] for tensor in group['tensors']]
            if not names or len(names) != len(set(names)):
                raise ValueError('invalid ordered tensor names')
            for tensor in group['tensors']:
                if not SHA.fullmatch(tensor['sha256']) or tensor['dtype'] not in ('float32', 'int64', 'uint8', 'bool'):
                    raise ValueError('invalid tensor metadata')
                if any(type(size) is not int or size < 0 for size in tensor['shape']):
                    raise ValueError('invalid tensor shape')


def tensor_records(tensors):
    import torch
    if type(tensors) is not dict or not tensors or any(type(key) is not str or not isinstance(t, torch.Tensor)
                                                    for key, t in tensors.items()):
        raise ValueError('expected a flat named tensor map')
    return [{'name': name, 'dtype': str(t.dtype).removeprefix('torch.'), 'shape': list(t.shape),
             'sha256': hashlib.sha256(t.detach().cpu().contiguous().reshape(-1).view(torch.uint8).numpy().tobytes()).hexdigest()}
            for name, t in tensors.items()]


def verify_bundle(manifest_path, assets, expected=None, tensors=False):
    manifest = read_json(manifest_path)
    contract = {key: value for key, value in manifest.items() if key not in ('archive', 'members')}
    check_contract(contract)
    if expected and any(contract[key] != expected[key] for key in ('fixture_id', 'artifact_id', 'recipe_sha256', 'expected_cases', 'kind')):
        raise ValueError('selected fixture differs from index')
    if not SAFE.fullmatch(manifest['archive']['name']):
        raise ValueError('unsafe archive name')
    archive = Path(assets) / manifest['archive']['name']
    verify_file(archive, manifest['archive'])
    members = manifest['members']
    with tempfile.TemporaryDirectory() as scratch:
        extract(archive, scratch, members)
        if read_json(Path(scratch) / 'task-contract.json') != contract:
            raise ValueError('archive contract differs from external manifest')
        for case in contract['cases']:
            for raw in case['raw']:
                if members.get(raw['path']) != {key: raw[key] for key in ('sha256', 'size')}:
                    raise ValueError('raw input pin missing from member inventory')
            for path, group in case['files'].items():
                if path not in members:
                    raise ValueError('case tensor file missing from inventory')
                if tensors:
                    import torch
                    value = torch.load(Path(scratch) / path, map_location='cpu', weights_only=True)
                    if tensor_records(value) != group['tensors']:
                        raise ValueError('tensor names, content, dtype or shape mismatch')
    return contract


def build_index(directory, repository, tag, request):
    directory = Path(directory)
    rows = []
    for path in sorted(directory.glob('*.manifest.json')):
        contract = verify_bundle(path, directory, tensors=True)
        manifest = read_json(path)
        assets = {'manifest': {'name': path.name, **file_pin(path)}, 'archive': manifest['archive']}
        for pin in assets.values():
            pin['url'] = f'https://github.com/{repository}/releases/download/{tag}/{pin["name"]}'
        rows.append({key: contract[key] for key in ('fixture_id', 'artifact_id', 'recipe_id', 'recipe_sha256', 'kind', 'expected_cases')} | {'assets': assets})
    if sorted(row['recipe_id'] for row in rows) != sorted(task['recipe_id'] for task in request['tasks']):
        raise ValueError('missing, duplicate or unexpected task bundles')
    document = {'schema_version': 1, 'repository': repository, 'release_tag': tag,
                'request_sha256': digest(request), 'reference_publication': request['reference_publication'], 'fixtures': rows}
    path = directory / 'task-fixtures.json'
    write_json(path, document)
    pin = {'name': path.name, 'url': f'https://github.com/{repository}/releases/download/{tag}/{path.name}', **file_pin(path)}
    write_json(directory / 'task-fixtures.pin.json', pin)
    return document


def verify_index(path, pin, assets, tensors=False):
    verify_file(path, pin)
    document = read_json(path)
    if document['schema_version'] != 1 or not document['fixtures']:
        raise ValueError('unsupported or empty task index')
    seen = set()
    for row in document['fixtures']:
        if row['fixture_id'] in seen:
            raise ValueError('duplicate fixture identity')
        seen.add(row['fixture_id'])
        for asset in row['assets'].values():
            if not SAFE.fullmatch(asset['name']):
                raise ValueError('unsafe asset name')
            verify_file(Path(assets) / asset['name'], asset)
        contract = verify_bundle(Path(assets) / row['assets']['manifest']['name'], assets, row, tensors)
        if contract['request_sha256'] != document['request_sha256'] or contract['reference_publication'] != document['reference_publication']:
            raise ValueError('fixture/index provenance mismatch')
    return document
