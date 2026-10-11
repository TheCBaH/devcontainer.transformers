"""Find a published safetensors checkpoint for every pinned Transformers architecture."""
import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import re
import threading
import time
import tomllib

LIMIT = 1_000_000_000
DTYPE_BYTES = {'F64': 8, 'F32': 4, 'F16': 2, 'BF16': 2, 'I64': 8, 'I32': 4,
               'I16': 2, 'I8': 1, 'U8': 1, 'BOOL': 1, 'F8_E4M3': 1, 'F8_E5M2': 1}
REQUEST_INTERVAL = 60 / 90
REQUEST_LOCK = threading.Lock()
LAST_REQUEST = 0
API_NOT_BEFORE = 0


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def assess_weights(info, limit=LIMIT):
    siblings = {file.rfilename: file for file in info.siblings or []}
    files = {name: file for name, file in siblings.items() if name.endswith('.safetensors')}
    if not files:
        return {'status': 'no-safetensors'}
    if 'model.safetensors' not in files and 'model.safetensors.index.json' not in siblings:
        return {'status': 'no-full-checkpoint'}
    if any(type(file.size) is not int or file.size <= 0 for file in files.values()):
        return {'status': 'unknown-file-sizes'}
    total = sum(file.size for file in files.values())
    if total >= limit:
        return {'status': 'too-large', 'safetensors_total_bytes': total}
    metadata = {}
    for name, file in sorted(files.items()):
        lfs = file.lfs
        metadata[name] = {'size': file.size, 'sha256': getattr(lfs, 'sha256', None),
                          'git_oid': file.blob_id}
    return {'status': 'eligible', 'safetensors_total_bytes': total, 'safetensors_files': metadata}


def minimum_weight_bytes(info):
    parameters = getattr(getattr(info, 'safetensors', None), 'parameters', {}) or {}
    return sum(count * DTYPE_BYTES.get(dtype, 0) for dtype, count in parameters.items()
               if type(count) is int and count > 0)


def pace():
    global LAST_REQUEST
    with REQUEST_LOCK:
        delay = max(LAST_REQUEST + REQUEST_INTERVAL, API_NOT_BEFORE) - time.monotonic()
        if delay > 0:
            time.sleep(delay)
        LAST_REQUEST = time.monotonic()


def retry(call, api=False):
    global API_NOT_BEFORE
    for attempt in range(5):
        try:
            if api:
                pace()
            return call()
        except Exception as error:
            response = getattr(error, 'response', None)
            status = getattr(response, 'status_code', None)
            if status not in (429, 500, 502, 503, 504) or attempt == 4:
                raise
            delay = 2 ** (attempt + 2)
            header = response.headers.get('Retry-After', '')
            if header.isdigit():
                delay = max(delay, int(header) + 2)
            else:
                match = re.search(r'Retry after (\d+) seconds', str(error))
                if match:
                    delay = max(delay, int(match[1]) + 2)
            if api and status == 429:
                with REQUEST_LOCK:
                    API_NOT_BEFORE = max(API_NOT_BEFORE, time.monotonic() + delay)
            time.sleep(delay)


def pinned_architectures(root):
    from transformers.models.auto.configuration_auto import CONFIG_MAPPING_NAMES

    version = importlib.metadata.version('transformers')
    dependencies = tomllib.loads((root / 'pyproject.toml').read_text())['project']['dependencies']
    if f'transformers=={version}' not in dependencies:
        raise ValueError('installed Transformers differs from the repository pin; use uv run --frozen')
    return version, dict(CONFIG_MAPPING_NAMES)


