from pathlib import Path

from pt2_export_core import catalog
from pt2_export_core.selection import build_candidates, select
import yaml

from .artifacts import write_json


def render(root, document):
    root = Path(root)
    rows = document['models']
    policies = ', '.join(sorted({row['policy'] for row in rows.values()}))
    dtypes = ', '.join(sorted({row['dtype'] for row in rows.values()}))
    lines = ['# Transformers architecture probes', '',
             f"Population: **{document['population']}**, deterministic random weights. "
             f"{document['verified']}/{document['attempted']} attempted artifacts verified. "
             'Coverage describes this curated population, not the full Transformers library.', '',
             f'CPU eager attention; policies: {policies}; dtypes: {dtypes}; strict=False, no caches, functional tensor-tuple boundary. '
             'FLOPs are not measured. These probes do not establish pretrained accuracy.', '',
             '| Model | Category | Parameters | Weight MiB | ATen / functional / core nodes | Result |',
             '| --- | --- | ---: | ---: | --- | --- |']
    for name, row in sorted(rows.items()):
        nodes = [str(sum(cell[2] for cell in row['ops'].get(d, [])))
                 if d in row['ops'] else '—' for d in ('aten', 'func', 'core-cpu')]
        outcome = row['status'] if row['status'] == 'ok' else f"{row['status']}: {row.get('failed_stage', 'worker')}"
        lines.append(f"| {name} | {row['category']} | {row.get('parameter_count', '—')} | "
                     f"{row.get('weight_bytes', 0) / 2**20:.3f} | {' / '.join(nodes)} | {outcome} |")
    lines += ['', 'Original checkpoint pins remain in `model-candidates.yaml`; tiny probes use separately '
              'reviewed configs. Time-series outputs are model states, location and scale; forecasting '
              'requires its distribution head and host sampling loop.', '']
    (root / 'models.md').write_text('\n'.join(lines))
    for label, dialect in [('aten', catalog.ATEN), ('func', catalog.FUNC), ('core-cpu', catalog.core('cpu'))]:
        matrices = {name: row['ops'][label] for name, row in sorted(rows.items()) if label in row['ops']}
        skipped = {name: row.get('failed_stage', 'not collected') for name, row in rows.items() if label not in row['ops']}
        families = {name: row['category'] for name, row in rows.items()}
        schemas = {op: schema for row in rows.values() for op, schema in row['schemas'].items()}
        versions = next(iter(rows.values()))['producer']['versions']
        (root / f'ops-{label}.yaml').write_text(catalog.render_ops_yaml(
            matrices, schemas, skipped, dialect, 'Transformers', versions['transformers'],
            versions['torch'], script='hf-pt2 report'))
        (root / f'ops-{label}.md').write_text(catalog.render_ops_md(
            matrices, schemas, families, skipped, dialect, 'Transformers', versions['transformers'],
            versions['torch'], script='hf-pt2 report'))


def selection(root, document):
    root = Path(root)
    rows = document['models']
    successful = {name: row for name, row in rows.items() if row['status'] == 'ok'}
    adapted = {name: {'status': 'ok', 'family': row['category'],
                      'weight_str': str(row['weight_bytes'] / 2**20)} for name, row in successful.items()}
    matrices = [{name: row['ops'][dialect] for name, row in successful.items() if dialect in row['ops']}
                for dialect in ('func', 'aten', 'core-cpu')]
    candidates = build_candidates(adapted, *matrices)
    includes = []
    for category in sorted({row['category'] for row in rows.values()}):
        options = [name for name, row in successful.items() if row['category'] == category]
        if not options:
            raise ValueError(f'no verified representative for {category}')
        includes.append(min(options, key=lambda name: (candidates[name]['nodes'], name)))
    chosen = select(candidates, len(candidates), 10000, 64, includes, [])
    units = set().union(*(c['ops'] for c in candidates.values()))
    covered = set().union(*(candidates[name]['ops'] for name, _ in chosen))
    manifest = {'schema_version': 1, 'population': document['population'],
                'selection': {'max_weight_mb': 64, 'release_max_weight_mb': 64,
                              'candidate_count': len(candidates), 'selected_count': len(chosen),
                              'covered_units': len(covered), 'total_units': len(units),
                              'uncovered_units': sorted(units - covered), 'mandatory_categories': sorted({r['category'] for r in rows.values()})},
                'models': {name: {'artifact_id': rows[name]['artifact_id'], 'category': rows[name]['category'],
                                 'nodes': candidates[name]['nodes'], 'weight_bytes': rows[name]['weight_bytes'],
                                 'phase': phase} for name, phase in chosen}}
    (root / 'models-selected.yaml').write_text(yaml.safe_dump(manifest, sort_keys=False))
