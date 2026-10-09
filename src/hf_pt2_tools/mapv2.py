"""Version-2 checkpoint map: where every captured tensor of a graph comes from, with declared conversions.

Specification: docs/checkpoint-map-v2.md. `build_map_v2` is the producer, `load_tensors` the reference consumer
that applies a map to local files and reproduces every capture's digest.
"""
import base64
import hashlib
import json
from pathlib import Path

import torch
from safetensors import safe_open
from safetensors.torch import save_file

from .artifacts import file_hash, write_json
from .inventory import SAFETENSORS_DTYPES, program_values

INLINE_LIMIT = 64 * 1024
TORCH_DTYPES = {code: getattr(torch, name) for name, code in SAFETENSORS_DTYPES.items()}


def value_digest(value):
    return hashlib.sha256(value.detach().cpu().contiguous().reshape(-1).view(torch.uint8).numpy().tobytes()).hexdigest()


def _bytes(value):
    return value.detach().cpu().contiguous().reshape(-1).view(torch.uint8).numpy().tobytes()


def _generator(value):
    """Exact description of an empty or uniform tensor, else None."""
    if value.numel() == 0:
        return {'op': 'empty'}
    raw, width = _bytes(value), value.element_size()
    first = raw[:width]
    if raw == first * value.numel():
        return {'op': 'fill', 'element_hex': first.hex()}
    return None


def describe_graph_owned(value):
    """Origin for a graph-owned tensor: generated, inline, or pending for the small graph-owned pack."""
    generator = _generator(value)
    if generator:
        return {'kind': 'generated', **generator}
    if value.numel() * value.element_size() <= INLINE_LIMIT:
        return {'kind': 'inline', 'data_base64': base64.b64encode(_bytes(value)).decode()}
    return {'kind': 'pack', 'pending': value}


def _source_dtype(name):
    return SAFETENSORS_DTYPES[name.removeprefix('torch.')]


def build_map_v2(binding, snapshot, program_path, output, artifact_id, release_base):
    """Write `<output>/<flat>.map.v2.json` (and a graph-owned pack when needed); return the document."""
    if 'captures' not in binding:
        raise ValueError('binding predates the all-capture inventory; rerun `hf-pt2 bind` for this graph')
    if binding['status'] != 'verified':
        raise ValueError('map requires a verified checkpoint binding')
    output, snapshot = Path(output), Path(snapshot)
    output.mkdir(parents=True, exist_ok=True)
    flat = artifact_id.replace('/', '--')
    reference, repo, revision = binding['reference'], binding['reference']['repo'], binding['reference']['revision']
    conversion = reference.get('conversion')
    files, hosted_as = [], {}
    for name in sorted(n for n in binding['checkpoint_sha256'] if n.endswith('.safetensors')):
        hosted_as[name] = name
        entry = {'name': name, 'sha256': binding['checkpoint_sha256'][name], 'size': binding['checkpoint_bytes'][name]}
        if conversion:
            hosted = f"{binding['model_id']}--{revision[:12]}.{name}"
            (output / hosted).write_bytes((snapshot / name).read_bytes())
            hosted_as[name] = hosted
            entry.update(name=hosted, url=release_base + hosted,
                         derived_from={'repo_id': repo, 'revision': revision, 'file': conversion['source'],
                                       'sha256': conversion['source_sha256'],
                                       'tool': 'hf-pt2 convert: torch.load(weights_only) to safetensors, tensor-for-tensor verified'})
        else:
            entry.update(url=f'https://huggingface.co/{repo}/resolve/{revision}/{name}', repo_id=repo, revision=revision)
        files.append(entry)
    values = program_values(torch.export.load(program_path))
    tensors, pack = {}, {}
    for row in binding['captures']:
        target, origin = row['target'], row['source']
        code = SAFETENSORS_DTYPES[row['dtype']]
        if origin['kind'] == 'checkpoint':
            held = _source_dtype(origin['source_dtype'])
            convert = {'op': 'none'} if held == code else {'op': 'cast', 'from': held, 'to': code}
            described = {'kind': 'checkpoint', 'file': hosted_as[origin['checkpoint_file']], 'key': origin['checkpoint_tensor'],
                         'convert': convert, 'tied_aliases': origin['tied_aliases']}
            digest = origin['loaded_sha256']
        else:
            value = values[target].detach().contiguous()
            digest = origin.get('value_sha256') or origin['payload_sha256']
            if value_digest(value) != digest:
                raise ValueError(f'graph-owned capture differs from the verified binding: {target}')
            described = describe_graph_owned(value)
            if described['kind'] == 'pack':
                pack[target] = described.pop('pending').clone()
                described['key'] = target
        tensors[target] = {'dtype': code, 'shape': row['shape'], 'sha256': digest, 'origin': described}
    sources = {'checkpoint': {'files': files}}
    if pack:
        pack_path = output / (flat + '.graph-owned.safetensors')
        save_file(pack, pack_path, metadata={'format': 'pt'})
        sources['graph_owned'] = {'name': pack_path.name, 'sha256': file_hash(pack_path), 'size': pack_path.stat().st_size,
                                  'url': release_base + pack_path.name}
    document = {'schema_version': 2, 'artifact_id': artifact_id, 'graph_sha256': binding['graph_sha256'],
                'model_id': binding['model_id'], 'sources': sources, 'tensors': tensors, 'unmapped': []}
    write_json(output / (flat + '.map.v2.json'), document)
    return document