def scan_architecture(architecture, config_class, args):
    from huggingface_hub import HfApi, hf_hub_download

    api = HfApi(token=False)
    checked = []
    cache = Path(args.cache) / 'architectures' / f'{architecture}.json'
    if cache.exists() and not args.refresh:
        result = json.loads(cache.read_text())
        if (result.get('candidate_limit') == args.candidates and result.get('config_class') == config_class
                and result.get('status') not in ('query-error', 'metadata-error')):
            return result
    result = {'architecture': architecture, 'config_class': config_class,
              'candidate_limit': args.candidates, 'checked': checked}
    try:
        candidates = retry(lambda: list(api.list_models(
            filter=(architecture, 'safetensors'), sort='downloads', limit=args.candidates,
            expand=['config', 'sha', 'safetensors', 'downloads', 'gated', 'private', 'pipeline_tag'])), api=True)
        result['candidates_returned'] = len(candidates)
        for candidate in candidates:
            row = {'repo': candidate.id, 'revision': candidate.sha}
            checked.append(row)
            if candidate.private or candidate.gated:
                row['status'] = 'not-public'
                continue
            if not candidate.sha:
                row['status'] = 'missing-revision'
                continue
            minimum = minimum_weight_bytes(candidate)
            if minimum >= LIMIT:
                row.update(status='too-large', minimum_safetensors_bytes=minimum)
                continue
            try:
                info = retry(lambda: api.model_info(candidate.id, revision=candidate.sha,
                                                    files_metadata=True, timeout=30), api=True)
                row.update(assess_weights(info))
                if row['status'] != 'eligible':
                    continue
                if 'config.json' not in {file.rfilename for file in info.siblings}:
                    row['status'] = 'missing-config'
                    continue

                def read_json(filename):
                    path = retry(lambda: hf_hub_download(candidate.id, filename, revision=candidate.sha,
                                                        cache_dir=Path(args.cache) / 'hub', token=False))
                    raw = Path(path).read_bytes()
                    return json.loads(raw), hashlib.sha256(raw).hexdigest()

                config, config_hash = read_json('config.json')
                if config.get('model_type') != architecture:
                    row['status'] = 'different-architecture'
                    row['reported_architecture'] = config.get('model_type')
                    continue
                if 'model.safetensors.index.json' in {file.rfilename for file in info.siblings}:
                    index, index_hash = read_json('model.safetensors.index.json')
                    required = set(index.get('weight_map', {}).values())
                    if not required or not required <= row['safetensors_files'].keys():
                        row['status'] = 'incomplete-shards'
                        continue
                    row['index_sha256'] = index_hash
                row.update(type=info.pipeline_tag or 'unspecified',
                           model_classes=config.get('architectures', []), config_sha256=config_hash,
                           config_url=f'https://huggingface.co/{candidate.id}/resolve/{candidate.sha}/config.json',
                           downloads=candidate.downloads or 0,
                           weights_url=f'https://huggingface.co/{candidate.id}/tree/{candidate.sha}')
                result['checkpoint'] = dict(row)
                result['status'] = 'eligible'
                break
            except Exception as error:
                row['status'] = 'metadata-error'
                row['error'] = f'{type(error).__name__}: {error}'[:300]
        else:
            if any(row['status'] == 'metadata-error' for row in checked):
                result['status'] = 'metadata-error'
            elif len(candidates) == args.candidates:
                result['status'] = 'search-limit'
            else:
                result['status'] = 'no-qualifying-checkpoint'
    except Exception as error:
        result.update(status='query-error', error=f'{type(error).__name__}: {error}'[:300])
    result['scanned_at'] = datetime.now(timezone.utc).isoformat()
    write_json(cache, result)
    return result


def catalogue(version, architectures, rows, candidate_limit):
    groups = defaultdict(dict)
    for architecture, row in sorted(rows.items()):
        if row['status'] == 'eligible':
            checkpoint = row['checkpoint']
            groups[checkpoint['type']][architecture] = checkpoint
    return {'schema_version': 1, 'transformers_version': version,
            'scanned_at': datetime.now(timezone.utc).isoformat(),
            'criteria': {'safetensors_total_bytes_exclusive': LIMIT, 'published_full_checkpoint': True,
                         'public_ungated': True, 'count_all_repository_safetensors': True},
            'scope': {'architectures': len(architectures), 'candidate_limit_per_architecture': candidate_limit,
                      'selection': 'first qualifying checkpoint in Hub downloads order; architecture-tag search',
                      'weights_downloaded': False},
            'summary': dict(sorted(Counter(row['status'] for row in rows.values()).items())),
            'types': dict(sorted(groups.items())), 'architectures': dict(sorted(rows.items()))}


