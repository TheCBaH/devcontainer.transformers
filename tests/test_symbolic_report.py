import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from report_symbolic_shapes import expression, inspect_graph, render


def expr(text, hint=4):
    return {'as_expr': {'expr_str': text, 'hint': {'as_int': hint}}}


class SymbolicReportTests(unittest.TestCase):
    def graph(self):
        h = "Symbol('s15', positive=True, integer=True)"
        return {'range_constraints': {'s15': {'min_val': 1, 'max_val': 8}},
                'graph_module': {'graph': {
                    'tensor_values': {
                        'query': {'sizes': [{'as_int': 1}, {'as_int': 16}]},
                        'key': {'sizes': [{'as_int': 16}, expr(f'Add({h}, Integer(1))')]},
                        'result': {'sizes': [{'as_int': 1}, expr(f'Add({h}, Integer(1))')]}},
                    'sym_int_values': {'size': expr(h)},
                    'nodes': [
                        {'target': 'torch.ops.aten.matmul.default',
                         'inputs': [{'arg': {'as_tensor': {'name': name}}} for name in ('query', 'key')],
                         'outputs': [{'as_tensor': {'name': 'result'}}]},
                        {'target': 'torch.ops.aten.sym_size.int',
                         'inputs': [{'arg': {'as_tensor': {'name': 'key'}}}],
                         'outputs': [{'as_sym_int': {'as_name': 'size'}}]},
                        {'target': 'torch.ops.aten.empty.memory_format',
                         'inputs': [{'arg': {'as_sym_int': expr('Integer(4)')}}], 'outputs': []}]}}}

    def test_symbolic_tensor_operands_and_named_scalar_results(self):
        rows = inspect_graph(self.graph())
        self.assertEqual([r['operator'] for r in rows], ['aten.matmul.default', 'aten.sym_size.int'])
        self.assertEqual(rows[0]['symbols'], ['s15'])
        self.assertIn('key:[16,(s15+1)]', rows[0]['inputs'])
        self.assertIn('result:[1,(s15+1)]', rows[0]['outputs'])
        self.assertEqual(rows[1]['outputs'], 'size=s15')

    def test_hints_are_not_constants_and_constant_expressions_are_not_symbols(self):
        self.assertEqual(expression('Integer(4)'), ('4', set()))
        self.assertEqual(expression("Symbol('s15', positive=True, integer=True)"), ('s15', {'s15'}))

    def test_mixed_symint_list_is_detected_without_symbolic_tensor_dimensions(self):
        graph = self.graph()
        graph['graph_module']['graph']['nodes'] = [{
            'target': 'torch.ops.aten._assert_tensor_metadata.default',
            'inputs': [{'name': 'size', 'arg': {'as_sym_ints': [
                {'as_int': 1}, {'as_name': 'size'}, {'as_int': 16}]}}],
            'outputs': []}]
        rows = inspect_graph(graph)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['symbols'], ['s15'])
        self.assertEqual(rows[0]['inputs'], 'size=[1,s15,16]')

    def test_named_configurations_preserve_constants_and_list_boundaries(self):
        graph = self.graph()
        h = "Symbol('s15', positive=True, integer=True)"
        inner = graph['graph_module']['graph']
        inner['sym_int_values']['end'] = expr(f'Add({h}, Integer(1))')
        inner['nodes'] = [{
            'target': 'torch.ops.aten.slice.Tensor',
            'inputs': [
                {'name': 'self', 'arg': {'as_tensor': {'name': 'key'}}},
                {'name': 'dim', 'arg': {'as_int': 1}},
                {'name': 'start', 'arg': {'as_sym_int': {'as_int': 0}}},
                {'name': 'end', 'arg': {'as_sym_int': {'as_name': 'end'}}},
                {'name': 'step', 'arg': {'as_int': 1}}],
            'outputs': [{'as_tensor': {'name': 'result'}}]}, {
            'target': 'torch.ops.aten._assert_tensor_metadata.default',
            'inputs': [
                {'name': 'size', 'arg': {'as_sym_ints': [
                    {'as_int': 1}, {'as_int': 4}, {'as_name': 'end'}, {'as_int': 16}]}},
                {'name': 'stride', 'arg': {'as_sym_ints': [
                    {'as_int': 64}, {'as_int': 16}, {'as_int': 1}, {'as_int': 1}]}},
                {'name': 'pin_memory', 'arg': {'as_bool': False}},
                {'name': 'device', 'arg': {'as_none': True}}], 'outputs': []}]
        rows = inspect_graph(graph)
        self.assertEqual(rows[0]['inputs'],
                         'self=key:[16,(s15+1)], dim=1, start=0, end=(s15+1), step=1')
        self.assertEqual(rows[1]['inputs'],
                         'size=[1,4,(s15+1),16], stride=[64,16,1,1], pin_memory=False, device=None')
        self.assertEqual([row['symbols'] for row in rows], [['s15'], ['s15']])

    def test_tensor_lists_and_symbolic_predicates_keep_argument_names(self):
        graph = self.graph()
        inner = graph['graph_module']['graph']
        inner['sym_bool_values'] = {'guard': expr("Equality(Symbol('s15'), Integer(4))")}
        inner['nodes'] = [{
            'target': 'torch.ops.aten.cat.default',
            'inputs': [
                {'name': 'tensors', 'arg': {'as_tensors': [{'name': 'query'}, {'name': 'key'}]}},
                {'name': 'dim', 'arg': {'as_int': 0}}],
            'outputs': [{'as_tensor': {'name': 'result'}}]}, {
            'target': 'torch.ops.aten._assert_scalar.default',
            'inputs': [
                {'name': 'self', 'arg': {'as_sym_bool': {'as_name': 'guard'}}},
                {'name': 'assert_msg', 'arg': {'as_string': 'size must match'}}],
            'outputs': []}]
        rows = inspect_graph(graph)
        self.assertEqual(rows[0]['inputs'], 'tensors=[query:[1,16],key:[16,(s15+1)]], dim=0')
        self.assertEqual(rows[1]['inputs'], 'self=Equality(s15,4), assert_msg="size must match"')

    def test_report_links_graphs_scopes_symbols_and_rejects_tampering(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in ('first', 'second'):
                identity = f'{name}/text-decoder/tiny/decode/fp32/dynamo/dynamic'
                directory = root / 'models' / identity
                (directory / 'models').mkdir(parents=True)
                graph = directory / 'models/model.json'
                graph.write_text(json.dumps(self.graph()))
                (directory / 'contract.json').write_text(json.dumps({
                    'artifact_id': identity, 'graph_sha256': hashlib.sha256(graph.read_bytes()).hexdigest()}))
            first = render(root)
            self.assertEqual(first, render(root))
            self.assertIn('2 saved artifacts inspected; 2 contain symbolic', first)
            self.assertIn('first/text-decoder/tiny/decode/fp32/dynamo/dynamic/models/model.json', first)
            self.assertIn('second/text-decoder/tiny/decode/fp32/dynamo/dynamic/models/model.json', first)
            self.assertIn('| `s15` | `1` | `8` |', first)
            self.assertIn('`aten.matmul.default`', first)
            self.assertIn('size=s15', first)
            graph.write_text(graph.read_text() + ' ')
            with self.assertRaisesRegex(ValueError, 'graph hash mismatch'):
                render(root)


if __name__ == '__main__':
    unittest.main()
