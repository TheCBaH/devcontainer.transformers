import copy

import pytest

from hf_pt2_tools.inventory import inventory


def tensor(dtype, *sizes):
    return {'dtype': dtype, 'sizes': [{'as_int': size} for size in sizes]}


def entry(path, dtype, *sizes, param=False):
    return {'path_name': path, 'is_param': param, 'tensor_meta': tensor(dtype, *sizes)}


def arg(name):
    return {'as_tensor': {'name': name}}


def graph():
    nodes = [
        {'target': 'torch.ops.aten.add.Tensor', 'inputs': [{'name': 'self', 'arg': arg('x')}, {'name': 'other', 'arg': arg('p_w')}],
         'outputs': [arg('add')]},
        {'target': 'torch.ops.aten.mul.Tensor', 'inputs': [{'name': 'self', 'arg': arg('add')}, {'name': 'other', 'arg': arg('c_s')}],
         'outputs': [arg('mul')]},
        {'target': 'torch.ops.aten.clone.default', 'inputs': [{'name': 'self', 'arg': arg('b_ids')}], 'outputs': [arg('clone')]},
    ]
    specs = [{'user_input': {'arg': arg('x')}},
             {'parameter': {'arg': {'name': 'p_w'}, 'parameter_name': 'w'}},
             {'buffer': {'arg': {'name': 'b_ids'}, 'buffer_name': 'ids', 'persistent': False}},
             {'tensor_constant': {'arg': {'name': 'c_s'}, 'tensor_constant_name': 's'}},
             {'tensor_constant': {'arg': {'name': 'c_dead'}, 'tensor_constant_name': 'dead'}}]
    values = {'x': tensor(7, 4), 'p_w': tensor(7, 4), 'b_ids': tensor(5, 2), 'c_s': tensor(7), 'c_dead': tensor(7, 0)}
    return {'graph': {'nodes': nodes, 'outputs': [arg('mul')], 'tensor_values': values}, 'signature': {'input_specs': specs}}


WEIGHTS = {'config': {'w': entry('weight_0', 7, 4, param=True)}}
CONSTANTS = {'config': {'ids': entry('tensor_0', 5, 2), 's': entry('tensor_1', 7), 'dead': entry('tensor_2', 7, 0)}}


def test_every_capture_kind_is_accounted_with_liveness():
    rows = {row['target']: row for row in inventory(graph(), WEIGHTS, CONSTANTS)}
    assert [r['kind'] for r in rows.values()] == ['PARAMETER', 'BUFFER', 'CONSTANT_TENSOR', 'CONSTANT_TENSOR']
    assert rows['w']['dtype'] == 'float32' and rows['w']['live'] and rows['w']['payload_name'] == 'weight_0'
    assert rows['ids']['dtype'] == 'int64' and rows['ids']['persistent'] is False
    assert rows['ids']['referenced'] and not rows['ids']['live']
    assert rows['s']['scalar'] and rows['s']['live']
    assert not rows['dead']['referenced'] and not rows['dead']['live'] and rows['dead']['shape'] == [0]


def test_unaccounted_and_inconsistent_entries_rejected():
    extra = copy.deepcopy(CONSTANTS)
    extra['config']['orphan'] = entry('tensor_3', 7, 1)
    with pytest.raises(ValueError, match='without a graph capture'):
        inventory(graph(), WEIGHTS, extra)
    missing = copy.deepcopy(CONSTANTS)
    del missing['config']['s']
    with pytest.raises(ValueError, match='no payload-config entry'):
        inventory(graph(), WEIGHTS, missing)
    wrong = copy.deepcopy(WEIGHTS)
    wrong['config']['w']['tensor_meta']['dtype'] = 6
    with pytest.raises(ValueError, match='disagree'):
        inventory(graph(), wrong, CONSTANTS)
    with pytest.raises(ValueError, match='both weight and constant'):
        inventory(graph(), {'config': {**WEIGHTS['config'], 's': entry('weight_9', 7)}}, CONSTANTS)
