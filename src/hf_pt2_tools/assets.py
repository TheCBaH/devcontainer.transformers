"""Pinned processor/tokenizer assets and tensor-level input recipes, with one raw-input-to-tensor example per family."""
import json
from pathlib import Path

import numpy as np
import torch

from .artifacts import file_hash, write_json
from .fixtures import tensor_digest
from .registry import read_manifest

ASSET_PATTERNS = ['config.json', 'preprocessor_config.json', 'processor_config.json', 'video_preprocessor_config.json',
                  'tokenizer.json', 'tokenizer_config.json', 'special_tokens_map.json', 'added_tokens.json',
                  'vocab.json', 'vocab.txt', 'merges.txt', 'spiece.model', 'normalizer.json',
                  'generation_config.json', 'chat_template.json', 'chat_template.jinja']
IMAGE_KEYS = ('do_resize', 'size', 'resample', 'do_center_crop', 'crop_size', 'do_rescale', 'rescale_factor',
              'do_normalize', 'image_mean', 'image_std', 'do_pad', 'size_divisor', 'do_flip_channel_order',
              'keep_aspect_ratio', 'ensure_multiple_of', 'do_reduce_labels', 'format', 'num_frames',
              'do_image_splitting', 'max_image_size', 'do_convert_rgb')
AUDIO_KEYS = ('feature_size', 'sampling_rate', 'padding_value', 'return_attention_mask', 'do_normalize',
              'n_fft', 'hop_length', 'chunk_length', 'n_samples', 'nb_max_frames', 'dither')
GENERATION_KEYS = ('bos_token_id', 'eos_token_id', 'pad_token_id', 'decoder_start_token_id', 'max_length',
                   'max_new_tokens', 'do_sample', 'forced_decoder_ids', 'suppress_tokens', 'begin_suppress_tokens')
FAMILIES = {'bert-tiny': 'text', 'smollm2-135m': 'text', 't5-small': 'text', 'mobilevit-xxs': 'image',
            'whisper-tiny': 'audio', 'tinyclip': 'image-text', 'videomae-small': 'video',
            'time-series-small': 'tensor-only', 'yolos-tiny': 'image', 'segformer-b0': 'image',
            'depth-anything-small': 'image', 'wav2vec2-base': 'audio', 'smolvlm-256m': 'image-text-chat'}
TEXT = 'The quick brown fox jumps over the lazy dog.'


def raw_image(seed=3, size=(96, 128)):
    return np.random.RandomState(seed).randint(0, 256, (*size, 3), dtype=np.uint8)


def raw_audio(rate, seed=5, seconds=1):
    return np.random.RandomState(seed).uniform(-0.5, 0.5, rate * seconds).astype(np.float32)


def _subset(path, keys):
    document = json.loads(Path(path).read_text())
    return {key: document[key] for key in keys if key in document}


# config.json is pinned by the registry; it is downloaded for the Auto* classes but stays a model asset, not a recipe.
def describe_files(snapshot, repo, revision):
    """Digest every downloaded asset; URLs are revision-pinned Hub resolve links."""
    snapshot = Path(snapshot)
    if not snapshot.exists():
        return {}
    return {path.name: {'sha256': file_hash(path), 'size': path.stat().st_size,
                        'url': f'https://huggingface.co/{repo}/resolve/{revision}/{path.name}'}
            for path in sorted(snapshot.iterdir()) if path.is_file() or path.is_symlink()}


def tensors_record(tensors):
    return {name: {'dtype': str(t.dtype).removeprefix('torch.'), 'shape': list(t.shape), 'sha256': tensor_digest({name: t})}
            for name, t in tensors.items()}


def text_recipe(snapshot):
    import transformers
    try:
        tokenizer = transformers.AutoTokenizer.from_pretrained(snapshot, local_files_only=True)
    except Exception:
        if not (Path(snapshot) / 'vocab.txt').exists():
            raise
        tokenizer = transformers.BertTokenizer.from_pretrained(snapshot, local_files_only=True)
    specials = {name: {'token': str(token), 'id': tokenizer.convert_tokens_to_ids(str(token))}
                for name, token in tokenizer.special_tokens_map.items() if isinstance(token, str)}
    recipe = {'special_tokens': specials, 'model_max_length': tokenizer.model_max_length,
              'padding_side': tokenizer.padding_side, 'truncation_side': tokenizer.truncation_side,
              'vocab_size': len(tokenizer)}
    encoded = tokenizer(TEXT, return_tensors='pt')
    return recipe, {'raw': {'kind': 'text', 'value': TEXT}, 'tensors': tensors_record(dict(encoded)),
                    'decoded': tokenizer.decode(encoded['input_ids'][0])}


def image_recipe(snapshot, family, files):
    from transformers import AutoImageProcessor
    config = 'video_preprocessor_config.json' if 'video_preprocessor_config.json' in files else 'preprocessor_config.json'
    recipe = {'preprocessor': _subset(Path(snapshot) / config, IMAGE_KEYS)}
    processor = AutoImageProcessor.from_pretrained(snapshot, local_files_only=True)
    if family == 'video':
        frames = [raw_image(seed) for seed in range(recipe['preprocessor'].get('num_frames') or 16)]
        out = processor(frames, return_tensors='pt')
        raw = {'kind': 'video', 'frames': len(frames), 'seeded_uint8_hwc': [96, 128, 3], 'seeds': list(range(len(frames)))}
    else:
        out = processor(raw_image(), return_tensors='pt')
        raw = {'kind': 'image', 'seeded_uint8_hwc': [96, 128, 3], 'seed': 3}
    return recipe, {'raw': raw, 'tensors': tensors_record(dict(out))}


