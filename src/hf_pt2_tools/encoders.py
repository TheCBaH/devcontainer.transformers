"""Independently usable TinyCLIP tower components: image and text encoders with their own graphs, cases and captures."""
import copy
from pathlib import Path
import traceback

import torch
from transformers.exporters.exporter_dynamo import DynamoConfig, DynamoExporter

from .artifacts import write_json
from .generation import save_component
from .recipes import compare, make_inputs
from .registry import build_model, read_manifest, weight_provenance

MODELS = ('tinyclip',)


class ImageEncoder(torch.nn.Module):
    """Pixel values to unnormalized projected image features (CLIPModel.get_image_features)."""

    def __init__(self, model):
        super().__init__()
        self.vision_model, self.visual_projection = model.vision_model, model.visual_projection
        self.config = model.config

    def forward(self, pixel_values):
        return (self.visual_projection(self.vision_model(pixel_values=pixel_values).pooler_output),)


class TextEncoder(torch.nn.Module):
    """Token ids and mask to unnormalized projected text features (CLIPModel.get_text_features)."""

    def __init__(self, model):
        super().__init__()
        self.text_model, self.text_projection = model.text_model, model.text_projection
        self.config = model.config

    def forward(self, input_ids, attention_mask):
        return (self.text_projection(self.text_model(input_ids=input_ids, attention_mask=attention_mask).pooler_output),)


def run(root, output_root, name='tinyclip', population='tiny', snapshot=None, allow_unpinned=False):
    torch.set_num_threads(1)
    entry = next(e for e in read_manifest(root)['models'] if e['id'] == name)
    weights = weight_provenance(entry, snapshot, allow_unpinned)
    cap_mb = 64 if population == 'tiny' else entry.get('reference_max_weight_mb', read_manifest(root)['selection']['max_weight_mb'])
    model, config = build_model(root, entry, population, 'fp32', snapshot)
    result = {'schema_version': 1, 'model_id': name, 'status': 'failed', 'components': {}, 'population': population,
              'weights': weights}
    work = Path(output_root) / '.build/encoders'
    work.mkdir(parents=True, exist_ok=True)
    stage = 'inputs'
    try:
        with torch.no_grad():
            cases = [make_inputs(entry, config, population, seed=seed, root=root) for seed in (17, 29)]
            reference = [model(**copy.deepcopy(inputs)) for inputs in cases]
            for component, step, keys, field, embed in (
                    ('image-encoder', ImageEncoder(model).eval(), ('pixel_values',), 'image_features', 'image_embeds'),
                    ('text-encoder', TextEncoder(model).eval(), ('input_ids', 'attention_mask'), 'text_features', 'text_embeds')):
                stage = component
                entries = []
                for inputs, whole in zip(cases, reference, strict=True):
                    arguments = {key: inputs[key] for key in keys}
                    outputs = step(**copy.deepcopy(arguments))
                    normalized = outputs[0] / outputs[0].norm(dim=-1, keepdim=True)
                    torch.testing.assert_close(normalized, getattr(whole, embed), atol=1e-5, rtol=1e-4)
                    entries.append({'inputs': arguments, 'outputs': outputs})
                program = DynamoExporter().export(step, copy.deepcopy(entries[0]['inputs']), DynamoConfig(strict=False))
                program = program.run_decompositions(decomp_table={})
                for case in entries:
                    compare(program.module()(**copy.deepcopy(case['inputs'])), case['outputs'])
                result['components'][component] = save_component(
                    root, output_root, entry, config, component, program, entries, [field], weights=weights,
                    population=population, cap_mb=cap_mb)
            result['status'] = 'verified'
    except Exception as error:
        result['failed_stage'] = stage
        result['error_category'] = type(error).__name__
        (work / (stage + '.log')).write_text(traceback.format_exc())
    suffix = '' if population == 'tiny' and snapshot is None else f"-{population}{'-checkpoint' if snapshot else ''}"
    write_json(Path(output_root) / 'results/encoders' / (name + suffix + '.json'), result)
    return result
