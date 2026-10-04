import hashlib
import importlib.metadata
import json
from pathlib import Path

import torch
from huggingface_hub import snapshot_download
from safetensors import safe_open

from .artifacts import file_hash, verify_artifact, write_json
from .registry import CONFIG_CLASSES, read_manifest


def fetch(root, name):
    entry = next(e for e in read_manifest(root)['models'] if e['id'] == name)
    reference = entry['reference']
    if not reference['safetensors_files']:
        raise ValueError(f'{name}: no upstream safetensors at the pinned revision')
    path = snapshot_download(reference['repo'], revision=reference['revision'],
                             cache_dir=Path(root) / '.hf-cache',
                             allow_patterns=['config.json', 'model.safetensors.index.json', *reference['safetensors_files']])
    if file_hash(Path(path) / 'config.json') != reference['config_sha256']:
        raise ValueError('downloaded config differs from the pinned snapshot')
    return path


def tensor_hash(value):
    return hashlib.sha256(value.detach().cpu().contiguous().reshape(-1).view(torch.uint8).numpy().tobytes()).hexdigest()


def bind(root, name, graph_root, output):
    import transformers
    from transformers.conversion_mapping import get_model_conversion_mapping
    from transformers.core_model_loading import WeightRenaming

    root = Path(root)
    entry = next(e for e in read_manifest(root)['models'] if e['id'] == name)
    reference = entry['reference']
    if not reference['safetensors_files']:
        document = {'schema_version': 1, 'model_id': name, 'status': 'unavailable',
                    'reason': 'no upstream safetensors at the pinned revision', 'reference': reference}
        write_json(output, document)
        return document
    contract = verify_artifact(root, Path(graph_root).parent.parent)
    if contract['population'] != 'reference' or contract['model_id'] != name or contract['model_class'] != entry['model_class']:
        raise ValueError('checkpoint binding requires this model\'s original-config graph')
    snapshot = Path(snapshot_download(reference['repo'], revision=reference['revision'],
                                    cache_dir=root / '.hf-cache', local_files_only=True,
                                    allow_patterns=['config.json', 'model.safetensors.index.json', *reference['safetensors_files']]))
    if file_hash(snapshot / 'config.json') != reference['config_sha256']:
        raise ValueError('cached config differs from the pinned snapshot')
    config = getattr(transformers, CONFIG_CLASSES[entry['model_class']]).from_dict(
        json.loads((root / 'configs/reference' / (entry.get('config_model_id', name) + '.json')).read_text()))
    config.use_cache = False
    model = getattr(transformers, entry['model_class']).from_pretrained(
        snapshot, config=config, local_files_only=True, use_safetensors=True,
        dtype=torch.float32, attn_implementation='eager').eval()
    tensors = {}
    files = {}
    for filename in reference['safetensors_files']:
        path = snapshot / filename
        files[filename] = file_hash(path)
        with safe_open(path, framework='pt', device='cpu') as archive:
            for key in archive.keys():
                if key in tensors:
                    raise ValueError('duplicate checkpoint tensor key across shards')
                tensors[key] = (filename, archive.get_tensor(key))
    index = snapshot / 'model.safetensors.index.json'
    if index.exists():
        weight_map = json.loads(index.read_text())['weight_map']
        if weight_map != {key: filename for key, (filename, _) in tensors.items()}:
            raise ValueError('shard index differs from the pinned tensor files')
        files[index.name] = file_hash(index)
    graph = json.loads(Path(graph_root).read_text())['graph_module']
    renamings = [conversion for conversion in get_model_conversion_mapping(model)
                 if isinstance(conversion, WeightRenaming)]
    converted_keys = {}
    for source in tensors:
        renamed = source
        for conversion in renamings:
            renamed, _ = conversion.rename_source_key(renamed)
        converted_keys.setdefault(renamed, []).append(source)
    parameters = dict(model.named_parameters(remove_duplicate=False))
    aliases = {}
    for key, value in parameters.items():
        aliases.setdefault(id(value), []).append(key)
    bindings = []
    unused = []
    for spec in graph['signature']['input_specs']:
        if 'parameter' not in spec:
            continue
        parameter = spec['parameter']
        target = parameter['parameter_name']
        local = target.removeprefix('model.')
        value = parameters[local]
        candidate_keys = [local, 'model.' + local]
        for alias in aliases[id(value)]:
            candidate_keys.extend([alias, 'model.' + alias])
        candidates = [key for key in dict.fromkeys(candidate_keys) if key in tensors]
        for alias in aliases[id(value)]:
            candidates.extend(converted_keys.get(alias, []))
        candidates = list(dict.fromkeys(candidates))
        if not candidates:
            argument = parameter['arg']['name']
            used = any(argument in json.dumps(node['inputs']) for node in graph['graph']['nodes'])
            used = used or argument in json.dumps(graph['graph']['outputs'])
            if not used:
                unused.append({'graph_parameter': target, 'reason': 'absent from checkpoint; graph input is unused'})
                continue
            raise ValueError(f'no pinned checkpoint tensor or tied alias for {local}')
        source = candidates[0]
        filename, checkpoint_value = tensors[source]
        serialized = graph['graph']['tensor_values'][parameter['arg']['name']]
        shape = [size['as_int'] for size in serialized['sizes']]
        if list(value.shape) != shape or list(checkpoint_value.shape) != shape:
            raise ValueError('graph/checkpoint/library parameter shape differs')
        converted = checkpoint_value.to(dtype=value.dtype)
        if not torch.equal(value.detach(), converted):
            raise ValueError(f'checkpoint binding differs from library load: {local}')
        bindings.append({'graph_parameter': target, 'checkpoint_file': filename,
                         'checkpoint_tensor': source, 'library_parameter': local, 'shape': shape,
                         'source_dtype': str(checkpoint_value.dtype), 'loaded_dtype': str(value.dtype),
                         'loaded_sha256': tensor_hash(value),
                         'key_renamed': source != local,
                         'tied_aliases': aliases[id(value)] if len(aliases[id(value)]) > 1 else []})
    document = {'schema_version': 1, 'model_id': name, 'status': 'verified',
                'graph_sha256': file_hash(graph_root), 'reference': reference,
                'checkpoint_sha256': files, 'bindings': bindings, 'unbound_unused_parameters': unused,
                'versions': {name: importlib.metadata.version(name) for name in ('transformers', 'torch', 'safetensors')},
                'conversion': 'library load and checkpoint values compared after explicit float32 conversion',
                'scope': 'parameter bindings for an original-config architecture graph; no pretrained accuracy claim'}
    write_json(output, document)
    return document
