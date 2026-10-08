"""Derived captured-value safetensors pack and the version-1 `safetensors.json` map for mltorch."""
import json
from pathlib import Path

import torch
from safetensors import safe_open
from safetensors.torch import save_file

from .artifacts import file_hash, write_json
from .checkpoints import tensor_hash
from .inventory import SAFETENSORS_DTYPES, program_values

SOURCE_FIELDS = ('repo_id', 'revision', 'url')


def build_pack(binding, snapshot, program_path, output, source, graph=None):
    """Combine verified checkpoint values with graph-owned captures; return the v1 map document."""
    if 'captures' not in binding:
        raise ValueError('binding predates the all-capture inventory; rerun `hf-pt2 bind` for this graph')
    if binding['status'] != 'verified':
        raise ValueError('pack requires a verified checkpoint binding')
    if graph is not None and file_hash(graph) != binding['graph_sha256']:
        raise ValueError('binding was made for a different graph; rerun `hf-pt2 bind`')
    missing = [field for field in SOURCE_FIELDS if not source.get(field)]
    if missing:
        raise ValueError(f'pack source needs a pinned location: {missing}')
    values = program_values(torch.export.load(program_path))
    handles = {name: safe_open(Path(snapshot) / name, framework='pt', device='cpu')
               for name in binding['checkpoint_sha256'] if name.endswith('.safetensors')}
    tensors = {}
    for row in binding['captures']:
        target, origin = row['target'], row['source']
        if origin['kind'] == 'checkpoint':
            value = handles[origin['checkpoint_file']].get_tensor(origin['checkpoint_tensor'])
            value = value.to(dtype=getattr(torch, row['dtype']))
            if tensor_hash(value) != origin['loaded_sha256']:
                raise ValueError(f'checkpoint value differs from the verified binding: {target}')
        else:
            value = values[target]
            digest = origin.get('value_sha256') or origin['payload_sha256']
            if tensor_hash(value) != digest:
                raise ValueError(f'graph-owned capture differs from the verified binding: {target}')
        tensors[target] = value.detach().contiguous().clone()
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    save_file(tensors, output, metadata={'format': 'pt'})
    document = {'schema_version': 1,
                'source': {'filename': output.name, 'repo_id': source['repo_id'], 'revision': source['revision'],
                           'sha256': file_hash(output), 'size': output.stat().st_size, 'url': source['url']},
                'tensors': {row['target']: {'dtype': SAFETENSORS_DTYPES[row['dtype']], 'key': row['target'],
                                            'shape': row['shape']} for row in binding['captures']},
                'unmapped': []}
    write_json(output.with_name(output.name.removesuffix('.safetensors') + '.map.json'), document)
    return document


def check_pack(document, pack, rows):
    """Mirror the consumer's up-front checks: every capture mapped, header agrees, source pin holds."""
    pack = Path(pack)
    if document['schema_version'] != 1 or document['unmapped']:
        raise ValueError('map schema or unmapped captures')
    source = document['source']
    if pack.stat().st_size != source['size'] or file_hash(pack) != source['sha256']:
        raise ValueError('pack differs from the pinned source digest/size')
    targets = [row['target'] for row in rows]
    if sorted(document['tensors']) != sorted(targets):
        raise ValueError('map does not account for exactly the captured tensors')
    with safe_open(pack, framework='pt', device='cpu') as archive:
        header = set(archive.keys())
        for row in rows:
            entry = document['tensors'][row['target']]
            if entry['key'] not in header:
                raise ValueError(f'missing in pack: {entry["key"]}')
            tensor = archive.get_slice(entry['key'])
            if entry['dtype'] != SAFETENSORS_DTYPES[row['dtype']] or tensor.get_dtype() != entry['dtype']:
                raise ValueError(f'dtype mismatch: {row["target"]}')
            if entry['shape'] != row['shape'] or list(tensor.get_shape()) != row['shape']:
                raise ValueError(f'shape mismatch: {row["target"]}')
    return True
