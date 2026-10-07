import hashlib
import json
from pathlib import Path

import yaml


CONFIG_CLASSES = {
    'BertModel': 'BertConfig',
    'BertForSequenceClassification': 'BertConfig',
    'BertForQuestionAnswering': 'BertConfig',
    'BertForTokenClassification': 'BertConfig',
    'BertForMaskedLM': 'BertConfig',
    'LlamaForCausalLM': 'LlamaConfig',
    'T5ForConditionalGeneration': 'T5Config',
    'MobileViTForImageClassification': 'MobileViTConfig',
    'WhisperForConditionalGeneration': 'WhisperConfig',
    'CLIPModel': 'CLIPConfig',
    'VideoMAEForVideoClassification': 'VideoMAEConfig',
    'TimeSeriesTransformerModel': 'TimeSeriesTransformerConfig',
    'YolosForObjectDetection': 'YolosConfig',
    'SegformerForSemanticSegmentation': 'SegformerConfig',
    'DepthAnythingForDepthEstimation': 'DepthAnythingConfig',
    'Wav2Vec2ForCTC': 'Wav2Vec2Config',
    'Idefics3ForConditionalGeneration': 'Idefics3Config',
}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     allow_nan=False).encode()).hexdigest()


def read_manifest(root):
    manifest = yaml.safe_load((Path(root) / 'model-candidates.yaml').read_text())
    if manifest['schema_version'] != 1:
        raise ValueError('unsupported manifest version')
    entries = manifest['models']
    ids = [e['id'] for e in entries]
    if len(ids) != len(set(ids)):
        raise ValueError('duplicate model ID')
    for entry in entries:
        if not entry['id'].replace('-', '').isalnum():
            raise ValueError('invalid model ID')
        if entry['model_class'] not in CONFIG_CLASSES:
            raise ValueError('unknown model/config pair')
        config_id = entry.get('config_model_id', entry['id'])
        if not config_id.replace('-', '').isalnum():
            raise ValueError('invalid configuration ID')
        reference = Path(root) / 'configs/reference' / (config_id + '.json')
        if hashlib.sha256(reference.read_bytes()).hexdigest() != entry['reference']['config_sha256']:
            raise ValueError(f"changed pinned config: {entry['id']}")
        for key in ('processor_fixture', 'reference_processor_fixture'):
            if not entry.get(key):
                continue
            fixture_path = Path(root) / entry[key]
            fixture = json.loads(fixture_path.read_text())
            source = fixture_path.parent / entry['id']
            for name, expected in fixture['source_sha256'].items():
                if hashlib.sha256((source / name).read_bytes()).hexdigest() != expected:
                    raise ValueError('processor source fixture hash mismatch')
    return manifest


def artifact_id(entry, population='tiny', dtype='fp32', policy='dynamo', shape='static', revision=None):
    if population not in ('tiny', 'reference') or dtype not in ('fp32', 'fp16', 'bf16'):
        raise ValueError('unknown population or dtype')
    if policy not in ('dynamo', 'direct', 'autocast') or shape not in ('static', 'dynamic'):
        raise ValueError('unknown export or shape policy')
    identity = f"{entry['id']}/{entry['category']}/{population}/forward/{dtype}/{policy}/{shape}"
    return identity if revision is None else f"{identity}/ckpt-{revision[:12]}"


RANDOM_WEIGHTS = {'kind': 'random', 'model_seed': 0}


def weight_provenance(entry, snapshot=None, allow_unpinned=False):
    """Weight source recorded in contracts, case manifests and results."""
    if snapshot is None:
        return dict(RANDOM_WEIGHTS)
    reference, snapshot = entry['reference'], Path(snapshot)
    if not reference['safetensors_files']:
        raise ValueError(f"{entry['id']}: no upstream safetensors at the pinned revision")
    config_hash = hashlib.sha256((snapshot / 'config.json').read_bytes()).hexdigest()
    if config_hash != reference['config_sha256'] and not allow_unpinned:
        raise ValueError('snapshot config differs from the pinned checkpoint')
    names = list(reference['safetensors_files'])
    if (snapshot / 'model.safetensors.index.json').exists():
        names.append('model.safetensors.index.json')
    files = {name: {'sha256': hashlib.sha256((snapshot / name).read_bytes()).hexdigest(),
                    'size': (snapshot / name).stat().st_size} for name in names}
    return {'kind': 'checkpoint', 'repo': reference['repo'], 'revision': reference['revision'],
            'config_sha256': config_hash, 'pinned_config_match': config_hash == reference['config_sha256'],
            'files': files, 'conversion': 'transformers from_pretrained, explicit dtype cast to the artifact dtype'}


def build_model(root, entry, population='tiny', dtype='fp32', snapshot=None):
    import torch
    import transformers

    config_path = Path(root) / 'configs' / population / (entry.get('config_model_id', entry['id']) + '.json')
    document = json.loads(config_path.read_text())
    config = getattr(transformers, CONFIG_CLASSES[entry['model_class']]).from_dict(document)
    config.use_cache = False
    if hasattr(config, 'text_config'):
        config.text_config.use_cache = False
    config.return_dict = True
    config.output_attentions = False
    config.output_hidden_states = False
    config._attn_implementation = 'eager'
    torch.manual_seed(0)
    if snapshot is None:
        model = getattr(transformers, entry['model_class'])(config).eval()
    else:
        model = getattr(transformers, entry['model_class']).from_pretrained(
            snapshot, config=config, local_files_only=True, use_safetensors=True,
            dtype=torch.float32, attn_implementation='eager').eval()
    model.to(dtype={'fp32': torch.float32, 'fp16': torch.float16, 'bf16': torch.bfloat16}[dtype])
    return model, config
