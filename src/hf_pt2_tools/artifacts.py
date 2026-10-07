import hashlib
import json
import os
from pathlib import Path
import shutil

from pt2_export_core.archive import graph_op_counts
from pt2_export_core.opgraph import DROPPED_OPS, strict_json_loads
from pt2_export_core.schema_validate import validate_document
from torch._export.serde.schema import ScalarType


def write_json(path, document):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(document, indent=2, sort_keys=True, allow_nan=False) + '\n')
    os.replace(temporary, path)


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_artifact(root, directory, expected_id=None):
    directory = Path(directory)
    contract = strict_json_loads((directory / 'contract.json').read_text())
    facts = strict_json_loads((directory / 'models/op_facts.json').read_text())
    for name, document in [('contract', contract), ('op-facts', facts)]:
        validate_document(document, name, str(Path(root) / 'schemas'))
    if expected_id is not None and contract['artifact_id'] != expected_id:
        raise ValueError('artifact identity mismatch')
    graph_hash = file_hash(directory / 'models/model.json')
    if graph_hash != contract['graph_sha256'] or graph_hash != facts['graph_sha256']:
        raise ValueError('graph/contract/facts hash mismatch')
    if graph_op_counts(directory / 'models/model.json') != facts['counts']:
        raise ValueError('published graph/operator counts differ')
    computation = {}
    for op, _, count in facts['ops']:
        computation[op] = computation.get(op, 0) + count
    if computation != {op: count for op, count in facts['counts'].items()
                       if op not in DROPPED_OPS and not op.startswith('_operator.')
                       and not op.startswith('torch.sym_')}:
        raise ValueError('computational operator facts differ from graph')
    graph = strict_json_loads((directory / 'models/model.json').read_text())['graph_module']
    signature = graph['module_call_graph'][0]['signature']
    input_spec = strict_json_loads(signature['in_spec'])[1]
    if input_spec['children_spec'][0]['children_spec'] or input_spec['children_spec'][1]['type'] != 'builtins.dict':
        raise ValueError('unsupported positional/custom input structure')
    keys = strict_json_loads(input_spec['children_spec'][1]['context'])
    if keys != contract['call']['kwargs'] or keys != [t['name'] for t in contract['inputs']]:
        raise ValueError('contract does not describe the saved call signature')
    out_spec = strict_json_loads(signature['out_spec'])[1]
    if out_spec['type'] != 'builtins.tuple' or len(out_spec['children_spec']) != len(contract['outputs']):
        raise ValueError('contract output structure differs from graph')
    if any(child['type'] is not None for child in out_spec['children_spec']):
        raise ValueError('custom output dependency at published boundary')
    dtypes = {'float32': ScalarType.FLOAT, 'float16': ScalarType.HALF,
              'bfloat16': ScalarType.BFLOAT16, 'int64': ScalarType.LONG,
              'int32': ScalarType.INT, 'bool': ScalarType.BOOL}
    specs = graph['signature']
    saved_inputs = [spec['user_input']['arg']['as_tensor']['name'] for spec in specs['input_specs'] if 'user_input' in spec]
    saved_outputs = [spec['user_output']['arg']['as_tensor']['name'] for spec in specs['output_specs'] if 'user_output' in spec]
    for names, metadata in ((saved_inputs, contract['inputs']), (saved_outputs, contract['outputs'])):
        if len(names) != len(metadata):
            raise ValueError('tensor metadata length differs from graph')
        for name, tensor in zip(names, metadata, strict=True):
            saved = graph['graph']['tensor_values'][name]
            if saved['dtype'] != int(dtypes[tensor['dtype']]) or len(saved['sizes']) != len(tensor['shape']):
                raise ValueError('tensor dtype/rank metadata differs from graph')
            if any('as_int' in size and size['as_int'] != extent
                   for size, extent in zip(saved['sizes'], tensor['shape'], strict=True)):
                raise ValueError('static tensor shape metadata differs from graph')
    for relative, expected in contract['files'].items():
        if relative not in ('models/model.json', 'data/weights/model_weights_config.json',
                            'data/constants/model_constants_config.json', 'cases.json'):
            raise ValueError('unknown contract file')
        if file_hash(directory / relative) != expected:
            raise ValueError('contract file hash mismatch')
    if 'cases.json' not in contract['files']:
        raise ValueError('artifact lacks a cases manifest')
    from .fixtures import check_cases_document
    check_cases_document(strict_json_loads((directory / 'cases.json').read_text()), contract)
    return contract


def publish(stage, destination):
    stage, destination = Path(stage), Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    previous = destination.with_name(destination.name + '.previous')
    if previous.exists():
        if not destination.exists():
            os.replace(previous, destination)
        else:
            shutil.rmtree(previous)
    if destination.exists():
        os.replace(destination, previous)
    try:
        os.replace(stage, destination)
    except BaseException:
        if previous.exists():
            os.replace(previous, destination)
        raise
    if previous.exists():
        shutil.rmtree(previous)
