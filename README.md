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
| `make clean` | Remove declared temporary outputs; keep committed graphs/configs |

Use `WORKERS=1` initially and `TIMEOUT=900` for per-artifact isolation. `SUBSET`
accepts comma-separated reviewed model IDs. The CLI supports separate output
roots, populations and experimental BERT/Llama dynamic shapes. Resume is opt-in
and invalidates on configuration, recipe, dependency, code or policy changes.
Random workers forbid network connections; fetching pretrained resources is a
separate later milestone.

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
loop. No-cache logits do not implement text/audio generation. Processor fixtures,
pretrained parameter binding, generation components and precision policies are
separate research milestones. The manual `research` workflow records reference
attempts and diagnostics without changing the committed tiny population.
