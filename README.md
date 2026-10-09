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
The shared `pt2-export-core` is an editable path dependency on the
`modules/devcontainer.pytorch-image-models` submodule (tracks `main`;
Dependabot bumps the pointer). Initialize it non-recursively:
`git submodule update --init --depth 1`.
Update torch/torchvision together and rerun corpus validation. Their automatic
updates are excluded because Dependabot's uv updater resolves one pin at a time,
including inside a dependency group.

| Command | Purpose |
| --- | --- |
| `make test` | Semantic, dynamic-shape, isolation, corruption and publication regressions |
| `make report` | Run the eight tiny probes; render structured results and three operator matrices |
| `make report.symbolic` | Inspect saved graphs; report symbolic shapes/scalars and affected nodes across model artifacts |
| `make models.select` | Select verified artifacts from existing results, with category representatives |
| `make models` | Independently regenerate functional graph JSON, facts and contracts |
| `make models.verify` | Check graph hashes, operator facts and saved call contracts |
| `make check-tree-clean` | Reject generated drift and unexpected files |
| `make research.reference SUBSET=bert-tiny` | Explicit original-config random-weight experiment |
| `make models.fetch SUBSET=t5-small` | Fetch only the pinned config and safetensors for one model |
| `make models.weights.verify SUBSET=t5-small GRAPH=<reference-model.json>` | Verify checkpoint bindings against the library load |
| `make models.generation SUBSET=smollm2-135m` | Verify prefill/decode, tensor cache state, reset and capacity |
| `make models.precision.fp16` / `make models.precision.bf16` | Separate cast/autocast probes for BERT, MobileViT and Llama |
| `make catalogue` | Rewrite `catalogue.json`: graph-only index of every artifact with weight source and case digests |
| `make bundles` / `make bundles.verify` | Pack each artifact with `model.pt2` and flat case tensors; replay with torch only |
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

Operator configurations preserve fixed arguments exactly, including constants
whose schema type is `SymInt`. Only genuinely symbolic integers appear as
`SymInt` in Markdown and `{$symint: true}` in YAML/JSON. Mixed size lists retain
their fixed entries, such as `[1,SymInt,64]`. Symbol expressions and range bounds
remain in the exported graph and tensor contract. Coverage distinguishes fixed
argument values across graphs; it groups symbolic arguments by this marker.

[`symbolic-shapes.md`](symbolic-shapes.md) covers every saved functional artifact,
including prefill and dynamic decode. It links operators to model artifacts and
shows graph-local symbols, declared bounds and expandable per-node tensor shapes
and named argument configurations, resolving symbolic scalars to expressions
while preserving fixed settings and complete mixed lists such as
`size=[1,4,(s15+1),16]`. Operations using symbolically shaped tensors
are included even when they have no explicit SymInt argument. Export hints do
not determine actual sizes. Regenerate with `make report.symbolic`; it reads JSON
and checks graph hashes without loading models or importing torch. The manual
research workflow's `report_only` mode generates this report and runs its focused
regressions without building the export environment.

