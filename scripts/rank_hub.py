"""Rank public Transformers checkpoints globally by Hugging Face downloads."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from catalogue_hub import assess_weights, pinned_architectures, retry, write_json


def inspect(candidate, api, download, architectures, cache):
    row = {'repo': candidate.id, 'revision': candidate.sha,
           'downloads': candidate.downloads or 0}
    if candidate.private or candidate.gated:
        return {**row, 'status': 'not-public'}
    if not candidate.sha:
        return {**row, 'status': 'missing-revision'}
    try:
        path = retry(lambda: download(candidate.id, 'config.json', revision=candidate.sha,
                                      cache_dir=cache, token=False))
    except Exception as error:
        if getattr(getattr(error, 'response', None), 'status_code', None) == 404:
            return {**row, 'status': 'missing-config'}
        raise
    raw = Path(path).read_bytes()
    config = json.loads(raw)
    architecture = config.get('model_type')
    row.update(architecture=architecture, model_classes=config.get('architectures', []),
               config_sha256=hashlib.sha256(raw).hexdigest())
    if architecture not in architectures:
        return {**row, 'status': 'unsupported-architecture'}
    info = retry(lambda: api.model_info(candidate.id, revision=candidate.sha,
                                       files_metadata=True, timeout=30), api=True)
    row.update(assess_weights(info), type=info.pipeline_tag or 'unspecified')
    if row['status'] == 'eligible' and 'model.safetensors.index.json' in {
            file.rfilename for file in info.siblings}:
        path = retry(lambda: download(candidate.id, 'model.safetensors.index.json',
                                      revision=candidate.sha, cache_dir=cache, token=False))
        raw = Path(path).read_bytes()
        required = set(json.loads(raw).get('weight_map', {}).values())
        if not required or not required <= row['safetensors_files'].keys():
            row['status'] = 'incomplete-shards'
        row['index_sha256'] = hashlib.sha256(raw).hexdigest()
    return row


def rankings(rows, count):
    ordered = sorted(rows, key=lambda row: (-row.get('downloads', 0), row['repo']))
    supported = [row for row in ordered if row.get('architecture') and
                 row['status'] not in ('unsupported-architecture', 'metadata-error')]
    return {'eligible': [row for row in supported if row['status'] == 'eligible'][:count],
            'overall': supported[:count]}


def render(document, mode):
    rows = document['rankings'][mode]
    lines = ['# Most downloaded Transformers checkpoints', '',
             f"Transformers {document['transformers_version']}; scanned {document['scanned_at']}.", '',
             'Global Hub downloads order, retaining multiple checkpoints per architecture. '
             'Public ungated repositories tagged with the Transformers library are considered; '
             'the pinned config model_type must be supported. Native graph export is not certified. '
             'Published test checkpoints and quantized weights are included. '
             'Downloads are the Hub rolling-window snapshot, not lifetime downloads. '
             'Configs and shard indices are downloaded; weights are not.', '',
             'Eligible means published full safetensors strictly below 1,000,000,000 bytes '
             'in total across the repository. The overall ranking also shows rejected sizes/formats.', '',
             f"Examined {len(document['checked'])} repositories; "
             f"scan status: {document['status']}. Metadata errors may leave gaps.", '',
             '| Rank | Checkpoint | Architecture | Task | Downloads | Safetensors bytes | Eligibility |',
             '| ---: | --- | --- | --- | ---: | ---: | --- |']
    for rank, row in enumerate(rows, 1):
        url = f"https://huggingface.co/{row['repo']}/tree/{row['revision']}"
        size = row.get('safetensors_total_bytes')
        size = f'{size:,}' if size is not None else 'unknown'
        lines.append(f"| {rank} | [{row['repo']}]({url}) | {row['architecture']} | "
                     f"{row.get('type', 'unspecified')} | {row['downloads']:,} | {size} | {row['status']} |")
    return '\n'.join(lines) + '\n'


def main():
    from huggingface_hub import HfApi, hf_hub_download

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--count', type=int, default=100)
    parser.add_argument('--candidates', type=int, default=5000)
    parser.add_argument('--output', type=Path, default=Path('hub-top100.json'))
    parser.add_argument('--cache', type=Path, default=Path('.build/hub-ranking-cache'))
    args = parser.parse_args()
    if args.count < 1 or args.candidates < args.count:
        parser.error('count must be positive and candidates must be at least count')
    version, architectures = pinned_architectures(args.root)
    api = HfApi(token=False)
    candidates = retry(lambda: list(api.list_models(
        filter='transformers', sort='downloads', limit=args.candidates,
        expand=['sha', 'downloads', 'gated', 'private'])), api=True)
    if any((left.downloads or 0) < (right.downloads or 0)
           for left, right in zip(candidates, candidates[1:])):
        raise ValueError('Hub did not return descending downloads order')
    rows = []
    document = {'schema_version': 1, 'transformers_version': version,
                'scope': {'library': 'transformers', 'candidate_limit': args.candidates,
                          'count': args.count, 'weights_downloaded': False,
                          'selection': 'global downloads order, multiple checkpoints per architecture'},
                'checked': rows}
    for candidate in candidates:
        try:
            row = inspect(candidate, api, hf_hub_download, architectures, args.cache)
        except Exception as error:
            row = {'repo': candidate.id, 'revision': candidate.sha,
                   'downloads': candidate.downloads or 0, 'status': 'metadata-error',
                   'error': f'{type(error).__name__}: {error}'[:300]}
        rows.append(row)
        document['rankings'] = rankings(rows, args.count)
        document['scanned_at'] = datetime.now(timezone.utc).isoformat()
        document['status'] = 'scanning'
        write_json(args.output, document)
        print(f"[{len(rows)}] {candidate.id}: {row['status']} "
              f"({len(document['rankings']['eligible'])}/{args.count} eligible)", flush=True)
        if all(len(values) == args.count for values in document['rankings'].values()):
            document['status'] = 'complete'
            break
    else:
        document['status'] = 'search-limit' if len(candidates) == args.candidates else 'exhausted'
    document['summary'] = dict(Counter(row['status'] for row in rows))
    write_json(args.output, document)
    for mode in document['rankings']:
        args.output.with_name(f'{args.output.stem}-{mode}.md').write_text(render(document, mode))
    return int(document['status'] != 'complete' or any(row['status'] == 'metadata-error' for row in rows))


if __name__ == '__main__':
    raise SystemExit(main())
