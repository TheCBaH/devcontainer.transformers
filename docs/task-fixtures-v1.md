# Task fixtures v1

The producer computes references in its frozen CPU environment. Consumers read
JSON, raw bytes and flat tensor maps; they do not install or execute this
repository's Python, torch, Transformers, tokenizers, Pillow or NumPy. Upstream
ATen torchgen is outside this task-fixture boundary.

[`task-recipes.json`](../task-recipes.json) is the source registry.
[`task-fixture-request.json`](../task-fixture-request.json) selects exact recipes,
an immutable checkpoint publication, its SHA-256/size, the older release
producer, architecture and frozen lock. A top-level checkout supplies recipes,
schemas, configs and [`catalogue.json`](../catalogue.json) without initializing
submodules. The tiny random-weight source population and checkpoint/task release
populations have independent identities. None implies OCaml admission.

## Publication and selection

Push a changed task request to `devel`, or dispatch `checkpoint` with
`task_fixtures: true`. The existing checkpoint workflow runs isolated ARM64
producer generators, checks every named tensor and complete requested case set,
then collects a task index. With `publish: true` it creates a companion release
`task-fixtures-<generator-sha12>-<canonical-request-sha12>`. It uploads a draft,
downloads and compares every asset (including the index), then publishes the
completed release and checks public payload downloads. An existing tag, even a
draft, fails; a changed request or generator requires a new identity. Old
checkpoint releases and their assets are never changed.

The release contains `task-fixtures.json`, `task-fixtures.pin.json`, an external
`*.manifest.json` and a bounded `*.tar.gz` per recipe. The index pins each
manifest/archive by exact download URL, SHA-256 and byte size. Consumers must
record the index's SHA-256/size in their own trusted manifest; fetching its pin
file alongside an untrusted index is not a trust anchor. Artifact and recipe IDs
are full strings in the index/manifests and consumer cache keys. Asset filenames
use a safe recipe name plus a hash of the full fixture identity. No `latest`,
branch downloads, replacement assets or architecture-based weight substitutions.

The generator commit and original checkpoint-release producer commit are
separate fields. A fixture identity includes the full primary artifact ID,
recipe ID and canonical recipe digest, generator commit and canonical request
digest. Canonical JSON uses sorted keys, compact separators, ASCII escapes,
finite numbers and SHA-256 of UTF-8 bytes. Checkpoint/model/config identities,
original graph/contract/v2 map pins and release environment remain in
`references`. Checkpoint weights are referenced, never included in task bundles.
All selected component references must use the same checkpoint and FP32 dtype.

