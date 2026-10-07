"""Report symbolic dimensions and scalars directly from saved functional graphs."""
import argparse
import ast
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
from urllib.parse import quote


def expression(source):
    tree = ast.parse(source, mode='eval').body
    symbols = {node.args[0].value for node in ast.walk(tree)
               if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
               and node.func.id == 'Symbol' and node.args
               and isinstance(node.args[0], ast.Constant)}
    functions = {node.func.id for node in ast.walk(tree)
                 if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
    symbols.update(node.id for node in ast.walk(tree)
                   if isinstance(node, ast.Name) and node.id not in functions and node.id != 'oo')

    def fmt(node):
        if isinstance(node, ast.Constant):
            return str(node.value)
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            name = node.func.id
            args = [fmt(arg) for arg in node.args]
            if name in ('Symbol', 'Integer', 'Float'):
                return args[0]
            if name in ('Add', 'Mul'):
                return '(' + ('+' if name == 'Add' else '*').join(args) + ')'
            if name in ('Pow', 'Rational'):
                return '(' + ('**' if name == 'Pow' else '/').join(args) + ')'
            return name + '(' + ','.join(args) + ')'
        return ast.unparse(node)

    return fmt(tree), symbols


def scalar(value):
    if 'as_expr' in value:
        return expression(value['as_expr']['expr_str'])
    for key in ('as_int', 'as_bool', 'as_float'):
        if key in value:
            return str(value[key]), set()
    raise ValueError(f'unknown scalar encoding: {value}')


def references(value):
    if isinstance(value, list):
        for item in value:
            yield from references(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            if key in ('as_tensor', 'as_sym_int', 'as_sym_bool', 'as_sym_float'):
                yield key, item
            elif key == 'as_tensors':
                for tensor in item:
                    yield 'as_tensor', tensor
            elif key in ('as_sym_ints', 'as_sym_bools', 'as_sym_floats'):
                for element in item:
                    yield key[:-1], element
            else:
                yield from references(item)


def argument(value, graph):
    tables = {'as_sym_int': 'sym_int_values', 'as_sym_bool': 'sym_bool_values',
              'as_sym_float': 'sym_float_values'}
    kind, ref = next(iter(value.items()))
    if kind == 'as_tensor':
        name = ref['name']
        dims = [scalar(dim) for dim in graph['tensor_values'][name]['sizes']]
        return (name + ':[' + ','.join(text for text, _ in dims) + ']',
                {symbol for _, symbols in dims for symbol in symbols})
    if kind in tables:
        name = ref.get('as_name')
        return scalar(graph[tables[kind]][name] if name is not None else ref)
    if kind in ('as_tensors', 'as_sym_ints', 'as_sym_bools', 'as_sym_floats'):
        parts = [argument({kind[:-1]: item}, graph) for item in ref]
        return ('[' + ','.join(text for text, _ in parts) + ']',
                {symbol for _, symbols in parts for symbol in symbols})
    if kind in ('as_int', 'as_bool', 'as_float'):
        return scalar(value)
    if kind == 'as_none':
        return 'None', set()
    if kind in ('as_string', 'as_ints', 'as_bools', 'as_floats', 'as_strings'):
        return json.dumps(ref, separators=(',', ':')), set()
    return json.dumps(value, sort_keys=True, separators=(',', ':')), set()


def describe(value, graph):
    parts, symbols = [], set()
    for index, item in enumerate(value):
        is_input = 'arg' in item
        encoded = item['arg'] if is_input else item
        text, names = argument(encoded, graph)
        if is_input:
            text = item.get('name', f'arg[{index}]') + '=' + text
        elif any(kind in encoded for kind in ('as_sym_int', 'as_sym_bool', 'as_sym_float')):
            ref = next(iter(encoded.values()))
            if 'as_name' in ref:
                text = ref['as_name'] + '=' + text
        parts.append(text)
        symbols.update(names)
    return ', '.join(parts) or '—', symbols


def inspect_graph(document):
    graph = document['graph_module']['graph']
    rows = []
    for index, node in enumerate(graph['nodes']):
        inputs, input_symbols = describe(node['inputs'], graph)
        outputs, output_symbols = describe(node['outputs'], graph)
        symbols = input_symbols | output_symbols
        if symbols:
            names = [ref.get('name', ref.get('as_name')) for _, ref in references(node['outputs'])]
            name = next((name for name in names if name), f'nodes[{index}]')
            rows.append({'name': name, 'operator': node['target'].removeprefix('torch.ops.'),
                         'inputs': inputs, 'outputs': outputs, 'symbols': sorted(symbols)})
    return rows


def artifacts(root):
    model_root = Path(root) / 'models'
    for path in sorted(model_root.rglob('contract.json')):
        contract = json.loads(path.read_text())
        identity = str(path.parent.relative_to(model_root))
        if contract['artifact_id'] != identity:
            raise ValueError(f'artifact identity mismatch: {path}')
        graph_path = path.parent / 'models/model.json'
        data = graph_path.read_bytes()
        if hashlib.sha256(data).hexdigest() != contract['graph_sha256']:
            raise ValueError(f'graph hash mismatch: {graph_path}')
        graph = json.loads(data)
        rows = inspect_graph(graph)
        yield {'id': identity, 'path': str(graph_path.relative_to(root)),
               'nodes': len(graph['graph_module']['graph']['nodes']),
               'rows': rows, 'symbols': sorted({s for row in rows for s in row['symbols']}),
               'ranges': graph['range_constraints'], 'sha256': contract['graph_sha256']}


def code(text):
    return '`' + str(text).replace('`', '&#96;').replace('|', '\\|') + '`'


def render(root):
    items = list(artifacts(root))
    affected = [item for item in items if item['rows']]
    count = sum(len(item['rows']) for item in items)
    lines = ['# Symbolic shapes in functional graphs', '',
             f'{len(items)} saved artifacts inspected; {len(affected)} contain symbolic dimensions '
             f'or scalars, affecting {count} nodes.', '',
             'Generated from the hash-bound `models/**/models/model.json` files. This includes '
             'forward, encoder, vision, connector, prefill and decode artifacts present under '
             '`models/`. Symbols are local to each artifact: the same name in two graphs '
             'does not connect their dimensions. Export hints are examples, not fixed sizes. '
             'A static input contract can still contain data-dependent internal dimensions.', '',
             'A node is included when an input/output tensor dimension or scalar contains a '
             'symbol. This catches tensor operations such as `matmul` as well as explicit '
             'SymInt arguments and symbolic guard predicates. Fixed SymInt-typed values alone '
             'do not qualify a node. Included nodes retain every serialized argument by name, '
             'including fixed settings and complete mixed lists such as `size=[1,4,(s15+1),16]`. '
             'Symbolic references are resolved to expressions; constants remain literal. '
             'Shape-reading nodes supply scalar sizes at runtime; the input tensors '
             'carry the actual dimensions. Symbolic strides alone are outside this report.', '',
             'The operator catalog in [ops-func.md](ops-func.md) describes the core forward '
             'population; this report describes the saved functional artifacts. It does not '
             'measure FLOPs or count inference steps.', '',
             '| Artifact | Graph nodes | Affected nodes | Symbols |',
             '| --- | ---: | ---: | --- |']
    for index, item in enumerate(items, 1):
        label = code(item['id'])
        target = f'#artifact-{index}' if item['rows'] else quote(item['path'], safe='/')
        lines.append(f"| [{label}]({target}) | {item['nodes']} | {len(item['rows'])} | "
                     f"{', '.join(map(code, item['symbols'])) or '—'} |")

    usage = defaultdict(list)
    for index, item in enumerate(items, 1):
        for operator, nodes in sorted(Counter(row['operator'] for row in item['rows']).items()):
            usage[operator].append((index, item['id'], nodes))
    lines += ['', '## Operators using symbolic shapes or scalars', '',
              '| Operator | Affected nodes | Model artifacts (node counts) |',
              '| --- | ---: | --- |']
    for operator, users in sorted(usage.items()):
        links = ', '.join(f'[{code(identity)}](#artifact-{index}) ({count})'
                          for index, identity, count in users)
        lines.append(f'| {code(operator)} | {sum(n for _, _, n in users)} | {links} |')
    if not usage:
        lines += ['', 'No nodes with symbolic dimensions or scalars were found.']

    for index, item in enumerate(items, 1):
        if not item['rows']:
            continue
        lines += ['', f'<a id="artifact-{index}"></a>', '', f"## {item['id']}", '',
                  f"[Saved graph]({quote(item['path'], safe='/')}) · "
                  f"[Contract]({quote(item['path'].replace('models/model.json', 'contract.json'), safe='/')})", '',
                  f"Graph SHA256: {code(item['sha256'])}.", '',
                  '| Symbol or expression | Minimum | Maximum |',
                  '| --- | ---: | ---: |']
        if item['ranges']:
            for expr, bounds in sorted(item['ranges'].items()):
                lines.append(f"| {code(expr)} | {code(bounds['min_val'])} | {code(bounds['max_val'])} |")
        else:
            lines += ['| No declared ranges | — | — |']
        lines += ['', '| Operator | Affected nodes | Symbols | Example node |',
                  '| --- | ---: | --- | --- |']
        grouped = defaultdict(list)
        for row in item['rows']:
            grouped[row['operator']].append(row)
        for operator, rows in sorted(grouped.items()):
            symbols = sorted({symbol for row in rows for symbol in row['symbols']})
            lines.append(f"| {code(operator)} | {len(rows)} | {', '.join(map(code, symbols))} | "
                         f"{code(rows[0]['name'])} |")
        lines += ['', '<details>', '<summary>Every affected node: tensor shapes and named argument configurations</summary>', '',
                  '| Node | Operator | Inputs and argument configurations | Outputs | Symbols |',
                  '| --- | --- | --- | --- | --- |']
        for row in item['rows']:
            lines.append('| ' + ' | '.join([code(row['name']), code(row['operator']),
                         code(row['inputs']), code(row['outputs']),
                         ', '.join(map(code, row['symbols']))]) + ' |')
        lines += ['', '</details>']
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('.'))
    args = parser.parse_args()
    root = args.root.resolve()
    (root / 'symbolic-shapes.md').write_text(render(root))


if __name__ == '__main__':
    main()