def audio_recipe(snapshot):
    from transformers import AutoFeatureExtractor
    extractor = AutoFeatureExtractor.from_pretrained(snapshot, local_files_only=True)
    recipe = {'preprocessor': _subset(Path(snapshot) / 'preprocessor_config.json', AUDIO_KEYS)}
    rate = extractor.sampling_rate
    out = extractor(raw_audio(rate), sampling_rate=rate, return_tensors='pt')
    return recipe, {'raw': {'kind': 'audio', 'sampling_rate': rate, 'seconds': 1, 'seed': 5, 'uniform': [-0.5, 0.5]},
                    'tensors': tensors_record(dict(out))}


def describe_model(entry, snapshot, root):
    """Assets, recipe and example for one pinned model; every failure is recorded, not hidden."""
    name, reference = entry['id'], entry['reference']
    family = FAMILIES[name]
    files = describe_files(snapshot, reference['repo'], reference['revision'])
    record = {'model_id': name, 'family': family, 'repo': reference['repo'], 'revision': reference['revision'],
              'files': files, 'recipe': {}, 'example': {}}
    generation = Path(snapshot) / 'generation_config.json'
    if generation.exists():
        record['recipe']['generation'] = _subset(generation, GENERATION_KEYS)
    steps = []
    if family in ('text', 'image-text', 'image-text-chat') and any(f in files for f in ('tokenizer.json', 'tokenizer_config.json', 'vocab.txt', 'spiece.model')):
        steps.append(('text', lambda: text_recipe(snapshot)))
    if family in ('image', 'video', 'image-text') and 'preprocessor_config.json' in files:
        steps.append(('image', lambda: image_recipe(snapshot, 'video' if family == 'video' else 'image', files)))
    if family == 'image-text-chat':
        fixture = Path(root) / entry['processor_fixture']
        record['recipe']['processor_fixture'] = {'path': entry['processor_fixture'], 'sha256': file_hash(fixture)}
        if 'preprocessor_config.json' in files:
            record['recipe']['image_preprocessor'] = _subset(Path(snapshot) / 'preprocessor_config.json', IMAGE_KEYS)
    if family == 'audio':
        steps.append(('audio', lambda: audio_recipe(snapshot)))
        if 'tokenizer.json' in files or 'vocab.json' in files:
            steps.append(('tokenizer', lambda: text_recipe(snapshot)))
    if family == 'tensor-only':
        record['example'] = {'tensor-only': {'status': 'no processor: callers build past/future value and time-feature tensors directly'}}
    config = json.loads((Path(snapshot) / 'config.json').read_text()) if 'config.json' in files else {}
    if config.get('id2label'):
        record['recipe']['output_decoding'] = {'config_file': 'config.json', 'num_labels': len(config['id2label'])}
    for kind, build in steps:
        try:
            recipe, example = build()
            record['recipe'][kind] = recipe
            record['example'][kind] = example
        except Exception as error:
            record['example'][kind] = {'status': 'failed', 'error_category': type(error).__name__, 'error': str(error)[:300]}
    return record


def input_agreement(record, entry):
    """Compare processor output tensors with the model's pinned original-size input contract (informational)."""
    inputs = entry.get('reference_inputs') or {}
    agreement = {}
    for kind, example in record['example'].items():
        for name, tensor in example.get('tensors', {}).items() if kind != 'tokenizer' else ():
            if name in inputs:
                agreement[name] = {'dtype_matches': inputs[name]['dtype'] == tensor['dtype'],
                                   'rank_matches': len(inputs[name]['shape']) == len(tensor['shape']),
                                   'shape_matches': list(inputs[name]['shape']) == tensor['shape'],
                                   'model_shape': list(inputs[name]['shape']), 'processor_shape': tensor['shape']}
    return agreement


def build_assets(root, output, models=None):
    from huggingface_hub import snapshot_download
    import importlib.metadata
    root = Path(root)
    seen, rows = set(), []
    for entry in read_manifest(root)['models']:
        reference = entry['reference']
        key = (reference['repo'], reference['revision'])
        if entry['id'] not in FAMILIES or key in seen or (models and entry['id'] not in models):
            continue
        seen.add(key)
        snapshot = snapshot_download(reference['repo'], revision=reference['revision'], cache_dir=root / '.hf-cache',
                                     allow_patterns=ASSET_PATTERNS)
        record = describe_model(entry, snapshot, root)
        record['input_agreement'] = input_agreement(record, entry)
        rows.append(record)
    document = {'schema_version': 1,
                'versions': {n: importlib.metadata.version(n) for n in ('transformers', 'torch', 'numpy', 'tokenizers')},
                'scope': 'pinned processor/tokenizer assets and tensor-level recipes; raw-media decoding is not covered',
                'models': rows}
    write_json(output, document)
    return document