The first end-to-end BERT publication is
[task-fixtures-f50e2d2edb87-46c01cb3ac5f](https://github.com/TheCBaH/devcontainer.transformers/releases/tag/task-fixtures-f50e2d2edb87-46c01cb3ac5f).
Its index SHA-256 is
`56702527be5d1e1e4f7f3dd9fadab62693b80cf1b49c6eef67e576343125a31b`.
The six verified small WordPiece examples are also committed in
[`fixtures/task-examples/bert-wordpiece-v1.json`](../fixtures/task-examples/bert-wordpiece-v1.json).

## Archive and tensor format

Each archive contains `task-contract.json`, `environment.json`, the exact
tokenizer/processor/config asset bytes, `raw/*` and named tensor files under
`cases/<case-id>/*.pt`. MobileViT includes all config labels in `labels.json`.
Every archive member has a SHA-256 and size in the external manifest; that
manifest also pins the archive itself. The index pins the external manifest.
`task-contract.json` equals the manifest after removing `members` and `archive`,
avoiding circular hashes. Only unique relative regular-file members are allowed;
extra, missing, duplicate, linked, oversized and traversal members fail. The
uncompressed bound is 768 MiB and 4096 members per bundle.

The format `torch-flat-tensor-map-v1` reuses the existing `torch.save` zip archive
with a flat `dict[str, Tensor]`. It has no model, Python class, NumPy array or
custom object. Existing OCaml PT readers can consume its storage and pickle
structure as data. No consumer conversion or producer interpreter is needed.
Tensor records are ordered arrays, preserving call/output order despite sorted
JSON keys. Each record names the tensor, dtype, complete integer shape
and SHA-256 of contiguous CPU storage bytes in row-major order. Supported task
dtypes are float32, int64, uint8 and bool; storage is little-endian on the frozen
ARM64 producer. These content hashes exclude the tensor name/metadata; member
byte hashes separately cover the serialized `.pt` files. Empty tensors hash
empty bytes. Dtypes/shapes/names must be checked before comparison.

Schemas: [`task-contract`](../schemas/task-contract.schema.json),
[`task-manifest`](../schemas/task-manifest.schema.json) and
[`task-index`](../schemas/task-index.schema.json). Missing case coverage,
incorrect recipe/revision, corrupt bytes, unsupported format or state must fail
explicitly. Verify the trusted index pin, select a full artifact/recipe identity,
verify its manifest and archive pins, enforce the exact member inventory and
case list, then compare offline. Producer integrity regressions cover these
failure paths; this does not implement the consumer's OCaml selection tools.

## Recipes and numerical scope

* BERT WordPiece: six UTF-8 examples cover natural text, empty input, punctuation,
  Unicode, padding and truncation to the selected static length 16. IDs, masks,
  token types, offsets and special-token masks accompany every hidden and pooled
  output. Small JSON tokenization vectors are emitted for source examples.
* TinyCLIP: a pinned COCO photograph of two cats, portrait/wide crops and a tiny
  image exercise aspect ratios, resize/crop and channel handling. Natural text
  includes truncation. Records contain decoded RGB, resize/crop intermediates,
  final pixels, tokenization, projected image/text features, their L2-normalized
  embeddings, `exp(logit_scale)` and both similarity matrices. Both independently
  pinned tower contracts are validated and replayed.
* MobileViT: the same bounded images, exact processor/config bytes, BGR pixels
  at 256x256, all 1000 logits, labels and top five. Pillow and torchvision
  are different explicit recipes for both image families; neither silently
  substitutes for the other. Raw decoding and Pillow preprocessing can be tested
  from the released bytes/vectors without installing Pillow in the consumer.
* SmolLM2: two independently reset natural prompts tokenize/truncate to four real
  tokens. Prefill emits the first greedy token, static history-4 decode emits the
  second. Every full logit/K/V tensor, next input, mask, absolute position and
  token is recorded. State transitions name source/destination tensors. The
  host stops on EOS or two emitted tokens. History 5 is rejected by the selected
  static graph; no third token is authorized. This bounded recipe does not imply
  support for every dynamic history or for another checkpoint. Other generation
  families and SmolVLM raw image/chat routing remain explicit coverage gaps.
* Diagnostics: original SmolLM2 prefill, Whisper decode and SmolVLM decode cases
  preserve all original output tensors and tolerances, alongside controlled
  eager and re-exported results. Every named output/K/V has bitwise, absolute
  error and over-tolerance counts. A re-export is identified as such; it is not
  represented as execution of a released graph or an OCaml kernel. Diagnostic
  mismatch status never converts a consumer failure into a pass.

Loading checks reject missing/mismatched weights and unexpected keys; unused
BERT checkpoint task-head keys are explicitly allowed and recorded. Generators
verify all checkpoint bytes against the older release, and require its exact
lock, package versions and architecture. Environment evidence includes Python,
tokenizers/Pillow/NumPy versions, generator/source hashes, torch CPU build/kernel
configuration, CPU identity, threading, attention route and export policy.
Default and alternate consumer numerical policies remain unmeasured. The
historical SmolLM2 logit and MobileViT/connector tolerance failures are not closed
by publishing these producer references or by a sequential-dot policy pass.

## Producer commands

```
uv run --frozen python scripts/task-fixtures.py generate --recipe bert-wordpiece-v1
uv run --frozen python scripts/task-fixtures.py index --repository TheCBaH/devcontainer.transformers --tag <new-tag>
uv run --frozen python scripts/task-fixtures.py verify --index-pin .build/task-fixtures/task-fixtures.pin.json --tensors
```

Generation requires committed sources and the exact requested ARM64 environment.
The verification command without `--tensors` uses only the standard library and
checks all byte pins, case coverage and manifest identities. It is a producer
maintenance tool; consumers implement selection/integrity and numerical
comparison in OCaml and never invoke it.
