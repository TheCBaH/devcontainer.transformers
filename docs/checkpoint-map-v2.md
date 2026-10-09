# Checkpoint map, version 2

A v2 map tells a consumer how to obtain every tensor a graph captures
(`PARAMETER`, `BUFFER`, `CONSTANT_TENSOR`) from pinned files, and declares any
conversion. It replaces the derived full-weights pack with: the original
checkpoint where a tensor already exists, and a small description of the rest.
Version 1 (`safetensors.json`, one source file, no conversions) is unchanged.

A bundle carries the map as `models/safetensors.v2.json`. A map belongs to one
artifact: `artifact_id` and `graph_sha256` must equal the graph's. The schema is
[`schemas/checkpoint-map-v2.schema.json`](../schemas/checkpoint-map-v2.schema.json).

## Document

```json
{
  "schema_version": 2,
  "artifact_id": "smollm2-135m/text-decoder/reference/prefill/fp32/dynamo/static/ckpt-12fd25f7a0b1",
  "graph_sha256": "<sha256 of models/model.json>",
  "model_id": "smollm2-135m",
  "sources": {
    "checkpoint": {"files": [<checkpoint file>, ...]},
    "graph_owned": <pinned file>
  },
  "tensors": {"<capture target>": <tensor>, ...},
  "unmapped": []
}
```

`tensors` has exactly one entry for each capture of the graph (the targets in
`captures.json`), and `unmapped` is always empty: a graph with a capture that has
no source has no map.

### Files

Every file is pinned by `name`, `sha256` (of the bytes), `size` and an
`https://` `url`. A consumer must verify size and digest before use. Two kinds of
checkpoint file exist:

- **Upstream:** `repo_id` and `revision` (a 40-hex commit). The URL is the
  revision-pinned Hub resolve link.
- **Converted:** the upstream repository has no safetensors file at the pinned
  revision. `derived_from` records `repo_id`, `revision`, `file`, `sha256` of the
  upstream file and the `tool`. The converted file itself is hosted at `url`
  (release asset) and its digest is the pin.

`graph_owned` (optional) is a safetensors file holding graph-owned tensors too
large to inline.

### Tensors

```json
{"dtype": "F32", "shape": [49152, 576], "sha256": "<digest of the final value>", "origin": {...}}
```

`dtype` uses safetensors codes (`F64 F32 F16 BF16 I64 I32 I16 I8 U8 BOOL`) and
`shape` is the graph's. `sha256` is the digest of the tensor's raw
little-endian row-major bytes **after** all conversions, i.e. the value the graph
must receive. A consumer applies the origin, checks dtype and shape, and checks
this digest; any mismatch is an error.

Origins:

| `kind` | Fields | Meaning |
| --- | --- | --- |
| `checkpoint` | `file`, `key`, `convert`, `tied_aliases` | Read `key` from the named checkpoint file, then apply `convert`. `tied_aliases` lists other names that share the stored tensor (information only). |
| `generated` | `op: "empty"` | A tensor with zero elements. |
| `generated` | `op: "fill"`, `element_hex` | Every element equals the given bytes (one element, little-endian hex). Covers scalars, zero buffers, constants. |
| `inline` | `data_base64` | The raw bytes, at most 64 KiB. |
| `pack` | `key` | A tensor of that name in the `graph_owned` file. |

### Conversion

`convert` is `{"op": "none"}` (stored dtype equals `dtype`) or
`{"op": "cast", "from": "BF16", "to": "F32"}`. The consumer must check that the
stored dtype equals `from`, then convert elementwise to `to` with
round-to-nearest-even (widening conversions such as `BF16` or `F16` to `F32` are
exact). No other conversion exists; in particular nothing renames, transposes,
reshapes or merges tensors. Anything else (key renames, tying) is already
resolved: `key` is the name in the file.

## Producer and reference consumer

- `hf-pt2 map --subset M --binding B --program P --artifact ID --graph G
  --pack-url <release base URL> --output DIR` writes `<flat id>.map.v2.json`
  (plus the graph-owned and converted files it hosts), validates the schema,
  checks the structure against the graph's captures, then applies the map to the
  sources with the reference consumer and requires every digest to reproduce.
- `hf-pt2 bundle --maps DIR [--slim]` adds the map and the hosted files to a
  bundle. `--slim` also leaves out `model.pt2` and the full v1 pack; the
  manifest then has `payload: null` and `map_v2.assets`.
- `mapv2.load_tensors` is the reference consumer (about 40 lines) and
  `mapv2.check_structure` the weight-free structural check.

## What a consumer needs

1. Read the graph and configs from the bundle; read this map.
2. Fetch the files in `sources` (Hub or release), verifying size and digest.
3. For each capture, produce the value from its origin, verify `sha256`.
4. Run the graph; compare with the bundled reference cases.

Replay with `model.pt2` is a CI check on the full artifact; slim bundles record
the case tensors and the digests but do not ship the program.