**Fixtures, captures and weights.** Every artifact carries `cases.json` (named
input/output order and content digests of flat `cases/<id>/{inputs,outputs}.pt`
`dict[str, Tensor]` files), `captures.json` (every `PARAMETER`, `BUFFER` and
`CONSTANT_TENSOR` with payload-config name, dtype, shape, liveness and
graph-owned value digest), and a `weights` record in its contract: `random`
(seed 0) or a pinned `checkpoint` (repo, revision, file digests and sizes).
Checkpoint-backed artifacts add `/ckpt-<revision[:12]>` to the ID, so they can
never overwrite random-weight ones. `hf-pt2 bundle` packs graph, `model.pt2` and
case tensors reproducibly; `bundle-verify` extracts, checks every hash and
replays all cases with torch only. `bind` records, per capture, a checkpoint
source (file, key, dtype, conversion, aliases) or a graph-owned payload digest,
and `unmapped` means a live capture without a source. `hf-pt2 pack` emits the
captured-value safetensors file plus the version-1 `safetensors.json` map for
mltorch and checks it as the consumer would. `pack --artifact <id>` names the
files after the full artifact ID (components of one model would otherwise
collide) and `--graph` rejects a binding made for another graph; maps from
before the all-capture inventory are refused with a request to rerun `bind`.
`bundle --packs <dir>` adds the map as the loader's `models/safetensors.json`
member, copies the pack beside the archive and records it in the manifest;
`bundle-verify` re-checks the pack digest and that every capture is mapped. Static-history decode variants
(`decode/.../static-h<N>`, for SmolLM2, T5, Whisper and SmolVLM at the first history and the
capacity; `--static-history auto`) pin one history length beside the dynamic artifact,
with two independent cases each (the initial prompt and a cache reset onto
another prompt, both rolled forward to every history) and a recorded refusal of
every other history and of an over-capacity state.
Empty-cache captures are live, not dead: their clones feed the cache
concatenations, so canonical exports keep them. The cohort's 36 empty captures
all have shape `[0]`; a static consumer must support empty 1-D tensors in
concatenation (or normalize them with value-preserving provenance) rather than
prune them, which would change the graph.
Original-size and checkpoint-backed runs are heavy: dispatch the `checkpoint`
workflow by editing `checkpoint-request.json` (push to `devel`), which exports,
binds, packs and bundles the requested models and uploads the evidence.
With `publish` (a request field or dispatch input) a second job uploads bundles,
manifests, packs and `publication.json` (`hf-pt2 index`: exact URLs, SHA-256 and
sizes, with producer commit, upstream checkpoint and release tag kept as
separate facts) to the release `pack_tag` (default `checkpoint-packs-<sha12>`),
never overwriting assets, then downloads each URL fresh and compares digests.
The maps' `source.url` points at those assets; mltorch's resolver still reads
only `repo_id`/`revision`/`filename` as a Hugging Face source, so consumers use
the URL or a local file until it gains URL loading.

**Checkpoint map v2.** [`docs/checkpoint-map-v2.md`](docs/checkpoint-map-v2.md)
specifies a map that points every capture at pinned files instead of a derived
full-weights pack: the original (or converted) checkpoint with a declared
conversion (`none`, or `cast` such as BF16 to F32), and small graph-owned values
generated, inlined or in a tiny pack. `hf-pt2 map` emits it and proves it by
reproducing every capture digest; `bundle --maps [--slim]` ships it, and slim
bundles omit `model.pt2` and the full pack. Version 1 maps are unchanged.

**Converted checkpoints and the matrix.** BERT, MobileViT and VideoMAE have no
upstream safetensors at their pinned revisions, so `reference.conversion` pins the
upstream `pytorch_model.bin` digest and the digest of the converted file;
`hf-pt2 convert` loads the bin with `weights_only`, writes safetensors, checks it
tensor-for-tensor and prints both digests. Their contracts record the
conversion apart from upstream weights. BERT task heads stay random
architecture probes. `hf-pt2 matrix` joins one checkpoint run's export, bind,
pack and offline-replay results into `checkpoint-matrix.md/json` (released with
the bundles); consumer admission is never inferred from producer success.

**Task assets and components.** `task-assets.json` (`make assets`, needs the
Hub) pins each base model's processor, tokenizer and generation files by
revision URL and SHA-256 and records tensor-level recipes: preprocessing
policies, special-token ids, output decoding and one seeded raw-input-to-tensor
example per family, with an informational comparison to the model's original-size
input shapes (for example YOLOS/SegFormer processors emit larger images than
the exported 224 contract, and tokenizers pad to their own length). Raw media
decoding is out of scope. `make models.encoders` publishes TinyCLIP's
`image-encoder` and `text-encoder` as standalone components with their own
graphs, cases, captures and (checkpoint-backed) packs, verified against the
combined model's normalized embeddings.

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
