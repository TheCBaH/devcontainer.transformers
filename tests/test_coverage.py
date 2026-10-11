import copy
from pathlib import Path

import pytest

from hf_pt2_tools.recipes import make_inputs, TensorOutputs
from hf_pt2_tools.registry import build_model, read_manifest, checkpoint_weight_bytes

ROOT = Path(__file__).resolve().parents[1]
MODELS = ('distilbert-base', 'roberta-base', 'albert-base', 'gpt2', 'bart-base',
          'vit-base', 'swin-tiny', 'dinov2-small', 'resnet-18', 'convnextv2-tiny',
          'minilm-l6-v2', 'mpnet-base', 'nomic-embed', 'qwen2-05b',
          'modernbert-embed', 'pythia-160m', 'ast-audioset', 'layoutlmv3-base',
          'sam-vit-base', 'owlv2-base', 'marian-fr-en', 'esm2-8m', 'mamba-130m',
          'clap-htsat', 'yolos-tiny', 'segformer-b0', 'depth-anything-small',
          'wav2vec2-base', 'smolvlm-256m')


@pytest.mark.parametrize('name', MODELS)
def test_checkpoint_budget_and_offline_tiny_recipe(name, monkeypatch):
    import torch
    import transformers

    def refuse_checkpoint(*args, **kwargs):
        raise AssertionError('architecture probes must not load checkpoints')

    entry = next(entry for entry in read_manifest(ROOT)['models'] if entry['id'] == name)
    monkeypatch.setattr(getattr(transformers, entry['model_class']), 'from_pretrained', refuse_checkpoint)
    assert 0 < checkpoint_weight_bytes(entry['reference']) < 1_000_000_000
    model, config = build_model(ROOT, entry)
    inputs = make_inputs(entry, config, root=ROOT)
    with torch.no_grad():
        outputs = TensorOutputs(model, entry['output_fields'])(**inputs)
    for value in outputs:
        assert isinstance(value, torch.Tensor) and torch.isfinite(value).all()


def test_sentence_pooling_masks_padding_and_normalizes():
    import torch
    from types import SimpleNamespace

    class Encoder(torch.nn.Module):
        config = SimpleNamespace()

        def forward(self, hidden, attention_mask):
            return SimpleNamespace(last_hidden_state=hidden)

    wrapper = TensorOutputs(Encoder(), ['sentence_embedding'])
    hidden = torch.tensor([[[6., 0.], [0., 8.], [1000., -1000.]]])
    mask = torch.tensor([[1, 1, 0]])
    actual, = wrapper(hidden=hidden, attention_mask=mask)
    torch.testing.assert_close(actual, torch.tensor([[0.6, 0.8]]))
    empty, = wrapper(hidden=hidden, attention_mask=torch.zeros_like(mask))
    assert torch.equal(empty, torch.zeros_like(empty))


def test_modernbert_graph_is_stable_across_caller_hash_seeds(tmp_path):
    import json
    import os
    import subprocess
    import sys

    graphs = []
    for seed in ('0', '1'):
        output = tmp_path / seed
        process = subprocess.run(
            [sys.executable, str(ROOT / 'scripts/worker.py'), 'worker', '--root', str(ROOT),
             '--output', str(output), '--subset', 'modernbert-embed'],
            env={**os.environ, 'PYTHONHASHSEED': seed, 'HF_HUB_OFFLINE': '1'},
            capture_output=True, text=True, timeout=180, check=True)
        result = json.loads(process.stdout.strip().splitlines()[-1])
        assert result['status'] == 'ok', result
        graphs.append((output / 'models' / result['artifact_id'] / 'models/model.json').read_bytes())
    assert graphs[0] == graphs[1]


@pytest.mark.parametrize('total,accepted', [(999_999_999, True), (1_000_000_000, False), (1_000_000_001, False)])
def test_budget_sums_shards_and_refuses_equality(total, accepted):
    sizes = [total // 2, total - total // 2]
    reference = {'safetensors_files': ['part-1.safetensors', 'part-2.safetensors'],
                 'safetensors_metadata': {f'part-{i + 1}.safetensors': {'size': size, 'sha256': 'a' * 64}
                                          for i, size in enumerate(sizes)},
                 'safetensors_total_bytes': total}
    if accepted:
        assert checkpoint_weight_bytes(reference) == total
    else:
        with pytest.raises(ValueError, match='less than 1 GB'):
            checkpoint_weight_bytes(reference)


def test_budget_refuses_missing_file_or_wrong_total():
    reference = copy.deepcopy(next(entry for entry in read_manifest(ROOT)['models']
                                  if entry['id'] == 'gpt2')['reference'])
    reference['safetensors_total_bytes'] += 1
    with pytest.raises(ValueError, match='total differs'):
        checkpoint_weight_bytes(reference)
    reference['safetensors_metadata'].clear()
    with pytest.raises(ValueError, match='inventory differs'):
        checkpoint_weight_bytes(reference)
