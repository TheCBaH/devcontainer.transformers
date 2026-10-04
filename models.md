# Transformers architecture probes

Population: **tiny**, deterministic random weights. 8/8 attempted artifacts verified. Coverage describes this curated population, not the full Transformers library.

CPU eager attention; policies: dynamo; dtypes: fp32; strict=False, no caches, functional tensor-tuple boundary. FLOPs are not measured. These probes do not establish pretrained accuracy.

| Model | Category | Parameters | Weight MiB | ATen / functional / core nodes | Result |
| --- | --- | ---: | ---: | --- | --- |
| bert-tiny | text-encoder | 331136 | 1.263 | 99 / 92 / 150 | ok |
| mobilevit-xxs | image-classification | 1272024 | 4.852 | 386 / 394 / 708 | ok |
| smollm2-135m | text-decoder | 90432 | 0.345 | 191 / 173 / 246 | ok |
| t5-small | text-encoder-decoder | 98880 | 0.377 | 279 / 251 / 335 | ok |
| time-series-small | time-series | 30456 | 0.116 | 297 / 259 / 440 | ok |
| tinyclip | image-text-embeddings | 143489 | 0.547 | 127 / 115 / 174 | ok |
| videomae-small | video-classification | 132554 | 0.506 | 39 / 39 / 67 | ok |
| whisper-tiny | audio-encoder-decoder | 42464 | 0.162 | 150 / 142 / 227 | ok |

Original checkpoint pins remain in `model-candidates.yaml`; tiny probes use separately reviewed configs. Time-series outputs are model states, location and scale; forecasting requires its distribution head and host sampling loop.