def check_structure(document, rows, artifact_id, graph_sha256):
    """Without any weights: the map accounts for exactly the graph's captures, with matching dtype and shape."""
    if document['schema_version'] != 2 or document['unmapped']:
        raise ValueError('map schema or unmapped captures')
    if document['artifact_id'] != artifact_id or document['graph_sha256'] != graph_sha256:
        raise ValueError('map was made for a different artifact or graph')
    if sorted(document['tensors']) != sorted(row['target'] for row in rows):
        raise ValueError('map does not account for exactly the captured tensors')
    for row in rows:
        entry = document['tensors'][row['target']]
        if entry['dtype'] != SAFETENSORS_DTYPES[row['dtype']] or entry['shape'] != row['shape']:
            raise ValueError(f'dtype/shape mismatch: {row["target"]}')


def _generate(entry):
    origin, dtype = entry['origin'], TORCH_DTYPES[entry['dtype']]
    count = 1
    for extent in entry['shape']:
        count *= extent
    if origin['op'] == 'empty':
        return torch.empty(entry['shape'], dtype=dtype)
    return torch.frombuffer(bytearray(bytes.fromhex(origin['element_hex']) * count), dtype=dtype).reshape(entry['shape']).clone()


def load_tensors(document, directory):
    """Reference consumer: apply the map to files in `directory` (by source name) and verify every digest."""
    directory = Path(directory)
    sources = {f['name']: f for f in document['sources']['checkpoint']['files']}
    if 'graph_owned' in document['sources']:
        sources[document['sources']['graph_owned']['name']] = document['sources']['graph_owned']
    handles = {}
    for name, source in sources.items():
        path = directory / name
        if path.stat().st_size != source['size'] or file_hash(path) != source['sha256']:
            raise ValueError(f'source differs from its pin: {name}')
        handles[name] = safe_open(path, framework='pt', device='cpu')
    owned = document['sources'].get('graph_owned', {}).get('name')
    tensors = {}
    for target, entry in document['tensors'].items():
        origin = entry['origin']
        if origin['kind'] == 'checkpoint':
            value = handles[origin['file']].get_tensor(origin['key'])
            convert = origin['convert']
            if convert['op'] == 'cast':
                if SAFETENSORS_DTYPES[str(value.dtype).removeprefix('torch.')] != convert['from']:
                    raise ValueError(f'stored dtype differs from the declared conversion source: {target}')
                value = value.to(TORCH_DTYPES[convert['to']])
        elif origin['kind'] == 'pack':
            value = handles[owned].get_tensor(origin['key'])
        elif origin['kind'] == 'inline':
            value = torch.frombuffer(bytearray(base64.b64decode(origin['data_base64'])), dtype=TORCH_DTYPES[entry['dtype']]).reshape(entry['shape']).clone()
        else:
            value = _generate(entry)
        if SAFETENSORS_DTYPES[str(value.dtype).removeprefix('torch.')] != entry['dtype'] or list(value.shape) != entry['shape']:
            raise ValueError(f'applied value has the wrong dtype/shape: {target}')
        if value_digest(value) != entry['sha256']:
            raise ValueError(f'applied value differs from the pinned digest: {target}')
        tensors[target] = value
    return tensors