def render(document):
    lines = ['# Hugging Face checkpoint catalogue', '',
             f"Transformers {document['transformers_version']}; scanned {document['scanned_at']}.", '',
             'Every included checkpoint has published full safetensors weights totaling strictly less than '
             '1,000,000,000 bytes across the entire repository. Configs and shard indices were downloaded; weights were not.', '',
             f"All {document['scope']['architectures']} pinned AutoConfig architectures are considered. "
             f"Search examines up to {document['scope']['candidate_limit_per_architecture']} checkpoints per architecture, "
             'ordered by Hub downloads, and stops at the first qualifying checkpoint. '
             'Discovery uses architecture tags. Untagged checkpoints and private/gated repositories are outside this scan. '
             'A search limit or missing candidate is not proof that no qualifying checkpoint exists. '
             'Published tiny random test checkpoints and quantized checkpoints are included. '
             'Task type comes from Hub pipeline metadata; absent metadata is unspecified. '
             'Eligibility does not establish graph-export support or pretrained quality.', '',
             '| Scan result | Architectures |', '| --- | ---: |']
    for status, count in document['summary'].items():
        lines.append(f'| {status} | {count} |')
    for kind, models in document['types'].items():
        lines += ['', f'## {kind}', '', '| Architecture | Checkpoint | Model classes | Safetensors bytes |',
                  '| --- | --- | --- | ---: |']
        for architecture, checkpoint in models.items():
            classes = ', '.join(checkpoint['model_classes']) or 'unspecified'
            lines.append(f"| {architecture} | [{checkpoint['repo']}]({checkpoint['weights_url']}) | "
                         f"{classes} | {checkpoint['safetensors_total_bytes']:,} |")
    lines += ['', '## Architecture scan inventory', '',
              '| Architecture | Config class | Result | Candidates checked |', '| --- | --- | --- | ---: |']
    for architecture, row in document['architectures'].items():
        lines.append(f"| {architecture} | {row['config_class']} | {row['status']} | {len(row['checked'])} |")
    return '\n'.join(lines) + '\n'


def main():
    global REQUEST_INTERVAL
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path, default=Path('hub-catalogue.json'))
    parser.add_argument('--cache', default='.build/hub-catalogue-cache')
    parser.add_argument('--candidates', type=int, default=100)
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--requests-per-minute', type=int, default=90)
    parser.add_argument('--subset', help='Comma-separated architecture model_type values')
    parser.add_argument('--refresh', action='store_true')
    args = parser.parse_args()
    if args.candidates < 1 or not 1 <= args.workers <= 8 or args.requests_per_minute < 1:
        parser.error('candidates/rate must be positive and workers must be between 1 and 8')
    REQUEST_INTERVAL = 60 / args.requests_per_minute
    version, architectures = pinned_architectures(args.root)
    if args.subset:
        names = set(args.subset.split(','))
        if names - architectures.keys():
            parser.error(f'unknown architectures: {sorted(names - architectures.keys())}')
        architectures = {name: config for name, config in architectures.items() if name in names}
    args.cache = str(Path(args.cache) / version)
    rows = {}
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(scan_architecture, name, config, args): name
                   for name, config in sorted(architectures.items())}
        for future in as_completed(futures):
            name = futures[future]
            rows[name] = future.result()
            print(f"[{len(rows)}/{len(architectures)}] {name}: {rows[name]['status']}", flush=True)
    document = catalogue(version, architectures, rows, args.candidates)
    write_json(args.output, document)
    args.output.with_suffix('.md').write_text(render(document))
    print(json.dumps(document['summary'], sort_keys=True))
    return int(any(row['status'] in ('query-error', 'metadata-error') for row in rows.values()))


if __name__ == '__main__':
    raise SystemExit(main())
