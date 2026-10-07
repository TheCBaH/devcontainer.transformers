# Symbolic shapes in functional graphs

22 saved artifacts inspected; 5 contain symbolic dimensions or scalars, affecting 249 nodes.

Generated from the hash-bound `models/**/models/model.json` files. This includes forward, encoder, vision, connector, prefill and decode artifacts present under `models/`. Symbols are local to each artifact: the same name in two graphs does not connect their dimensions. Export hints are examples, not fixed sizes. A static input contract can still contain data-dependent internal dimensions.

A node is included when an input/output tensor dimension or scalar contains a symbol. This catches tensor operations such as `matmul` as well as explicit SymInt arguments and symbolic guard predicates. Fixed SymInt-typed values alone do not qualify a node. Included nodes retain every serialized argument by name, including fixed settings and complete mixed lists such as `size=[1,4,(s15+1),16]`. Symbolic references are resolved to expressions; constants remain literal. Shape-reading nodes supply scalar sizes at runtime; the input tensors carry the actual dimensions. Symbolic strides alone are outside this report.

The operator catalog in [ops-func.md](ops-func.md) describes the core forward population; this report describes the saved functional artifacts. It does not measure FLOPs or count inference steps.

| Artifact | Graph nodes | Affected nodes | Symbols |
| --- | ---: | ---: | --- |
| [`bert-tiny/text-encoder/tiny/forward/fp32/dynamo/static`](models/bert-tiny/text-encoder/tiny/forward/fp32/dynamo/static/models/model.json) | 95 | 0 | — |
| [`mobilevit-xxs/image-classification/tiny/forward/fp32/dynamo/static`](models/mobilevit-xxs/image-classification/tiny/forward/fp32/dynamo/static/models/model.json) | 394 | 0 | — |
| [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-3) | 253 | 100 | `s15` |
| [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/static-h4`](models/smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/static-h4/models/model.json) | 202 | 0 | — |
| [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/static-h8`](models/smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/static-h8/models/model.json) | 202 | 0 | — |
| [`smollm2-135m/text-decoder/tiny/forward/fp32/dynamo/static`](models/smollm2-135m/text-decoder/tiny/forward/fp32/dynamo/static/models/model.json) | 192 | 0 | — |
| [`smollm2-135m/text-decoder/tiny/prefill/fp32/dynamo/static`](models/smollm2-135m/text-decoder/tiny/prefill/fp32/dynamo/static/models/model.json) | 200 | 0 | — |
| [`smolvlm-256m/image-text-generation/tiny/connector/fp32/dynamo/static`](models/smolvlm-256m/image-text-generation/tiny/connector/fp32/dynamo/static/models/model.json) | 9 | 0 | — |
| [`smolvlm-256m/image-text-generation/tiny/decode/fp32/dynamo/dynamic`](#artifact-9) | 141 | 44 | `s15` |
| [`smolvlm-256m/image-text-generation/tiny/prefill/fp32/dynamo/static`](models/smolvlm-256m/image-text-generation/tiny/prefill/fp32/dynamo/static/models/model.json) | 133 | 0 | — |
| [`smolvlm-256m/image-text-generation/tiny/vision/fp32/dynamo/static`](#artifact-11) | 98 | 7 | `u0` |
| [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) | 179 | 61 | `s0` |
| [`t5-small/text-encoder-decoder/tiny/encoder/fp32/dynamo/static`](models/t5-small/text-encoder-decoder/tiny/encoder/fp32/dynamo/static/models/model.json) | 108 | 0 | — |
| [`t5-small/text-encoder-decoder/tiny/forward/fp32/dynamo/static`](models/t5-small/text-encoder-decoder/tiny/forward/fp32/dynamo/static/models/model.json) | 272 | 0 | — |
| [`t5-small/text-encoder-decoder/tiny/prefill/fp32/dynamo/static`](models/t5-small/text-encoder-decoder/tiny/prefill/fp32/dynamo/static/models/model.json) | 172 | 0 | — |
| [`time-series-small/time-series/tiny/forward/fp32/dynamo/static`](models/time-series-small/time-series/tiny/forward/fp32/dynamo/static/models/model.json) | 259 | 0 | — |
| [`tinyclip/image-text-embeddings/tiny/forward/fp32/dynamo/static`](models/tinyclip/image-text-embeddings/tiny/forward/fp32/dynamo/static/models/model.json) | 124 | 0 | — |
| [`videomae-small/video-classification/tiny/forward/fp32/dynamo/static`](models/videomae-small/video-classification/tiny/forward/fp32/dynamo/static/models/model.json) | 40 | 0 | — |
| [`whisper-tiny/audio-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-19) | 106 | 37 | `s0` |
| [`whisper-tiny/audio-encoder-decoder/tiny/encoder/fp32/dynamo/static`](models/whisper-tiny/audio-encoder-decoder/tiny/encoder/fp32/dynamo/static/models/model.json) | 43 | 0 | — |
| [`whisper-tiny/audio-encoder-decoder/tiny/forward/fp32/dynamo/static`](models/whisper-tiny/audio-encoder-decoder/tiny/forward/fp32/dynamo/static/models/model.json) | 145 | 0 | — |
| [`whisper-tiny/audio-encoder-decoder/tiny/prefill/fp32/dynamo/static`](models/whisper-tiny/audio-encoder-decoder/tiny/prefill/fp32/dynamo/static/models/model.json) | 105 | 0 | — |

## Operators using symbolic shapes or scalars

| Operator | Affected nodes | Model artifacts (node counts) |
| --- | ---: | --- |
| `_operator.add` | 12 | [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-3) (9), [`smolvlm-256m/image-text-generation/tiny/decode/fp32/dynamo/dynamic`](#artifact-9) (1), [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (1), [`whisper-tiny/audio-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-19) (1) |
| `_operator.eq` | 16 | [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-3) (10), [`smolvlm-256m/image-text-generation/tiny/decode/fp32/dynamo/dynamic`](#artifact-9) (2), [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (2), [`whisper-tiny/audio-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-19) (2) |
| `_operator.ge` | 1 | [`smolvlm-256m/image-text-generation/tiny/vision/fp32/dynamo/static`](#artifact-11) (1) |
| `_operator.le` | 9 | [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-3) (2), [`smolvlm-256m/image-text-generation/tiny/decode/fp32/dynamo/dynamic`](#artifact-9) (2), [`smolvlm-256m/image-text-generation/tiny/vision/fp32/dynamo/static`](#artifact-11) (1), [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (2), [`whisper-tiny/audio-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-19) (2) |
| `_operator.mul` | 8 | [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-3) (8) |
| `aten.__and__.Tensor` | 8 | [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-3) (2), [`smolvlm-256m/image-text-generation/tiny/decode/fp32/dynamo/dynamic`](#artifact-9) (2), [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (2), [`whisper-tiny/audio-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-19) (2) |
| `aten._assert_scalar.default` | 6 | [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-3) (4), [`smolvlm-256m/image-text-generation/tiny/vision/fp32/dynamo/static`](#artifact-11) (2) |
| `aten._assert_tensor_metadata.default` | 17 | [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-3) (5), [`smolvlm-256m/image-text-generation/tiny/decode/fp32/dynamo/dynamic`](#artifact-9) (4), [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (5), [`whisper-tiny/audio-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-19) (3) |
| `aten._to_copy.default` | 6 | [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-3) (1), [`smolvlm-256m/image-text-generation/tiny/decode/fp32/dynamo/dynamic`](#artifact-9) (1), [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (3), [`whisper-tiny/audio-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-19) (1) |
| `aten._unsafe_view.default` | 4 | [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-3) (4) |
| `aten.add.Tensor` | 20 | [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-3) (5), [`smolvlm-256m/image-text-generation/tiny/decode/fp32/dynamo/dynamic`](#artifact-9) (4), [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (7), [`whisper-tiny/audio-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-19) (4) |
| `aten.arange.default` | 5 | [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-3) (1), [`smolvlm-256m/image-text-generation/tiny/decode/fp32/dynamo/dynamic`](#artifact-9) (1), [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (2), [`whisper-tiny/audio-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-19) (1) |
| `aten.cat.default` | 20 | [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-3) (8), [`smolvlm-256m/image-text-generation/tiny/decode/fp32/dynamo/dynamic`](#artifact-9) (4), [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (4), [`whisper-tiny/audio-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-19) (4) |
| `aten.clone.default` | 9 | [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-3) (6), [`smolvlm-256m/image-text-generation/tiny/decode/fp32/dynamo/dynamic`](#artifact-9) (1), [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (1), [`whisper-tiny/audio-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-19) (1) |
| `aten.div.Tensor` | 2 | [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (2) |
| `aten.embedding.default` | 1 | [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (1) |
| `aten.expand.default` | 10 | [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-3) (5), [`smolvlm-256m/image-text-generation/tiny/decode/fp32/dynamo/dynamic`](#artifact-9) (3), [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (1), [`whisper-tiny/audio-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-19) (1) |
| `aten.full_like.default` | 1 | [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (1) |
| `aten.index.Tensor` | 5 | [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-3) (1), [`smolvlm-256m/image-text-generation/tiny/decode/fp32/dynamo/dynamic`](#artifact-9) (1), [`smolvlm-256m/image-text-generation/tiny/vision/fp32/dynamo/static`](#artifact-11) (1), [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (1), [`whisper-tiny/audio-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-19) (1) |
| `aten.index_put.default` | 1 | [`smolvlm-256m/image-text-generation/tiny/vision/fp32/dynamo/static`](#artifact-11) (1) |
| `aten.le.Tensor` | 4 | [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-3) (1), [`smolvlm-256m/image-text-generation/tiny/decode/fp32/dynamo/dynamic`](#artifact-9) (1), [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (1), [`whisper-tiny/audio-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-19) (1) |
| `aten.log.default` | 1 | [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (1) |
| `aten.lt.Scalar` | 1 | [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (1) |
| `aten.matmul.default` | 10 | [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-3) (4), [`smolvlm-256m/image-text-generation/tiny/decode/fp32/dynamo/dynamic`](#artifact-9) (2), [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (2), [`whisper-tiny/audio-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-19) (2) |
| `aten.min.other` | 2 | [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (2) |
| `aten.mul.Tensor` | 6 | [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-3) (2), [`smolvlm-256m/image-text-generation/tiny/decode/fp32/dynamo/dynamic`](#artifact-9) (1), [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (2), [`whisper-tiny/audio-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-19) (1) |
| `aten.neg.default` | 1 | [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (1) |
| `aten.permute.default` | 1 | [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (1) |
| `aten.softmax.int` | 5 | [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-3) (2), [`smolvlm-256m/image-text-generation/tiny/decode/fp32/dynamo/dynamic`](#artifact-9) (1), [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (1), [`whisper-tiny/audio-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-19) (1) |
| `aten.sub.Tensor` | 1 | [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (1) |
| `aten.sym_size.int` | 19 | [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-3) (6), [`smolvlm-256m/image-text-generation/tiny/decode/fp32/dynamo/dynamic`](#artifact-9) (4), [`smolvlm-256m/image-text-generation/tiny/vision/fp32/dynamo/static`](#artifact-11) (1), [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (4), [`whisper-tiny/audio-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-19) (4) |
| `aten.transpose.int` | 5 | [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-3) (2), [`smolvlm-256m/image-text-generation/tiny/decode/fp32/dynamo/dynamic`](#artifact-9) (1), [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (1), [`whisper-tiny/audio-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-19) (1) |
| `aten.unsqueeze.default` | 20 | [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-3) (7), [`smolvlm-256m/image-text-generation/tiny/decode/fp32/dynamo/dynamic`](#artifact-9) (5), [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (5), [`whisper-tiny/audio-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-19) (3) |
| `aten.view.default` | 2 | [`smolvlm-256m/image-text-generation/tiny/decode/fp32/dynamo/dynamic`](#artifact-9) (2) |
| `aten.where.ScalarOther` | 4 | [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-3) (1), [`smolvlm-256m/image-text-generation/tiny/decode/fp32/dynamo/dynamic`](#artifact-9) (1), [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (1), [`whisper-tiny/audio-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-19) (1) |
| `aten.where.self` | 1 | [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (1) |
| `aten.zeros_like.default` | 1 | [`t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-12) (1) |
| `torch.sym_min` | 4 | [`smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic`](#artifact-3) (4) |

<a id="artifact-3"></a>

## smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic

[Saved graph](models/smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic/models/model.json) · [Contract](models/smollm2-135m/text-decoder/tiny/decode/fp32/dynamo/dynamic/contract.json)

Graph SHA256: `ee740087bf4063f92367ed976825a87c2a1ff5abd432a75f173b8b2fb36827ba`.

| Symbol or expression | Minimum | Maximum |
| --- | ---: | ---: |
| `s15` | `1` | `8` |
| `s15 + 1` | `2` | `9` |

| Operator | Affected nodes | Symbols | Example node |
| --- | ---: | --- | --- |
| `_operator.add` | 9 | `s15` | `add_209` |
| `_operator.eq` | 10 | `s15` | `eq_119` |
| `_operator.le` | 2 | `s15` | `le_4` |
| `_operator.mul` | 8 | `s15` | `mul_291` |
| `aten.__and__.Tensor` | 2 | `s15` | `and_1` |
| `aten._assert_scalar.default` | 4 | `s15` | `nodes[15]` |
| `aten._assert_tensor_metadata.default` | 5 | `s15` | `nodes[63]` |
| `aten._to_copy.default` | 1 | `s15` | `_to_copy` |
| `aten._unsafe_view.default` | 4 | `s15` | `_unsafe_view` |
| `aten.add.Tensor` | 5 | `s15` | `add_26` |
| `aten.arange.default` | 1 | `s15` | `arange_4` |
| `aten.cat.default` | 8 | `s15` | `cat` |
| `aten.clone.default` | 6 | `s15` | `clone_5` |
| `aten.expand.default` | 5 | `s15` | `expand` |
| `aten.index.Tensor` | 1 | `s15` | `index` |
| `aten.le.Tensor` | 1 | `s15` | `le_3` |
| `aten.matmul.default` | 4 | `s15` | `matmul_1` |
| `aten.mul.Tensor` | 2 | `s15` | `mul_151` |
| `aten.softmax.int` | 2 | `s15` | `softmax` |
| `aten.sym_size.int` | 6 | `s15` | `sym_size_int_14` |
| `aten.transpose.int` | 2 | `s15` | `transpose_4` |
| `aten.unsqueeze.default` | 7 | `s15` | `unsqueeze_10` |
| `aten.where.ScalarOther` | 1 | `s15` | `where` |
| `torch.sym_min` | 4 | `s15` | `sym_min_4` |

<details>
<summary>Every affected node: tensor shapes and named argument configurations</summary>

| Node | Operator | Inputs and argument configurations | Outputs | Symbols |
| --- | --- | --- | --- | --- |
| `sym_size_int_14` | `aten.sym_size.int` | `self=attention_mask:[1,(s15+1)], dim=1` | `sym_size_int_14=(s15+1)` | `s15` |
| `sym_size_int_15` | `aten.sym_size.int` | `self=past_0_key:[1,2,s15,16], dim=2` | `sym_size_int_15=s15` | `s15` |
| `sym_size_int_16` | `aten.sym_size.int` | `self=past_0_value:[1,2,s15,16], dim=2` | `sym_size_int_16=s15` | `s15` |
| `sym_size_int_17` | `aten.sym_size.int` | `self=past_1_key:[1,2,s15,16], dim=2` | `sym_size_int_17=s15` | `s15` |
| `sym_size_int_18` | `aten.sym_size.int` | `self=past_1_value:[1,2,s15,16], dim=2` | `sym_size_int_18=s15` | `s15` |
| `sym_size_int` | `aten.sym_size.int` | `self=attention_mask:[1,(s15+1)], dim=1` | `sym_size_int=(s15+1)` | `s15` |
| `add_209` | `_operator.add` | `a=1, b=s15` | `add_209=(s15+1)` | `s15` |
| `le_4` | `_operator.le` | `a=(s15+1), b=(s15+1)` | `le_4=True` | `s15` |
| `mul_291` | `_operator.mul` | `a=16, b=s15` | `mul_291=(16*s15)` | `s15` |
| `add_210` | `_operator.add` | `a=16, b=(16*s15)` | `add_210=((16*s15)+16)` | `s15` |
| `mul_292` | `_operator.mul` | `a=32, b=s15` | `mul_292=(32*s15)` | `s15` |
| `add_211` | `_operator.add` | `a=32, b=(32*s15)` | `add_211=((32*s15)+32)` | `s15` |
| `sym_min_4` | `torch.sym_min` | `a=((16*s15)+16), b=((32*s15)+32)` | `sym_min_4=Min(((16*s15)+16),((32*s15)+32))` | `s15` |
| `eq_119` | `_operator.eq` | `a=Min(((16*s15)+16),((32*s15)+32)), b=((16*s15)+16)` | `eq_119=Equality(Min(((16*s15)+16),((32*s15)+32)),((16*s15)+16))` | `s15` |
| `nodes[15]` | `aten._assert_scalar.default` | `self=Equality(Min(((16*s15)+16),((32*s15)+32)),((16*s15)+16)), assert_msg="Runtime assertion failed for expression Eq(Min(16*s59 + 16, 32*s59 + 32), 16*s59 + 16) on node 'eq_119'"` | `—` | `s15` |
| `mul_293` | `_operator.mul` | `a=16, b=s15` | `mul_293=(16*s15)` | `s15` |
| `add_212` | `_operator.add` | `a=16, b=(16*s15)` | `add_212=((16*s15)+16)` | `s15` |
| `mul_294` | `_operator.mul` | `a=32, b=s15` | `mul_294=(32*s15)` | `s15` |
| `add_213` | `_operator.add` | `a=32, b=(32*s15)` | `add_213=((32*s15)+32)` | `s15` |
| `sym_min_5` | `torch.sym_min` | `a=((16*s15)+16), b=((32*s15)+32)` | `sym_min_5=Min(((16*s15)+16),((32*s15)+32))` | `s15` |
| `eq_120` | `_operator.eq` | `a=Min(((16*s15)+16),((32*s15)+32)), b=((16*s15)+16)` | `eq_120=Equality(Min(((16*s15)+16),((32*s15)+32)),((16*s15)+16))` | `s15` |
| `nodes[22]` | `aten._assert_scalar.default` | `self=Equality(Min(((16*s15)+16),((32*s15)+32)),((16*s15)+16)), assert_msg="Runtime assertion failed for expression Eq(Min(16*s15 + 16, 32*s15 + 32), 16*s15 + 16) on node 'eq_120'"` | `—` | `s15` |
| `eq_121` | `_operator.eq` | `a=s15, b=s15` | `eq_121=True` | `s15` |
| `mul_295` | `_operator.mul` | `a=16, b=s15` | `mul_295=(16*s15)` | `s15` |
| `add_214` | `_operator.add` | `a=16, b=(16*s15)` | `add_214=((16*s15)+16)` | `s15` |
| `mul_296` | `_operator.mul` | `a=32, b=s15` | `mul_296=(32*s15)` | `s15` |
| `add_215` | `_operator.add` | `a=32, b=(32*s15)` | `add_215=((32*s15)+32)` | `s15` |
| `sym_min_6` | `torch.sym_min` | `a=((16*s15)+16), b=((32*s15)+32)` | `sym_min_6=Min(((16*s15)+16),((32*s15)+32))` | `s15` |
| `eq_122` | `_operator.eq` | `a=Min(((16*s15)+16),((32*s15)+32)), b=((16*s15)+16)` | `eq_122=Equality(Min(((16*s15)+16),((32*s15)+32)),((16*s15)+16))` | `s15` |
| `nodes[31]` | `aten._assert_scalar.default` | `self=Equality(Min(((16*s15)+16),((32*s15)+32)),((16*s15)+16)), assert_msg="Runtime assertion failed for expression Eq(Min(16*s54 + 16, 32*s54 + 32), 16*s54 + 16) on node 'eq_122'"` | `—` | `s15` |
| `mul_297` | `_operator.mul` | `a=16, b=s15` | `mul_297=(16*s15)` | `s15` |
| `add_216` | `_operator.add` | `a=16, b=(16*s15)` | `add_216=((16*s15)+16)` | `s15` |
| `mul_298` | `_operator.mul` | `a=32, b=s15` | `mul_298=(32*s15)` | `s15` |
| `add_217` | `_operator.add` | `a=32, b=(32*s15)` | `add_217=((32*s15)+32)` | `s15` |
| `sym_min_7` | `torch.sym_min` | `a=((16*s15)+16), b=((32*s15)+32)` | `sym_min_7=Min(((16*s15)+16),((32*s15)+32))` | `s15` |
| `eq_123` | `_operator.eq` | `a=Min(((16*s15)+16),((32*s15)+32)), b=((16*s15)+16)` | `eq_123=Equality(Min(((16*s15)+16),((32*s15)+32)),((16*s15)+16))` | `s15` |
| `nodes[38]` | `aten._assert_scalar.default` | `self=Equality(Min(((16*s15)+16),((32*s15)+32)),((16*s15)+16)), assert_msg="Runtime assertion failed for expression Eq(Min(16*s45 + 16, 32*s45 + 32), 16*s45 + 16) on node 'eq_123'"` | `—` | `s15` |
| `eq_124` | `_operator.eq` | `a=s15, b=s15` | `eq_124=True` | `s15` |
| `eq_125` | `_operator.eq` | `a=s15, b=s15` | `eq_125=True` | `s15` |
| `le_2` | `_operator.le` | `a=(s15+1), b=(s15+1)` | `le_2=True` | `s15` |
| `eq_6` | `_operator.eq` | `a=s15, b=s15` | `eq_6=True` | `s15` |
| `eq_9` | `_operator.eq` | `a=s15, b=s15` | `eq_9=True` | `s15` |
| `eq_10` | `_operator.eq` | `a=s15, b=s15` | `eq_10=True` | `s15` |
| `cat` | `aten.cat.default` | `tensors=[clone:[0],past_0_key:[1,2,s15,16]], dim=-2` | `cat:[1,2,s15,16]` | `s15` |
| `cat_1` | `aten.cat.default` | `tensors=[clone_1:[0],past_0_value:[1,2,s15,16]], dim=-2` | `cat_1:[1,2,s15,16]` | `s15` |
| `cat_2` | `aten.cat.default` | `tensors=[clone_2:[0],past_1_key:[1,2,s15,16]], dim=-2` | `cat_2:[1,2,s15,16]` | `s15` |
| `cat_3` | `aten.cat.default` | `tensors=[clone_3:[0],past_1_value:[1,2,s15,16]], dim=-2` | `cat_3:[1,2,s15,16]` | `s15` |
| `add_26` | `aten.add.Tensor` | `self=arange:[1], other=s15` | `add_26:[1]` | `s15` |
| `nodes[63]` | `aten._assert_tensor_metadata.default` | `a=attention_mask:[1,(s15+1)], size=None, stride=None, dtype={"as_scalar_type":5}, device={"as_device":{"index":null,"type":"cpu"}}, layout={"as_layout":7}` | `—` | `s15` |
| `_to_copy` | `aten._to_copy.default` | `self=attention_mask:[1,(s15+1)], dtype={"as_scalar_type":12}, device={"as_device":{"index":null,"type":"cpu"}}` | `_to_copy:[1,(s15+1)]` | `s15` |
| `add_30` | `aten.add.Tensor` | `self=arange_3:[1], other=s15` | `add_30:[1]` | `s15` |
| `arange_4` | `aten.arange.default` | `end=(s15+1), device={"as_device":{"index":null,"type":"cpu"}}, pin_memory=False` | `arange_4:[(s15+1)]` | `s15` |
| `add_33` | `aten.add.Tensor` | `self=arange_4:[(s15+1)], other=0` | `add_33:[(s15+1)]` | `s15` |
| `unsqueeze_10` | `aten.unsqueeze.default` | `self=add_33:[(s15+1)], dim=0` | `unsqueeze_10:[1,(s15+1)]` | `s15` |
| `unsqueeze_11` | `aten.unsqueeze.default` | `self=unsqueeze_10:[1,(s15+1)], dim=1` | `unsqueeze_11:[1,1,(s15+1)]` | `s15` |
| `unsqueeze_12` | `aten.unsqueeze.default` | `self=unsqueeze_11:[1,1,(s15+1)], dim=2` | `unsqueeze_12:[1,1,1,(s15+1)]` | `s15` |
| `le_3` | `aten.le.Tensor` | `self=unsqueeze_12:[1,1,1,(s15+1)], other=unsqueeze_9:[1,1,1,1]` | `le_3:[1,1,1,(s15+1)]` | `s15` |
| `nodes[81]` | `aten._assert_tensor_metadata.default` | `a=le_3:[1,1,1,(s15+1)], size=None, stride=None, dtype={"as_scalar_type":12}, device={"as_device":{"index":null,"type":"cpu"}}, layout={"as_layout":7}` | `—` | `s15` |
| `and_1` | `aten.__and__.Tensor` | `self=new_ones:[], other=le_3:[1,1,1,(s15+1)]` | `and_1:[1,1,1,(s15+1)]` | `s15` |
| `index` | `aten.index.Tensor` | `self=_to_copy:[1,(s15+1)], indices=[unsqueeze_3:[1,1,1,1],unsqueeze_12:[1,1,1,(s15+1)]]` | `index:[1,1,1,(s15+1)]` | `s15` |
| `nodes[84]` | `aten._assert_tensor_metadata.default` | `a=index:[1,1,1,(s15+1)], size=None, stride=None, dtype={"as_scalar_type":12}, device={"as_device":{"index":null,"type":"cpu"}}, layout={"as_layout":7}` | `—` | `s15` |
| `and_2` | `aten.__and__.Tensor` | `self=and_1:[1,1,1,(s15+1)], other=index:[1,1,1,(s15+1)]` | `and_2:[1,1,1,(s15+1)]` | `s15` |
| `expand` | `aten.expand.default` | `self=and_2:[1,1,1,(s15+1)], size=[1,-1,1,(s15+1)]` | `expand:[1,1,1,(s15+1)]` | `s15` |
| `where` | `aten.where.ScalarOther` | `condition=expand:[1,1,1,(s15+1)], self=clone_4:[], other=-3.4028234663852886e+38` | `where:[1,1,1,(s15+1)]` | `s15` |
| `cat_7` | `aten.cat.default` | `tensors=[cat:[1,2,s15,16],add_56:[1,2,1,16]], dim=-2` | `cat_7:[1,2,(s15+1),16]` | `s15` |
| `cat_8` | `aten.cat.default` | `tensors=[cat_1:[1,2,s15,16],transpose_3:[1,2,1,16]], dim=-2` | `cat_8:[1,2,(s15+1),16]` | `s15` |
| `unsqueeze_18` | `aten.unsqueeze.default` | `self=cat_7:[1,2,(s15+1),16], dim=2` | `unsqueeze_18:[1,2,1,(s15+1),16]` | `s15` |
| `expand_2` | `aten.expand.default` | `self=unsqueeze_18:[1,2,1,(s15+1),16], size=[1,2,2,(s15+1),16]` | `expand_2:[1,2,2,(s15+1),16]` | `s15` |
| `clone_5` | `aten.clone.default` | `self=expand_2:[1,2,2,(s15+1),16], memory_format={"as_memory_format":1}` | `clone_5:[1,2,2,(s15+1),16]` | `s15` |
| `_unsafe_view` | `aten._unsafe_view.default` | `self=clone_5:[1,2,2,(s15+1),16], size=[1,4,(s15+1),16]` | `_unsafe_view:[1,4,(s15+1),16]` | `s15` |
| `unsqueeze_19` | `aten.unsqueeze.default` | `self=cat_8:[1,2,(s15+1),16], dim=2` | `unsqueeze_19:[1,2,1,(s15+1),16]` | `s15` |
| `expand_3` | `aten.expand.default` | `self=unsqueeze_19:[1,2,1,(s15+1),16], size=[1,2,2,(s15+1),16]` | `expand_3:[1,2,2,(s15+1),16]` | `s15` |
| `clone_6` | `aten.clone.default` | `self=expand_3:[1,2,2,(s15+1),16], memory_format={"as_memory_format":1}` | `clone_6:[1,2,2,(s15+1),16]` | `s15` |
| `_unsafe_view_1` | `aten._unsafe_view.default` | `self=clone_6:[1,2,2,(s15+1),16], size=[1,4,(s15+1),16]` | `_unsafe_view_1:[1,4,(s15+1),16]` | `s15` |
| `transpose_4` | `aten.transpose.int` | `self=_unsafe_view:[1,4,(s15+1),16], dim0=2, dim1=3` | `transpose_4:[1,4,16,(s15+1)]` | `s15` |
| `matmul_1` | `aten.matmul.default` | `self=add_55:[1,4,1,16], other=transpose_4:[1,4,16,(s15+1)]` | `matmul_1:[1,4,1,(s15+1)]` | `s15` |
| `mul_151` | `aten.mul.Tensor` | `self=matmul_1:[1,4,1,(s15+1)], other=0.25` | `mul_151:[1,4,1,(s15+1)]` | `s15` |
| `add_115` | `aten.add.Tensor` | `self=mul_151:[1,4,1,(s15+1)], other=where:[1,1,1,(s15+1)]` | `add_115:[1,4,1,(s15+1)]` | `s15` |
| `softmax` | `aten.softmax.int` | `self=add_115:[1,4,1,(s15+1)], dim=-1, dtype={"as_scalar_type":7}` | `softmax:[1,4,1,(s15+1)]` | `s15` |
| `nodes[153]` | `aten._assert_tensor_metadata.default` | `a=softmax:[1,4,1,(s15+1)], size=None, stride=None, dtype={"as_scalar_type":7}, device={"as_device":{"index":null,"type":"cpu"}}, layout={"as_layout":7}` | `—` | `s15` |
| `clone_7` | `aten.clone.default` | `self=softmax:[1,4,1,(s15+1)]` | `clone_7:[1,4,1,(s15+1)]` | `s15` |
| `matmul_2` | `aten.matmul.default` | `self=clone_7:[1,4,1,(s15+1)], other=_unsafe_view_1:[1,4,(s15+1),16]` | `matmul_2:[1,4,1,16]` | `s15` |
| `cat_11` | `aten.cat.default` | `tensors=[cat_2:[1,2,s15,16],add_133:[1,2,1,16]], dim=-2` | `cat_11:[1,2,(s15+1),16]` | `s15` |
| `cat_12` | `aten.cat.default` | `tensors=[cat_3:[1,2,s15,16],transpose_8:[1,2,1,16]], dim=-2` | `cat_12:[1,2,(s15+1),16]` | `s15` |
| `unsqueeze_22` | `aten.unsqueeze.default` | `self=cat_11:[1,2,(s15+1),16], dim=2` | `unsqueeze_22:[1,2,1,(s15+1),16]` | `s15` |
| `expand_4` | `aten.expand.default` | `self=unsqueeze_22:[1,2,1,(s15+1),16], size=[1,2,2,(s15+1),16]` | `expand_4:[1,2,2,(s15+1),16]` | `s15` |
| `clone_8` | `aten.clone.default` | `self=expand_4:[1,2,2,(s15+1),16], memory_format={"as_memory_format":1}` | `clone_8:[1,2,2,(s15+1),16]` | `s15` |
| `_unsafe_view_2` | `aten._unsafe_view.default` | `self=clone_8:[1,2,2,(s15+1),16], size=[1,4,(s15+1),16]` | `_unsafe_view_2:[1,4,(s15+1),16]` | `s15` |
| `unsqueeze_23` | `aten.unsqueeze.default` | `self=cat_12:[1,2,(s15+1),16], dim=2` | `unsqueeze_23:[1,2,1,(s15+1),16]` | `s15` |
| `expand_5` | `aten.expand.default` | `self=unsqueeze_23:[1,2,1,(s15+1),16], size=[1,2,2,(s15+1),16]` | `expand_5:[1,2,2,(s15+1),16]` | `s15` |
| `clone_9` | `aten.clone.default` | `self=expand_5:[1,2,2,(s15+1),16], memory_format={"as_memory_format":1}` | `clone_9:[1,2,2,(s15+1),16]` | `s15` |
| `_unsafe_view_3` | `aten._unsafe_view.default` | `self=clone_9:[1,2,2,(s15+1),16], size=[1,4,(s15+1),16]` | `_unsafe_view_3:[1,4,(s15+1),16]` | `s15` |
| `transpose_9` | `aten.transpose.int` | `self=_unsafe_view_2:[1,4,(s15+1),16], dim0=2, dim1=3` | `transpose_9:[1,4,16,(s15+1)]` | `s15` |
| `matmul_3` | `aten.matmul.default` | `self=add_132:[1,4,1,16], other=transpose_9:[1,4,16,(s15+1)]` | `matmul_3:[1,4,1,(s15+1)]` | `s15` |
| `mul_269` | `aten.mul.Tensor` | `self=matmul_3:[1,4,1,(s15+1)], other=0.25` | `mul_269:[1,4,1,(s15+1)]` | `s15` |
| `add_192` | `aten.add.Tensor` | `self=mul_269:[1,4,1,(s15+1)], other=where:[1,1,1,(s15+1)]` | `add_192:[1,4,1,(s15+1)]` | `s15` |
| `softmax_1` | `aten.softmax.int` | `self=add_192:[1,4,1,(s15+1)], dim=-1, dtype={"as_scalar_type":7}` | `softmax_1:[1,4,1,(s15+1)]` | `s15` |
| `nodes[222]` | `aten._assert_tensor_metadata.default` | `a=softmax_1:[1,4,1,(s15+1)], size=None, stride=None, dtype={"as_scalar_type":7}, device={"as_device":{"index":null,"type":"cpu"}}, layout={"as_layout":7}` | `—` | `s15` |
| `clone_10` | `aten.clone.default` | `self=softmax_1:[1,4,1,(s15+1)]` | `clone_10:[1,4,1,(s15+1)]` | `s15` |
| `matmul_4` | `aten.matmul.default` | `self=clone_10:[1,4,1,(s15+1)], other=_unsafe_view_3:[1,4,(s15+1),16]` | `matmul_4:[1,4,1,16]` | `s15` |

</details>

<a id="artifact-9"></a>

## smolvlm-256m/image-text-generation/tiny/decode/fp32/dynamo/dynamic

[Saved graph](models/smolvlm-256m/image-text-generation/tiny/decode/fp32/dynamo/dynamic/models/model.json) · [Contract](models/smolvlm-256m/image-text-generation/tiny/decode/fp32/dynamo/dynamic/contract.json)

Graph SHA256: `042090360336664dd899e2b42255c5cf68d0aa9e5e993bcb1355297e91cea8a7`.

| Symbol or expression | Minimum | Maximum |
| --- | ---: | ---: |
| `s15` | `1` | `16` |
| `s15 + 1` | `2` | `17` |

| Operator | Affected nodes | Symbols | Example node |
| --- | ---: | --- | --- |
| `_operator.add` | 1 | `s15` | `add_90` |
| `_operator.eq` | 2 | `s15` | `eq_55` |
| `_operator.le` | 2 | `s15` | `le_4` |
| `aten.__and__.Tensor` | 2 | `s15` | `and_1` |
| `aten._assert_tensor_metadata.default` | 4 | `s15` | `nodes[22]` |
| `aten._to_copy.default` | 1 | `s15` | `_to_copy` |
| `aten.add.Tensor` | 4 | `s15` | `add_8` |
| `aten.arange.default` | 1 | `s15` | `arange_4` |
| `aten.cat.default` | 4 | `s15` | `cat` |
| `aten.clone.default` | 1 | `s15` | `clone_3` |
| `aten.expand.default` | 3 | `s15` | `expand` |
| `aten.index.Tensor` | 1 | `s15` | `index` |
| `aten.le.Tensor` | 1 | `s15` | `le_3` |
| `aten.matmul.default` | 2 | `s15` | `matmul_1` |
| `aten.mul.Tensor` | 1 | `s15` | `mul_111` |
| `aten.softmax.int` | 1 | `s15` | `softmax` |
| `aten.sym_size.int` | 4 | `s15` | `sym_size_int_8` |
| `aten.transpose.int` | 1 | `s15` | `transpose_4` |
| `aten.unsqueeze.default` | 5 | `s15` | `unsqueeze_10` |
| `aten.view.default` | 2 | `s15` | `view_3` |
| `aten.where.ScalarOther` | 1 | `s15` | `where` |

<details>
<summary>Every affected node: tensor shapes and named argument configurations</summary>

| Node | Operator | Inputs and argument configurations | Outputs | Symbols |
| --- | --- | --- | --- | --- |
| `sym_size_int_8` | `aten.sym_size.int` | `self=attention_mask:[1,(s15+1)], dim=1` | `sym_size_int_8=(s15+1)` | `s15` |
| `sym_size_int_9` | `aten.sym_size.int` | `self=past_0_key:[1,1,s15,32], dim=2` | `sym_size_int_9=s15` | `s15` |
| `sym_size_int_10` | `aten.sym_size.int` | `self=past_0_value:[1,1,s15,32], dim=2` | `sym_size_int_10=s15` | `s15` |
| `sym_size_int` | `aten.sym_size.int` | `self=attention_mask:[1,(s15+1)], dim=1` | `sym_size_int=(s15+1)` | `s15` |
| `add_90` | `_operator.add` | `a=1, b=s15` | `add_90=(s15+1)` | `s15` |
| `le_4` | `_operator.le` | `a=(s15+1), b=(s15+1)` | `le_4=True` | `s15` |
| `eq_55` | `_operator.eq` | `a=s15, b=s15` | `eq_55=True` | `s15` |
| `le_2` | `_operator.le` | `a=(s15+1), b=(s15+1)` | `le_2=True` | `s15` |
| `eq_2` | `_operator.eq` | `a=s15, b=s15` | `eq_2=True` | `s15` |
| `cat` | `aten.cat.default` | `tensors=[clone:[0],past_0_key:[1,1,s15,32]], dim=-2` | `cat:[1,1,s15,32]` | `s15` |
| `cat_1` | `aten.cat.default` | `tensors=[clone_1:[0],past_0_value:[1,1,s15,32]], dim=-2` | `cat_1:[1,1,s15,32]` | `s15` |
| `add_8` | `aten.add.Tensor` | `self=arange:[1], other=s15` | `add_8:[1]` | `s15` |
| `nodes[22]` | `aten._assert_tensor_metadata.default` | `a=attention_mask:[1,(s15+1)], size=None, stride=None, dtype={"as_scalar_type":5}, device={"as_device":{"index":null,"type":"cpu"}}, layout={"as_layout":7}` | `—` | `s15` |
| `_to_copy` | `aten._to_copy.default` | `self=attention_mask:[1,(s15+1)], dtype={"as_scalar_type":12}, device={"as_device":{"index":null,"type":"cpu"}}` | `_to_copy:[1,(s15+1)]` | `s15` |
| `add_12` | `aten.add.Tensor` | `self=arange_3:[1], other=s15` | `add_12:[1]` | `s15` |
| `arange_4` | `aten.arange.default` | `end=(s15+1), device={"as_device":{"index":null,"type":"cpu"}}, pin_memory=False` | `arange_4:[(s15+1)]` | `s15` |
| `add_15` | `aten.add.Tensor` | `self=arange_4:[(s15+1)], other=0` | `add_15:[(s15+1)]` | `s15` |
| `unsqueeze_10` | `aten.unsqueeze.default` | `self=add_15:[(s15+1)], dim=0` | `unsqueeze_10:[1,(s15+1)]` | `s15` |
| `unsqueeze_11` | `aten.unsqueeze.default` | `self=unsqueeze_10:[1,(s15+1)], dim=1` | `unsqueeze_11:[1,1,(s15+1)]` | `s15` |
| `unsqueeze_12` | `aten.unsqueeze.default` | `self=unsqueeze_11:[1,1,(s15+1)], dim=2` | `unsqueeze_12:[1,1,1,(s15+1)]` | `s15` |
| `le_3` | `aten.le.Tensor` | `self=unsqueeze_12:[1,1,1,(s15+1)], other=unsqueeze_9:[1,1,1,1]` | `le_3:[1,1,1,(s15+1)]` | `s15` |
| `nodes[40]` | `aten._assert_tensor_metadata.default` | `a=le_3:[1,1,1,(s15+1)], size=None, stride=None, dtype={"as_scalar_type":12}, device={"as_device":{"index":null,"type":"cpu"}}, layout={"as_layout":7}` | `—` | `s15` |
| `and_1` | `aten.__and__.Tensor` | `self=new_ones:[], other=le_3:[1,1,1,(s15+1)]` | `and_1:[1,1,1,(s15+1)]` | `s15` |
| `index` | `aten.index.Tensor` | `self=_to_copy:[1,(s15+1)], indices=[unsqueeze_3:[1,1,1,1],unsqueeze_12:[1,1,1,(s15+1)]]` | `index:[1,1,1,(s15+1)]` | `s15` |
| `nodes[43]` | `aten._assert_tensor_metadata.default` | `a=index:[1,1,1,(s15+1)], size=None, stride=None, dtype={"as_scalar_type":12}, device={"as_device":{"index":null,"type":"cpu"}}, layout={"as_layout":7}` | `—` | `s15` |
| `and_2` | `aten.__and__.Tensor` | `self=and_1:[1,1,1,(s15+1)], other=index:[1,1,1,(s15+1)]` | `and_2:[1,1,1,(s15+1)]` | `s15` |
| `expand` | `aten.expand.default` | `self=and_2:[1,1,1,(s15+1)], size=[1,-1,1,(s15+1)]` | `expand:[1,1,1,(s15+1)]` | `s15` |
| `where` | `aten.where.ScalarOther` | `condition=expand:[1,1,1,(s15+1)], self=clone_2:[], other=-3.4028234663852886e+38` | `where:[1,1,1,(s15+1)]` | `s15` |
| `cat_5` | `aten.cat.default` | `tensors=[cat:[1,1,s15,32],add_38:[1,1,1,32]], dim=-2` | `cat_5:[1,1,(s15+1),32]` | `s15` |
| `cat_6` | `aten.cat.default` | `tensors=[cat_1:[1,1,s15,32],transpose_3:[1,1,1,32]], dim=-2` | `cat_6:[1,1,(s15+1),32]` | `s15` |
| `unsqueeze_18` | `aten.unsqueeze.default` | `self=cat_5:[1,1,(s15+1),32], dim=2` | `unsqueeze_18:[1,1,1,(s15+1),32]` | `s15` |
| `expand_2` | `aten.expand.default` | `self=unsqueeze_18:[1,1,1,(s15+1),32], size=[1,1,2,(s15+1),32]` | `expand_2:[1,1,2,(s15+1),32]` | `s15` |
| `view_3` | `aten.view.default` | `self=expand_2:[1,1,2,(s15+1),32], size=[1,2,(s15+1),32]` | `view_3:[1,2,(s15+1),32]` | `s15` |
| `unsqueeze_19` | `aten.unsqueeze.default` | `self=cat_6:[1,1,(s15+1),32], dim=2` | `unsqueeze_19:[1,1,1,(s15+1),32]` | `s15` |
| `expand_3` | `aten.expand.default` | `self=unsqueeze_19:[1,1,1,(s15+1),32], size=[1,1,2,(s15+1),32]` | `expand_3:[1,1,2,(s15+1),32]` | `s15` |
| `view_4` | `aten.view.default` | `self=expand_3:[1,1,2,(s15+1),32], size=[1,2,(s15+1),32]` | `view_4:[1,2,(s15+1),32]` | `s15` |
| `transpose_4` | `aten.transpose.int` | `self=view_3:[1,2,(s15+1),32], dim0=2, dim1=3` | `transpose_4:[1,2,32,(s15+1)]` | `s15` |
| `matmul_1` | `aten.matmul.default` | `self=add_37:[1,2,1,32], other=transpose_4:[1,2,32,(s15+1)]` | `matmul_1:[1,2,1,(s15+1)]` | `s15` |
| `mul_111` | `aten.mul.Tensor` | `self=matmul_1:[1,2,1,(s15+1)], other=0.1767766952966369` | `mul_111:[1,2,1,(s15+1)]` | `s15` |
| `add_73` | `aten.add.Tensor` | `self=mul_111:[1,2,1,(s15+1)], other=where:[1,1,1,(s15+1)]` | `add_73:[1,2,1,(s15+1)]` | `s15` |
| `softmax` | `aten.softmax.int` | `self=add_73:[1,2,1,(s15+1)], dim=-1, dtype={"as_scalar_type":7}` | `softmax:[1,2,1,(s15+1)]` | `s15` |
| `nodes[110]` | `aten._assert_tensor_metadata.default` | `a=softmax:[1,2,1,(s15+1)], size=None, stride=None, dtype={"as_scalar_type":7}, device={"as_device":{"index":null,"type":"cpu"}}, layout={"as_layout":7}` | `—` | `s15` |
| `clone_3` | `aten.clone.default` | `self=softmax:[1,2,1,(s15+1)]` | `clone_3:[1,2,1,(s15+1)]` | `s15` |
| `matmul_2` | `aten.matmul.default` | `self=clone_3:[1,2,1,(s15+1)], other=view_4:[1,2,(s15+1),32]` | `matmul_2:[1,2,1,32]` | `s15` |

</details>

<a id="artifact-11"></a>

## smolvlm-256m/image-text-generation/tiny/vision/fp32/dynamo/static

[Saved graph](models/smolvlm-256m/image-text-generation/tiny/vision/fp32/dynamo/static/models/model.json) · [Contract](models/smolvlm-256m/image-text-generation/tiny/vision/fp32/dynamo/static/contract.json)

Graph SHA256: `e075d8233be0fcb21b2150a06449a9b9f2a6a78e7b16b525260fefdb1e426151`.

| Symbol or expression | Minimum | Maximum |
| --- | ---: | ---: |
| `u0` | `0` | `16` |

| Operator | Affected nodes | Symbols | Example node |
| --- | ---: | --- | --- |
| `_operator.ge` | 1 | `u0` | `ge_3` |
| `_operator.le` | 1 | `u0` | `le_1` |
| `aten._assert_scalar.default` | 2 | `u0` | `nodes[36]` |
| `aten.index.Tensor` | 1 | `u0` | `index` |
| `aten.index_put.default` | 1 | `u0` | `index_put` |
| `aten.sym_size.int` | 1 | `u0` | `sym_size_int_1` |

<details>
<summary>Every affected node: tensor shapes and named argument configurations</summary>

| Node | Operator | Inputs and argument configurations | Outputs | Symbols |
| --- | --- | --- | --- | --- |
| `index` | `aten.index.Tensor` | `self=view_1:[1,16], indices=[view_2:[1,16]]` | `index:[u0]` | `u0` |
| `sym_size_int_1` | `aten.sym_size.int` | `self=index:[u0], dim=0` | `sym_size_int_1=u0` | `u0` |
| `ge_3` | `_operator.ge` | `a=u0, b=0` | `ge_3=GreaterThan(u0,0)` | `u0` |
| `nodes[36]` | `aten._assert_scalar.default` | `self=GreaterThan(u0,0), assert_msg="Runtime assertion failed for expression u0 >= 0 on node 'ge_3'"` | `—` | `u0` |
| `le_1` | `_operator.le` | `a=u0, b=16` | `le_1=LessThan(u0,16)` | `u0` |
| `nodes[38]` | `aten._assert_scalar.default` | `self=LessThan(u0,16), assert_msg="Runtime assertion failed for expression u0 <= 16 on node 'le_1'"` | `—` | `u0` |
| `index_put` | `aten.index_put.default` | `self=full:[1,16], indices=[view_3:[1,16]], values=index:[u0]` | `index_put:[1,16]` | `u0` |

</details>

<a id="artifact-12"></a>

## t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic

[Saved graph](models/t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic/models/model.json) · [Contract](models/t5-small/text-encoder-decoder/tiny/decode/fp32/dynamo/dynamic/contract.json)

Graph SHA256: `4e8f5f02393df7ebb6000aa9f96fc8dcb9ac8925b21db9c0c6c0901622ee7b7b`.

| Symbol or expression | Minimum | Maximum |
| --- | ---: | ---: |
| `s0` | `1` | `8` |
| `s0 + 1` | `2` | `9` |

| Operator | Affected nodes | Symbols | Example node |
| --- | ---: | --- | --- |
| `_operator.add` | 1 | `s0` | `add_132` |
| `_operator.eq` | 2 | `s0` | `eq_47` |
| `_operator.le` | 2 | `s0` | `le_4` |
| `aten.__and__.Tensor` | 2 | `s0` | `and_1` |
| `aten._assert_tensor_metadata.default` | 5 | `s0` | `nodes[22]` |
| `aten._to_copy.default` | 3 | `s0` | `_to_copy` |
| `aten.add.Tensor` | 7 | `s0` | `add_13` |
| `aten.arange.default` | 2 | `s0` | `arange_3` |
| `aten.cat.default` | 4 | `s0` | `cat` |
| `aten.clone.default` | 1 | `s0` | `clone_7` |
| `aten.div.Tensor` | 2 | `s0` | `div` |
| `aten.embedding.default` | 1 | `s0` | `embedding_1` |
| `aten.expand.default` | 1 | `s0` | `expand` |
| `aten.full_like.default` | 1 | `s0` | `full_like` |
| `aten.index.Tensor` | 1 | `s0` | `index` |
| `aten.le.Tensor` | 1 | `s0` | `le_3` |
| `aten.log.default` | 1 | `s0` | `log` |
| `aten.lt.Scalar` | 1 | `s0` | `lt` |
| `aten.matmul.default` | 2 | `s0` | `matmul` |
| `aten.min.other` | 2 | `s0` | `min_1` |
| `aten.mul.Tensor` | 2 | `s0` | `mul_65` |
| `aten.neg.default` | 1 | `s0` | `neg` |
| `aten.permute.default` | 1 | `s0` | `permute` |
| `aten.softmax.int` | 1 | `s0` | `softmax` |
| `aten.sub.Tensor` | 1 | `s0` | `sub_18` |
| `aten.sym_size.int` | 4 | `s0` | `sym_size_int_9` |
| `aten.transpose.int` | 1 | `s0` | `transpose_3` |
| `aten.unsqueeze.default` | 5 | `s0` | `unsqueeze_9` |
| `aten.where.ScalarOther` | 1 | `s0` | `where` |
| `aten.where.self` | 1 | `s0` | `where_2` |
| `aten.zeros_like.default` | 1 | `s0` | `zeros_like` |

<details>
<summary>Every affected node: tensor shapes and named argument configurations</summary>

| Node | Operator | Inputs and argument configurations | Outputs | Symbols |
| --- | --- | --- | --- | --- |
| `sym_size_int_9` | `aten.sym_size.int` | `self=decoder_attention_mask:[1,(s0+1)], dim=1` | `sym_size_int_9=(s0+1)` | `s0` |
| `sym_size_int_10` | `aten.sym_size.int` | `self=past_0_self_key:[1,2,s0,32], dim=2` | `sym_size_int_10=s0` | `s0` |
| `sym_size_int_11` | `aten.sym_size.int` | `self=past_0_self_value:[1,2,s0,32], dim=2` | `sym_size_int_11=s0` | `s0` |
| `sym_size_int` | `aten.sym_size.int` | `self=decoder_attention_mask:[1,(s0+1)], dim=1` | `sym_size_int=(s0+1)` | `s0` |
| `add_132` | `_operator.add` | `a=1, b=s0` | `add_132=(s0+1)` | `s0` |
| `le_4` | `_operator.le` | `a=(s0+1), b=(s0+1)` | `le_4=True` | `s0` |
| `eq_47` | `_operator.eq` | `a=s0, b=s0` | `eq_47=True` | `s0` |
| `le_2` | `_operator.le` | `a=(s0+1), b=(s0+1)` | `le_2=True` | `s0` |
| `eq_2` | `_operator.eq` | `a=s0, b=s0` | `eq_2=True` | `s0` |
| `cat` | `aten.cat.default` | `tensors=[clone:[0],past_0_self_key:[1,2,s0,32]], dim=-2` | `cat:[1,2,s0,32]` | `s0` |
| `cat_1` | `aten.cat.default` | `tensors=[clone_1:[0],past_0_self_value:[1,2,s0,32]], dim=-2` | `cat_1:[1,2,s0,32]` | `s0` |
| `nodes[22]` | `aten._assert_tensor_metadata.default` | `a=decoder_attention_mask:[1,(s0+1)], size=None, stride=None, dtype={"as_scalar_type":5}, device={"as_device":{"index":null,"type":"cpu"}}, layout={"as_layout":7}` | `—` | `s0` |
| `_to_copy` | `aten._to_copy.default` | `self=decoder_attention_mask:[1,(s0+1)], dtype={"as_scalar_type":12}, device={"as_device":{"index":null,"type":"cpu"}}` | `_to_copy:[1,(s0+1)]` | `s0` |
| `add_13` | `aten.add.Tensor` | `self=arange_2:[1], other=s0` | `add_13:[1]` | `s0` |
| `arange_3` | `aten.arange.default` | `end=(s0+1), device={"as_device":{"index":null,"type":"cpu"}}, pin_memory=False` | `arange_3:[(s0+1)]` | `s0` |
| `add_16` | `aten.add.Tensor` | `self=arange_3:[(s0+1)], other=0` | `add_16:[(s0+1)]` | `s0` |
| `unsqueeze_9` | `aten.unsqueeze.default` | `self=add_16:[(s0+1)], dim=0` | `unsqueeze_9:[1,(s0+1)]` | `s0` |
| `unsqueeze_10` | `aten.unsqueeze.default` | `self=unsqueeze_9:[1,(s0+1)], dim=1` | `unsqueeze_10:[1,1,(s0+1)]` | `s0` |
| `unsqueeze_11` | `aten.unsqueeze.default` | `self=unsqueeze_10:[1,1,(s0+1)], dim=2` | `unsqueeze_11:[1,1,1,(s0+1)]` | `s0` |
| `le_3` | `aten.le.Tensor` | `self=unsqueeze_11:[1,1,1,(s0+1)], other=unsqueeze_8:[1,1,1,1]` | `le_3:[1,1,1,(s0+1)]` | `s0` |
| `nodes[40]` | `aten._assert_tensor_metadata.default` | `a=le_3:[1,1,1,(s0+1)], size=None, stride=None, dtype={"as_scalar_type":12}, device={"as_device":{"index":null,"type":"cpu"}}, layout={"as_layout":7}` | `—` | `s0` |
| `and_1` | `aten.__and__.Tensor` | `self=new_ones:[], other=le_3:[1,1,1,(s0+1)]` | `and_1:[1,1,1,(s0+1)]` | `s0` |
| `index` | `aten.index.Tensor` | `self=_to_copy:[1,(s0+1)], indices=[unsqueeze_2:[1,1,1,1],unsqueeze_11:[1,1,1,(s0+1)]]` | `index:[1,1,1,(s0+1)]` | `s0` |
| `nodes[43]` | `aten._assert_tensor_metadata.default` | `a=index:[1,1,1,(s0+1)], size=None, stride=None, dtype={"as_scalar_type":12}, device={"as_device":{"index":null,"type":"cpu"}}, layout={"as_layout":7}` | `—` | `s0` |
| `and_2` | `aten.__and__.Tensor` | `self=and_1:[1,1,1,(s0+1)], other=index:[1,1,1,(s0+1)]` | `and_2:[1,1,1,(s0+1)]` | `s0` |
| `expand` | `aten.expand.default` | `self=and_2:[1,1,1,(s0+1)], size=[1,-1,1,(s0+1)]` | `expand:[1,1,1,(s0+1)]` | `s0` |
| `where` | `aten.where.ScalarOther` | `condition=expand:[1,1,1,(s0+1)], self=clone_4:[], other=-3.4028234663852886e+38` | `where:[1,1,1,(s0+1)]` | `s0` |
| `cat_4` | `aten.cat.default` | `tensors=[cat:[1,2,s0,32],transpose_1:[1,2,1,32]], dim=-2` | `cat_4:[1,2,(s0+1),32]` | `s0` |
| `cat_5` | `aten.cat.default` | `tensors=[cat_1:[1,2,s0,32],transpose_2:[1,2,1,32]], dim=-2` | `cat_5:[1,2,(s0+1),32]` | `s0` |
| `add_48` | `aten.add.Tensor` | `self=unsqueeze_24:[1,1], other=s0` | `add_48:[1,1]` | `s0` |
| `arange_9` | `aten.arange.default` | `end=(s0+1), dtype={"as_scalar_type":5}, device={"as_device":{"index":null,"type":"cpu"}}, pin_memory=False` | `arange_9:[(s0+1)]` | `s0` |
| `unsqueeze_25` | `aten.unsqueeze.default` | `self=arange_9:[(s0+1)], dim=0` | `unsqueeze_25:[1,(s0+1)]` | `s0` |
| `sub_18` | `aten.sub.Tensor` | `self=unsqueeze_25:[1,(s0+1)], other=add_48:[1,1]` | `sub_18:[1,(s0+1)]` | `s0` |
| `zeros_like` | `aten.zeros_like.default` | `self=sub_18:[1,(s0+1)], pin_memory=False` | `zeros_like:[1,(s0+1)]` | `s0` |
| `min_1` | `aten.min.other` | `self=sub_18:[1,(s0+1)], other=zeros_like:[1,(s0+1)]` | `min_1:[1,(s0+1)]` | `s0` |
| `neg` | `aten.neg.default` | `self=min_1:[1,(s0+1)]` | `neg:[1,(s0+1)]` | `s0` |
| `lt` | `aten.lt.Scalar` | `self=neg:[1,(s0+1)], other=16` | `lt:[1,(s0+1)]` | `s0` |
| `nodes[103]` | `aten._assert_tensor_metadata.default` | `a=neg:[1,(s0+1)], size=None, stride=None, dtype={"as_scalar_type":5}, device={"as_device":{"index":null,"type":"cpu"}}, layout={"as_layout":7}` | `—` | `s0` |
| `_to_copy_2` | `aten._to_copy.default` | `self=neg:[1,(s0+1)], dtype={"as_scalar_type":7}` | `_to_copy_2:[1,(s0+1)]` | `s0` |
| `div` | `aten.div.Tensor` | `self=_to_copy_2:[1,(s0+1)], other=16` | `div:[1,(s0+1)]` | `s0` |
| `log` | `aten.log.default` | `self=div:[1,(s0+1)]` | `log:[1,(s0+1)]` | `s0` |
| `div_1` | `aten.div.Tensor` | `self=log:[1,(s0+1)], other=2.0794415416798357` | `div_1:[1,(s0+1)]` | `s0` |
| `mul_65` | `aten.mul.Tensor` | `self=div_1:[1,(s0+1)], other=16` | `mul_65:[1,(s0+1)]` | `s0` |
| `nodes[109]` | `aten._assert_tensor_metadata.default` | `a=mul_65:[1,(s0+1)], size=None, stride=None, dtype={"as_scalar_type":7}, device={"as_device":{"index":null,"type":"cpu"}}, layout={"as_layout":7}` | `—` | `s0` |
| `_to_copy_3` | `aten._to_copy.default` | `self=mul_65:[1,(s0+1)], dtype={"as_scalar_type":5}` | `_to_copy_3:[1,(s0+1)]` | `s0` |
| `add_75` | `aten.add.Tensor` | `self=_to_copy_3:[1,(s0+1)], other=16` | `add_75:[1,(s0+1)]` | `s0` |
| `full_like` | `aten.full_like.default` | `self=add_75:[1,(s0+1)], fill_value=31, pin_memory=False` | `full_like:[1,(s0+1)]` | `s0` |
| `min_2` | `aten.min.other` | `self=add_75:[1,(s0+1)], other=full_like:[1,(s0+1)]` | `min_2:[1,(s0+1)]` | `s0` |
| `where_2` | `aten.where.self` | `condition=lt:[1,(s0+1)], self=neg:[1,(s0+1)], other=min_2:[1,(s0+1)]` | `where_2:[1,(s0+1)]` | `s0` |
| `add_84` | `aten.add.Tensor` | `self=where_2:[1,(s0+1)], other=0` | `add_84:[1,(s0+1)]` | `s0` |
| `embedding_1` | `aten.embedding.default` | `weight=p_model_decoder_block_0_layer_0_selfattention_relative_attention_bias_weight:[32,2], indices=add_84:[1,(s0+1)]` | `embedding_1:[1,(s0+1),2]` | `s0` |
| `permute` | `aten.permute.default` | `self=embedding_1:[1,(s0+1),2], dims=[2,0,1]` | `permute:[2,1,(s0+1)]` | `s0` |
| `unsqueeze_26` | `aten.unsqueeze.default` | `self=permute:[2,1,(s0+1)], dim=0` | `unsqueeze_26:[1,2,1,(s0+1)]` | `s0` |
| `transpose_3` | `aten.transpose.int` | `self=cat_4:[1,2,(s0+1),32], dim0=2, dim1=3` | `transpose_3:[1,2,32,(s0+1)]` | `s0` |
| `matmul` | `aten.matmul.default` | `self=transpose:[1,2,1,32], other=transpose_3:[1,2,32,(s0+1)]` | `matmul:[1,2,1,(s0+1)]` | `s0` |
| `mul_95` | `aten.mul.Tensor` | `self=matmul:[1,2,1,(s0+1)], other=1.0` | `mul_95:[1,2,1,(s0+1)]` | `s0` |
| `add_106` | `aten.add.Tensor` | `self=mul_95:[1,2,1,(s0+1)], other=unsqueeze_26:[1,2,1,(s0+1)]` | `add_106:[1,2,1,(s0+1)]` | `s0` |
| `add_111` | `aten.add.Tensor` | `self=add_106:[1,2,1,(s0+1)], other=where:[1,1,1,(s0+1)]` | `add_111:[1,2,1,(s0+1)]` | `s0` |
| `softmax` | `aten.softmax.int` | `self=add_111:[1,2,1,(s0+1)], dim=-1` | `softmax:[1,2,1,(s0+1)]` | `s0` |
| `clone_7` | `aten.clone.default` | `self=softmax:[1,2,1,(s0+1)]` | `clone_7:[1,2,1,(s0+1)]` | `s0` |
| `matmul_1` | `aten.matmul.default` | `self=clone_7:[1,2,1,(s0+1)], other=cat_5:[1,2,(s0+1),32]` | `matmul_1:[1,2,1,32]` | `s0` |

</details>

<a id="artifact-19"></a>

## whisper-tiny/audio-encoder-decoder/tiny/decode/fp32/dynamo/dynamic

[Saved graph](models/whisper-tiny/audio-encoder-decoder/tiny/decode/fp32/dynamo/dynamic/models/model.json) · [Contract](models/whisper-tiny/audio-encoder-decoder/tiny/decode/fp32/dynamo/dynamic/contract.json)

Graph SHA256: `ccdccd7ab23829b838d81e8a1b9ac70a98f9e24cdf68c830dafdc1b9894088bc`.

| Symbol or expression | Minimum | Maximum |
| --- | ---: | ---: |
| `s0` | `1` | `8` |
| `s0 + 1` | `2` | `9` |

| Operator | Affected nodes | Symbols | Example node |
| --- | ---: | --- | --- |
| `_operator.add` | 1 | `s0` | `add_75` |
| `_operator.eq` | 2 | `s0` | `eq_25` |
| `_operator.le` | 2 | `s0` | `le_4` |
| `aten.__and__.Tensor` | 2 | `s0` | `and_1` |
| `aten._assert_tensor_metadata.default` | 3 | `s0` | `nodes[30]` |
| `aten._to_copy.default` | 1 | `s0` | `_to_copy` |
| `aten.add.Tensor` | 4 | `s0` | `add_10` |
| `aten.arange.default` | 1 | `s0` | `arange_4` |
| `aten.cat.default` | 4 | `s0` | `cat` |
| `aten.clone.default` | 1 | `s0` | `clone_6` |
| `aten.expand.default` | 1 | `s0` | `expand` |
| `aten.index.Tensor` | 1 | `s0` | `index_1` |
| `aten.le.Tensor` | 1 | `s0` | `le_3` |
| `aten.matmul.default` | 2 | `s0` | `matmul` |
| `aten.mul.Tensor` | 1 | `s0` | `mul_50` |
| `aten.softmax.int` | 1 | `s0` | `softmax` |
| `aten.sym_size.int` | 4 | `s0` | `sym_size_int_8` |
| `aten.transpose.int` | 1 | `s0` | `transpose_3` |
| `aten.unsqueeze.default` | 3 | `s0` | `unsqueeze_10` |
| `aten.where.ScalarOther` | 1 | `s0` | `where` |

<details>
<summary>Every affected node: tensor shapes and named argument configurations</summary>

| Node | Operator | Inputs and argument configurations | Outputs | Symbols |
| --- | --- | --- | --- | --- |
| `sym_size_int_8` | `aten.sym_size.int` | `self=decoder_attention_mask:[1,(s0+1)], dim=1` | `sym_size_int_8=(s0+1)` | `s0` |
| `sym_size_int_9` | `aten.sym_size.int` | `self=past_0_self_key:[1,2,s0,16], dim=2` | `sym_size_int_9=s0` | `s0` |
| `sym_size_int_10` | `aten.sym_size.int` | `self=past_0_self_value:[1,2,s0,16], dim=2` | `sym_size_int_10=s0` | `s0` |
| `sym_size_int` | `aten.sym_size.int` | `self=decoder_attention_mask:[1,(s0+1)], dim=1` | `sym_size_int=(s0+1)` | `s0` |
| `add_75` | `_operator.add` | `a=1, b=s0` | `add_75=(s0+1)` | `s0` |
| `le_4` | `_operator.le` | `a=(s0+1), b=(s0+1)` | `le_4=True` | `s0` |
| `eq_25` | `_operator.eq` | `a=s0, b=s0` | `eq_25=True` | `s0` |
| `le_2` | `_operator.le` | `a=(s0+1), b=(s0+1)` | `le_2=True` | `s0` |
| `eq_2` | `_operator.eq` | `a=s0, b=s0` | `eq_2=True` | `s0` |
| `cat` | `aten.cat.default` | `tensors=[clone:[0],past_0_self_key:[1,2,s0,16]], dim=-2` | `cat:[1,2,s0,16]` | `s0` |
| `cat_1` | `aten.cat.default` | `tensors=[clone_1:[0],past_0_self_value:[1,2,s0,16]], dim=-2` | `cat_1:[1,2,s0,16]` | `s0` |
| `add_10` | `aten.add.Tensor` | `self=arange:[1], other=s0` | `add_10:[1]` | `s0` |
| `nodes[30]` | `aten._assert_tensor_metadata.default` | `a=decoder_attention_mask:[1,(s0+1)], size=None, stride=None, dtype={"as_scalar_type":5}, device={"as_device":{"index":null,"type":"cpu"}}, layout={"as_layout":7}` | `—` | `s0` |
| `_to_copy` | `aten._to_copy.default` | `self=decoder_attention_mask:[1,(s0+1)], dtype={"as_scalar_type":12}, device={"as_device":{"index":null,"type":"cpu"}}` | `_to_copy:[1,(s0+1)]` | `s0` |
| `add_15` | `aten.add.Tensor` | `self=arange_3:[1], other=s0` | `add_15:[1]` | `s0` |
| `arange_4` | `aten.arange.default` | `end=(s0+1), device={"as_device":{"index":null,"type":"cpu"}}, pin_memory=False` | `arange_4:[(s0+1)]` | `s0` |
| `add_18` | `aten.add.Tensor` | `self=arange_4:[(s0+1)], other=0` | `add_18:[(s0+1)]` | `s0` |
| `unsqueeze_10` | `aten.unsqueeze.default` | `self=add_18:[(s0+1)], dim=0` | `unsqueeze_10:[1,(s0+1)]` | `s0` |
| `unsqueeze_11` | `aten.unsqueeze.default` | `self=unsqueeze_10:[1,(s0+1)], dim=1` | `unsqueeze_11:[1,1,(s0+1)]` | `s0` |
| `unsqueeze_12` | `aten.unsqueeze.default` | `self=unsqueeze_11:[1,1,(s0+1)], dim=2` | `unsqueeze_12:[1,1,1,(s0+1)]` | `s0` |
| `le_3` | `aten.le.Tensor` | `self=unsqueeze_12:[1,1,1,(s0+1)], other=unsqueeze_9:[1,1,1,1]` | `le_3:[1,1,1,(s0+1)]` | `s0` |
| `nodes[48]` | `aten._assert_tensor_metadata.default` | `a=le_3:[1,1,1,(s0+1)], size=None, stride=None, dtype={"as_scalar_type":12}, device={"as_device":{"index":null,"type":"cpu"}}, layout={"as_layout":7}` | `—` | `s0` |
| `and_1` | `aten.__and__.Tensor` | `self=new_ones:[], other=le_3:[1,1,1,(s0+1)]` | `and_1:[1,1,1,(s0+1)]` | `s0` |
| `index_1` | `aten.index.Tensor` | `self=_to_copy:[1,(s0+1)], indices=[unsqueeze_3:[1,1,1,1],unsqueeze_12:[1,1,1,(s0+1)]]` | `index_1:[1,1,1,(s0+1)]` | `s0` |
| `nodes[51]` | `aten._assert_tensor_metadata.default` | `a=index_1:[1,1,1,(s0+1)], size=None, stride=None, dtype={"as_scalar_type":12}, device={"as_device":{"index":null,"type":"cpu"}}, layout={"as_layout":7}` | `—` | `s0` |
| `and_2` | `aten.__and__.Tensor` | `self=and_1:[1,1,1,(s0+1)], other=index_1:[1,1,1,(s0+1)]` | `and_2:[1,1,1,(s0+1)]` | `s0` |
| `expand` | `aten.expand.default` | `self=and_2:[1,1,1,(s0+1)], size=[1,-1,1,(s0+1)]` | `expand:[1,1,1,(s0+1)]` | `s0` |
| `where` | `aten.where.ScalarOther` | `condition=expand:[1,1,1,(s0+1)], self=clone_5:[], other=-3.4028234663852886e+38` | `where:[1,1,1,(s0+1)]` | `s0` |
| `cat_4` | `aten.cat.default` | `tensors=[cat:[1,2,s0,16],transpose_1:[1,2,1,16]], dim=-2` | `cat_4:[1,2,(s0+1),16]` | `s0` |
| `cat_5` | `aten.cat.default` | `tensors=[cat_1:[1,2,s0,16],transpose_2:[1,2,1,16]], dim=-2` | `cat_5:[1,2,(s0+1),16]` | `s0` |
| `transpose_3` | `aten.transpose.int` | `self=cat_4:[1,2,(s0+1),16], dim0=2, dim1=3` | `transpose_3:[1,2,16,(s0+1)]` | `s0` |
| `matmul` | `aten.matmul.default` | `self=transpose:[1,2,1,16], other=transpose_3:[1,2,16,(s0+1)]` | `matmul:[1,2,1,(s0+1)]` | `s0` |
| `mul_50` | `aten.mul.Tensor` | `self=matmul:[1,2,1,(s0+1)], other=1.0` | `mul_50:[1,2,1,(s0+1)]` | `s0` |
| `add_59` | `aten.add.Tensor` | `self=mul_50:[1,2,1,(s0+1)], other=where:[1,1,1,(s0+1)]` | `add_59:[1,2,1,(s0+1)]` | `s0` |
| `softmax` | `aten.softmax.int` | `self=add_59:[1,2,1,(s0+1)], dim=-1` | `softmax:[1,2,1,(s0+1)]` | `s0` |
| `clone_6` | `aten.clone.default` | `self=softmax:[1,2,1,(s0+1)]` | `clone_6:[1,2,1,(s0+1)]` | `s0` |
| `matmul_1` | `aten.matmul.default` | `self=clone_6:[1,2,1,(s0+1)], other=cat_5:[1,2,(s0+1),16]` | `matmul_1:[1,2,1,16]` | `s0` |

</details>
