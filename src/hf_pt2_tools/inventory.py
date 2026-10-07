"""Inventory of every serialized captured tensor (PARAMETER, BUFFER, CONSTANT_TENSOR) of a saved graph."""
import hashlib
import json
from pathlib import Path

import torch
from torch._export.serde.schema import ScalarType

SPEC_KINDS = {'parameter': ('parameter_name', 'PARAMETER'),
              'buffer': ('buffer_name', 'BUFFER'),
              'tensor_constant': ('tensor_constant_name', 'CONSTANT_TENSOR')}
DTYPE_NAMES = {ScalarType.FLOAT: 'float32', ScalarType.HALF: 'float16', ScalarType.BFLOAT16: 'bfloat16',
               ScalarType.DOUBLE: 'float64', ScalarType.LONG: 'int64', ScalarType.INT: 'int32',
               ScalarType.SHORT: 'int16', ScalarType.CHAR: 'int8', ScalarType.BYTE: 'uint8', ScalarType.BOOL: 'bool'}
SAFETENSORS_DTYPES = {'float32': 'F32', 'float16': 'F16', 'bfloat16': 'BF16', 'float64': 'F64', 'int64': 'I64',
                      'int32': 'I32', 'int16': 'I16', 'int8': 'I8', 'uint8': 'U8', 'bool': 'BOOL'}
EFFECT_MARKERS = ('assert', 'constrain')


def value_hash(value):
    return hashlib.sha256(value.detach().cpu().contiguous().reshape(-1).view(torch.uint8).numpy().tobytes()).hexdigest()


def _tensor_names(node):
    """Names of tensors referenced anywhere inside a serialized argument tree."""
    names = []
    if isinstance(node, dict):
        for key, value in node.items():
            if key == 'as_tensor' and isinstance(value, dict) and 'name' in value:
                names.append(value['name'])
            elif key == 'as_tensors':
                names.extend(item['name'] for item in value)
            else:
                names.extend(_tensor_names(value))
    elif isinstance(node, list):
        for item in node:
            names.extend(_tensor_names(item))
    return names


def liveness(graph):
    """Return (referenced, live) tensor-name sets: any use by a node, and reachable from outputs/effects."""
    nodes = graph['graph']['nodes']
    referenced = {name for node in nodes for name in _tensor_names(node['inputs'])}
    referenced |= set(_tensor_names(graph['graph']['outputs']))
    produced = {}
    for index, node in enumerate(nodes):
        for name in _tensor_names(node['outputs']):
            produced[name] = index
    live = set(_tensor_names(graph['graph']['outputs']))
    pending = list(live)
    for node in nodes:
        if any(marker in node['target'] for marker in EFFECT_MARKERS):
            for name in _tensor_names(node['inputs']):
                if name not in live:
                    live.add(name)
                    pending.append(name)
    while pending:
        name = pending.pop()
        if name in produced:
            for source in _tensor_names(nodes[produced[name]]['inputs']):
                if source not in live:
                    live.add(source)
                    pending.append(source)
    return referenced, live


def _config_entries(*configs):
    entries = {}
    for config in configs:
        for name, entry in config['config'].items():
            if name in entries:
                raise ValueError(f'captured value in both weight and constant configs: {name}')
            entries[name] = entry
    return entries


def _shape(meta):
    if any('as_int' not in size for size in meta['sizes']):
        raise ValueError('captured tensor with a symbolic shape')
    return [size['as_int'] for size in meta['sizes']]


def inventory(graph, weights_config, constants_config):
    """Structural inventory from the committed JSON alone; no tensor bytes needed."""
    configs = _config_entries(weights_config, constants_config)
    referenced, live = liveness(graph)
    entries, seen = [], set()
    for spec in graph['signature']['input_specs']:
        kind = next(iter(spec))
        if kind not in SPEC_KINDS:
            if kind in ('user_input',):
                continue
            raise ValueError(f'unsupported graph input kind: {kind}')
        field, label = SPEC_KINDS[kind]
        body = spec[kind]
        target, ssa = body[field], body['arg']['name']
        if target not in configs:
            raise ValueError(f'captured value has no payload-config entry: {target}')
        if target in seen:
            raise ValueError(f'duplicate captured value: {target}')
        seen.add(target)
        meta = configs[target]['tensor_meta']
        graph_meta = graph['graph']['tensor_values'][ssa]
        shape = _shape(meta)
        if graph_meta['dtype'] != meta['dtype'] or [s.get('as_int') for s in graph_meta['sizes']] != shape:
            raise ValueError(f'graph and payload config disagree about {target}')
        entry = {'kind': label, 'ssa_name': ssa, 'target': target, 'payload_name': configs[target]['path_name'],
                 'dtype': DTYPE_NAMES[ScalarType(meta['dtype'])], 'shape': shape,
                 'referenced': ssa in referenced, 'live': ssa in live, 'scalar': kind == 'tensor_constant' and not shape}
        if kind == 'buffer':
            entry['persistent'] = body['persistent']
        entries.append(entry)
    extra = sorted(set(configs) - seen)
    if extra:
        raise ValueError(f'payload config entries without a graph capture: {extra}')
    return entries


def captures_document(identity, graph_sha256, entries, values=None):
    """Attach per-entry sources: graph-owned payload (with value digest) for exported random/library weights."""
    rows = []
    for entry in entries:
        row = {**entry, 'source': {'kind': 'payload'}}
        if values is not None:
            row['source']['value_sha256'] = value_hash(values[entry['target']])
        rows.append(row)
    return {'schema_version': 1, 'artifact_id': identity, 'graph_sha256': graph_sha256, 'captures': rows,
            'counts': {kind: sum(r['kind'] == kind for r in rows) for kind in ('PARAMETER', 'BUFFER', 'CONSTANT_TENSOR')}}


def program_values(program):
    """Captured tensors of an ExportedProgram keyed by signature target (state dict, then constants)."""
    values = {}
    for spec in program.graph_signature.input_specs:
        target = spec.target
        if target is None:
            continue
        if target in program.state_dict:
            values[target] = program.state_dict[target]
        elif target in program.constants and isinstance(program.constants[target], torch.Tensor):
            values[target] = program.constants[target]
    return values


def load_graph(directory):
    directory = Path(directory)
    graph = json.loads((directory / 'models/model.json').read_text())['graph_module']
    weights = json.loads((directory / 'data/weights/model_weights_config.json').read_text())
    constants = json.loads((directory / 'data/constants/model_constants_config.json').read_text())
    return graph, weights, constants


def check_captures_document(document, directory, contract):
    """Recompute the structural inventory from the artifact's JSON and require an exact match."""
    graph, weights, constants = load_graph(directory)
    expected = inventory(graph, weights, constants)
    if document.get('artifact_id') != contract['artifact_id'] or document.get('graph_sha256') != contract['graph_sha256']:
        raise ValueError('captures manifest identity mismatch')
    structural = [{k: v for k, v in row.items() if k != 'source'} for row in document['captures']]
    if structural != expected:
        raise ValueError('captures manifest differs from the saved graph and payload configs')
    for row in document['captures']:
        source = row['source']
        if source['kind'] != 'payload' or len(source.get('value_sha256', '')) != 64:
            raise ValueError('capture lacks a graph-owned value digest')
