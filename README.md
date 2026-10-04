# Devcontainer for HuggingFace Transformers library

[![Transformers devcontainer](https://github.com/TheCBaH/devcontainer.transformers/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/TheCBaH/devcontainer.transformers/actions/workflows/build.yml)

Offline architecture research for [Transformers](https://github.com/huggingface/transformers),
with reproducible CPU environments and verified functional PT2 graphs. Eight tiny
random-weight probes cover BERT, Llama, T5, MobileViT, Whisper, CLIP, VideoMAE and
time-series states. Original checkpoint configurations have separate identities;
these graphs do not contain pretrained checkpoint weights or establish accuracy.

## Get started
* [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=master&repo=950664099)
* Open this repository in its devcontainer, then run `make setup` and `make smoke`.
  The default `make` runs only the small offline BERT check.

The frozen baseline is Python 3.13.12, uv 0.12.23, Transformers 5.18.0,
torch 2.12.0+cpu and torchvision 0.27.0+cpu. CPU wheels exist for ARM64 and
x86-64. Committed graphs use ARM64 CPU; both uv and devcontainer CI regenerate
them on `ubuntu-24.04-arm`. The x86 job verifies its own BERT execution.
The shared `pt2-export-core` is installed from a pinned Git subdirectory;
no sibling checkout is required. Its initial Git fetch/cache measured 524 MiB.

| Command | Purpose |
| --- | --- |
| `make test` | Semantic, dynamic-shape, isolation, corruption and publication regressions |
| `make report` | Run the eight tiny probes; render structured results and three operator matrices |
| `make models.select` | Select verified artifacts from existing results, with category representatives |
| `make models` | Independently regenerate functional graph JSON, facts and contracts |
| `make models.verify` | Check graph hashes, operator facts and saved call contracts |
| `make check-tree-clean` | Reject generated drift and unexpected files |
| `make research.reference SUBSET=bert-tiny` | Explicit original-config random-weight experiment |
| `make models.fetch SUBSET=t5-small` | Fetch only the pinned config and safetensors for one model |
| `make models.weights.verify SUBSET=t5-small GRAPH=<reference-model.json>` | Verify checkpoint bindings against the library load |
| `make models.generation SUBSET=smollm2-135m` | Verify prefill/decode, tensor cache state, reset and capacity |
| `make models.precision.fp16` / `make models.precision.bf16` | Separate cast/autocast probes for BERT, MobileViT and Llama |
| `make clean` | Remove declared temporary outputs; keep committed graphs/configs |

Use `WORKERS=1` initially and `TIMEOUT=900` for per-artifact isolation. `SUBSET`
accepts comma-separated reviewed model IDs. The CLI supports separate output
roots, populations and experimental BERT/Llama dynamic shapes. Resume is opt-in
and invalidates on configuration, recipe, dependency, code or policy changes.
Random workers forbid network connections. `models.fetch` explicitly enables
downloads for one immutable checkpoint; binding then uses the local cache only.

[`models.md`](models.md) and `ops-{aten,func,core-cpu}.{yaml,md}` are rendered
from [`results/models.json`](results/models.json), which records each pipeline
stage independently. Empty-table functionalization supplies the published
graphs; default decomposition is separately executed and compared. FLOPs are
not measured. Computational reports omit serializer bookkeeping assertions;
`op_facts.json` retains exact saved graph counts and hash-bound configurations.

Each `models/<model>/<task>/<population>/forward/<dtype>/<policy>/<shape>/`
directory contains the unmodified serializer JSON, weight/constant metadata,
operator facts and a versioned tensor contract. Archives and example tensors
stay under ignored `.build/`. Every artifact is compared against eager output
for two input seeds and loaded/executed in a fresh process importing only torch.
Output boundaries are ordered tensor tuples, with mixed input dtypes retained.

Time-series graphs expose states, location and scale, not a full forecasting
loop. The eight core graphs expose no-cache forward outputs. Separate generation
artifacts cover Llama, T5 and Whisper encoder/prefill/decode, and Idefics3
vision/connector/language prefill/decode. Inputs and returned self/cross-attention
K/V tensors are plain tensors. The host feeds state into successive calls and
owns sampling and stopping. Checks compare greedy tokens, logits and all cache
tensors over five or six successive steps, reset state, and reject history
beyond the declared bound. Every component loads with torch alone. Upstream
`export_for_generation` capability results are recorded separately from these
verified adapters.

The extended pool covers detection, segmentation, depth, waveform CTC and
processor-derived image/text generation. Four additional BERT task heads cover
sequence classification, QA, token classification and masked LM with random
weights. Explicit `hf-pt2 research --subset ... --output .build/<experiment>`
runs these independently. Default reports and selection remain the eight core
tiny models. Original configs have distinct reference IDs; all thirteen were
verified locally. Their default weight cap is 768 MiB; the full FP32 Idefics3
reference explicitly allows 1536 MiB. Its original-resolution fixture uses 512px
images and 64 image tokens; the tiny fixture uses 32px and four image tokens.
Both derive from hashed, pinned processor/tokenizer files and disable image
splitting for this one-image probe.
Dense-vision reference results use the reviewed 224px structural inputs listed
in the manifest. SmolLM2-135M's functional reference graph is verified; its
default decomposition has a version-scoped numeric exclusion at the fixed FP32
tolerance. The tiny SmolLM2 probe passes all stages.

`checkpoint-maps/` records exact source-file and loaded-value hashes, key
renaming, shard indices, tied aliases and explicit FP32 conversion. Ten source
checkpoints have verified mappings. BERT, MobileViT and VideoMAE lack upstream
safetensors at their pins. Wav2Vec2's missing training-only mask embedding is
recorded as an unused graph input; it is never assigned a fabricated binding.
Maps bind original-config graphs and do not turn the tiny random corpus into
pretrained models or establish accuracy.

Precision evidence covers three representatives on ARM64 CPU: FP16/BF16 direct
casts and CPU autocast are distinct policies and artifacts. Each uses a fresh
model, retains integer/mask types and compares with its own eager reference;
FP16 tolerances are 0.005 and BF16 tolerances are 0.05. This twelve-case subset
does not imply whole-library or cross-architecture precision support.

`export-exclusions.yaml` scopes reviewed failures by artifact, stage, policy and
exact package/core versions, with a reason. New stage failures and stale
exclusions fail the command while preserving any successful functional graph.
The manual `research` workflow uploads reference/extended evidence and diagnostics
without changing the committed tiny population. Archives are research work
files; this repository does not publish a release payload yet.
