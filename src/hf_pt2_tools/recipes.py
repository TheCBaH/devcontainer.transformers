import json
from pathlib import Path

import torch


def specs(entry, config, population='tiny', batch=1, length=16):
    name = entry['id']
    tokens = {'input_ids': ('int64', [batch, length]),
              'attention_mask': ('int64', [batch, length])}
    if entry['model_class'].startswith('Bert'):
        return {**tokens, 'token_type_ids': ('int64', [batch, length])}
    if name == 'smollm2-135m':
        return tokens
    if name == 't5-small':
        return {**tokens, 'decoder_input_ids': ('int64', [batch, 4]),
                'decoder_attention_mask': ('int64', [batch, 4])}
    if name == 'mobilevit-xxs':
        return {'pixel_values': ('float32', [batch, 3, 256, 256])}
    if name == 'whisper-tiny':
        return {'input_features': ('float32', [batch, config.num_mel_bins, config.max_source_positions * 2]),
                'decoder_input_ids': ('int64', [batch, 4])}
    if name == 'tinyclip':
        return {**tokens, 'pixel_values': ('float32', [batch, 3, config.vision_config.image_size,
                                                    config.vision_config.image_size])}
    if name == 'videomae-small':
        return {'pixel_values': ('float32', [batch, config.num_frames, 3, config.image_size, config.image_size])}
    if name == 'time-series-small':
        past = config.context_length + max(config.lags_sequence)
        return {'past_values': ('float32', [batch, past]),
                'past_time_features': ('float32', [batch, past, config.num_time_features]),
                'past_observed_mask': ('float32', [batch, past]),
                'static_categorical_features': ('int64', [batch, 1]),
                'static_real_features': ('float32', [batch, 1]),
                'future_time_features': ('float32', [batch, config.prediction_length, config.num_time_features])}
    if name in ('yolos-tiny', 'segformer-b0', 'depth-anything-small'):
        return {'pixel_values': ('float32', [batch, 3, 224, 224])}
    if name == 'wav2vec2-base':
        return {'input_values': ('float32', [batch, 1024])}
    raise ValueError(f'no reviewed tensor recipe for {name}')


def make_inputs(entry, config, population='tiny', seed=17, batch=1, length=16, root=None):
    generator = torch.Generator().manual_seed(seed)
    if entry['id'] == 'smolvlm-256m':
        key = 'processor_fixture' if population == 'tiny' else 'reference_processor_fixture'
        fixture = json.loads((Path(root) / entry[key]).read_text())
        size = fixture['processor_overrides']['longest_edge']
        pixels = torch.randint(0, 256, (batch, 1, 3, size, size), generator=generator).float()
        pixels = pixels * fixture['pixel_recipe']['rescale']
        mean = torch.tensor(fixture['pixel_recipe']['mean']).view(1, 1, 3, 1, 1)
        std = torch.tensor(fixture['pixel_recipe']['std']).view(1, 1, 3, 1, 1)
        return {'input_ids': torch.tensor(fixture[population + '_input_ids']).expand(batch, -1).clone(),
                'attention_mask': torch.tensor(fixture['attention_mask']).expand(batch, -1).clone(),
                'pixel_values': (pixels - mean) / std,
                'pixel_attention_mask': torch.ones(batch, 1, size, size, dtype=torch.int64)}
    inputs = {}
    for name, (dtype, shape) in specs(entry, config, population, batch, length).items():
        if dtype == 'float32':
            value = torch.randn(shape, generator=generator)
            if 'observed_mask' in name:
                value = (value > -1).float()
            elif name == 'past_values':
                value = value.abs() + 0.5
            value = value.to(dtype=config.dtype or torch.float32)
        elif name.endswith('attention_mask'):
            value = torch.ones(shape, dtype=torch.int64)
            value[:, -1] = 0
        elif name == 'token_type_ids':
            value = torch.arange(shape[-1]).remainder(2).expand(shape).clone()
        elif name == 'static_categorical_features':
            value = torch.randint(0, config.cardinality[0], shape, generator=generator)
        else:
            vocab = config.text_config.vocab_size if hasattr(config, 'text_config') else config.vocab_size
            value = torch.randint(3, vocab, shape, generator=generator)
            if entry['id'] == 'tinyclip':
                value[:, -2] = config.text_config.eos_token_id
        inputs[name] = value
    return inputs


class TensorOutputs(torch.nn.Module):
    def __init__(self, model, fields):
        super().__init__()
        self.model = model
        self.config = model.config
        self.fields = tuple(fields)

    def forward(self, **kwargs):
        output = self.model(**kwargs)
        return tuple(getattr(output, field) for field in self.fields)


class AutocastTensorOutputs(TensorOutputs):
    def __init__(self, model, fields, dtype):
        super().__init__(model, fields)
        self.autocast_dtype = dtype

    def forward(self, **kwargs):
        with torch.autocast('cpu', dtype=self.autocast_dtype):
            return super().forward(**kwargs)


def tensor_metadata(inputs):
    return [{'name': name, 'dtype': str(tensor.dtype).removeprefix('torch.'),
             'shape': list(tensor.shape)} for name, tensor in inputs.items()]


def compare(actual, expected, dtype='fp32'):
    if not isinstance(actual, tuple) or len(actual) != len(expected):
        raise ValueError('output structure differs')
    atol, rtol = {'fp32': (1e-5, 1e-4), 'fp16': (5e-3, 5e-3), 'bf16': (5e-2, 5e-2)}[dtype]
    for left, right in zip(actual, expected, strict=True):
        if not isinstance(left, torch.Tensor) or left.dtype != right.dtype or left.shape != right.shape:
            raise ValueError('output shape/type differs')
        if not torch.isfinite(left).all() or not torch.isfinite(right).all():
            raise ValueError('nonfinite output')
        torch.testing.assert_close(left, right, atol=atol, rtol=rtol)
