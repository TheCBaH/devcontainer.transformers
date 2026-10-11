# Transformers architecture probes

Population: **tiny**, deterministic random weights. 37/37 attempted artifacts verified. Coverage describes this curated population, not the full Transformers library.

CPU eager attention; policies: dynamo; dtypes: fp32; strict=False, no caches, functional tensor-tuple boundary. FLOPs are not measured. These probes do not establish pretrained accuracy.

| Model | Category | Parameters | Weight MiB | ATen / functional / core nodes | Result |
| --- | --- | ---: | ---: | --- | --- |
| albert-base | text-encoder | 13280 | 0.051 | 112 / 105 / 166 | ok |
| ast-audioset | audio-classification | 12485 | 0.048 | 70 / 55 / 85 | ok |
| bart-base | text-encoder-decoder | 85376 | 0.326 | 401 / 376 / 650 | ok |
| bert-tiny | text-encoder | 331136 | 1.263 | 99 / 92 / 150 | ok |
| clap-htsat | audio-text-embeddings | 332641 | 1.269 | 349 / 340 / 658 | ok |
| convnextv2-tiny | image-classification | 63027 | 0.240 | 83 / 83 / 108 | ok |
| depth-anything-small | depth-estimation | 495361 | 1.890 | 232 / 217 / 330 | ok |
| dinov2-small | image-embeddings | 44672 | 0.170 | 91 / 76 / 133 | ok |
| distilbert-base | text-encoder | 23296 | 0.089 | 92 / 85 / 142 | ok |
| esm2-8m | protein-encoder | 19273 | 0.074 | 191 / 162 / 226 | ok |
| gpt2 | text-decoder | 31616 | 0.121 | 130 / 122 / 146 | ok |
| layoutlmv3-base | document-layout | 64928 | 0.248 | 201 / 191 / 222 | ok |
| mamba-130m | state-space-decoder | 223808 | 0.854 | 226 / 191 / 316 | ok |
| marian-fr-en | text-encoder-decoder | 72288 | 0.276 | 338 / 317 / 548 | ok |
| minilm-l6-v2 | sentence-embeddings | 24416 | 0.093 | 110 / 100 / 157 | ok |
| mobilevit-xxs | image-classification | 1272024 | 4.852 | 386 / 394 / 708 | ok |
| modernbert-embed | sentence-embeddings | 24736 | 0.094 | 214 / 178 / 244 | ok |
| mpnet-base | sentence-embeddings | 24480 | 0.093 | 144 / 134 / 191 | ok |
| nomic-embed | sentence-embeddings | 24960 | 0.095 | 158 / 148 / 218 | ok |
| owlv2-base | text-conditioned-detection | 56200 | 0.214 | 167 / 145 / 244 | ok |
| pythia-160m | text-decoder | 25344 | 0.097 | 147 / 135 / 188 | ok |
| qwen2-05b | text-decoder | 22816 | 0.087 | 194 / 173 / 246 | ok |
| resnet-18 | image-classification | 78507 | 0.299 | 41 / 41 / 42 | ok |
| roberta-base | text-encoder | 24384 | 0.093 | 110 / 102 / 160 | ok |
| sam-vit-base | prompted-segmentation | 94508 | 0.361 | 439 / 433 / 854 | ok |
| segformer-b0 | semantic-segmentation | 93957 | 0.358 | 218 / 214 / 354 | ok |
| smollm2-135m | text-decoder | 90432 | 0.345 | 191 / 173 / 246 | ok |
| smolvlm-256m | image-text-generation | 93312 | 0.356 | 257 / 225 / 301 | ok |
| swin-tiny | image-classification | 309738 | 1.182 | 249 / 233 / 364 | ok |
| t5-small | text-encoder-decoder | 98880 | 0.377 | 279 / 251 / 335 | ok |
| time-series-small | time-series | 30456 | 0.116 | 297 / 259 / 440 | ok |
| tinyclip | image-text-embeddings | 143489 | 0.547 | 127 / 115 / 174 | ok |
| videomae-small | video-classification | 132554 | 0.506 | 39 / 39 / 67 | ok |
| vit-base | image-classification | 24003 | 0.092 | 93 / 77 / 135 | ok |
| wav2vec2-base | audio-ctc | 20208 | 0.077 | 78 / 62 / 99 | ok |
| whisper-tiny | audio-encoder-decoder | 42464 | 0.162 | 150 / 142 / 227 | ok |
| yolos-tiny | object-detection | 114058 | 0.435 | 59 / 59 / 265 | ok |

Original checkpoint pins remain in `model-candidates.yaml`; tiny probes use separately reviewed configs. Time-series outputs are model states, location and scale; forecasting requires its distribution head and host sampling loop.

## Popular checkpoints and varied workflows

Selection uses published full safetensors below 1,000,000,000 bytes in total. Download counts are the catalogue snapshot, where available. Exports use reviewed tiny configurations and random weights. Sentence pooling and normalization are included; tokenization, OCR, waveform feature extraction, sampling and mask/box decoding remain host operations.

| Architecture | Model | HF checkpoint | Safetensors bytes | Hub downloads | Workflow |
| --- | --- | --- | ---: | ---: | --- |
| audio-spectrogram-transformer | ast-audioset | [MIT/ast-finetuned-audioset-10-10-0.4593](https://huggingface.co/MIT/ast-finetuned-audioset-10-10-0.4593/tree/f826b80d28226b62986cc218e5cec390b1096902) | 346,404,948 | 1091207 | Spectrogram-patch audio classification with two special tokens. |
| wav2vec2 | wav2vec2-base | [facebook/wav2vec2-base-960h](https://huggingface.co/facebook/wav2vec2-base-960h/tree/22aad52d435eb6dbaf354bdad9b0da84ce7d6156) | 377,607,901 | — | Base is the size compromise here; tiny config for CI. CTC decoding is outside graph. |
| clap | clap-htsat | [laion/clap-htsat-fused](https://huggingface.co/laion/clap-htsat-fused/tree/365dea6ef167def6676140ed93bbc43f84dabb28) | 614,496,152 | 8185193 | Contrastive text/audio embeddings from a single normalized mel spectrogram; reviewed tiny config disables the original checkpoint's audio fusion. |
| depth_anything | depth-anything-small | [depth-anything/Depth-Anything-V2-Small-hf](https://huggingface.co/depth-anything/Depth-Anything-V2-Small-hf/tree/5426e4f0f36572d16453bbda7a8389317b1bef99) | 99,173,660 | — | 224 is divisible by 14; default backbone image size is 518. Smaller probe resolution needs export and numerical verification. |
| layoutlmv3 | layoutlmv3-base | [microsoft/layoutlmv3-base](https://huggingface.co/microsoft/layoutlmv3-base/tree/cfbbbff0762e6aab37086fdd4739ad14fe7d5db4) | 501,338,056 | 938370 | Joint document tokens, integer bounding boxes and image patches; OCR remains host preprocessing. |
| idefics3 | smolvlm-256m | [HuggingFaceTB/SmolVLM-256M-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM-256M-Instruct/tree/7e3e67edbbed1bf9888184d9df282b700a323964) | 513,028,808 | — | Use pinned AutoProcessor to derive images, crops, masks and image-token IDs. Tiny nested config first; pretrained model is opt-in. |
| yolos | yolos-tiny | [hustvl/yolos-tiny](https://huggingface.co/hustvl/yolos-tiny/tree/95a90f3c189fbfca3bcfc6d7315b9e84d95dc2de) | 25,978,888 | — | 224px is proposed structural probe size; processor-derived pretrained size must be recorded separately. |
| sam | sam-vit-base | [facebook/sam-vit-base](https://huggingface.co/facebook/sam-vit-base/tree/70c1a07f894ebb5b307fd9eaaee97b9dfc16068f) | 374,979,480 | 239626 | Image plus labeled point prompts; exports mask logits and mask-quality scores. |
| esm | esm2-8m | [facebook/esm2_t6_8M_UR50D](https://huggingface.co/facebook/esm2_t6_8M_UR50D/tree/c731040fcd8d73dceaa04b0a8e6329b345b0f5df) | 31,384,292 | 462375 | Protein token encoder with rotary positions and mask-dependent token rescaling. |
| segformer | segformer-b0 | [nvidia/segformer-b0-finetuned-ade-512-512](https://huggingface.co/nvidia/segformer-b0-finetuned-ade-512-512/tree/489d5cd81a0b59fab9b7ea758d3548ebe99677da) | 15,036,944 | — | 224px is proposed structural probe size; pretrained processor normally targets 512. |
| bert | minilm-l6-v2 | [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/tree/1110a243fdf4706b3f48f1d95db1a4f5529b4d41) | 90,868,376 | 225633601 | Most-downloaded eligible checkpoint; masked mean pooling and L2-normalized sentence embeddings. |
| modernbert | modernbert-embed | [ibm-granite/granite-embedding-small-english-r2](https://huggingface.co/ibm-granite/granite-embedding-small-english-r2/tree/2ab6fa8ea2d674564defd37171ae19079b864b33) | 95,332,048 | 5141679 | Popular ModernBERT embedding checkpoint; alternating local/global attention and normalized pooling. |
| mpnet | mpnet-base | [sentence-transformers/all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2/tree/e8c3b32edf5434bc2275fc9bab85f82640a19130) | 437,971,872 | 18381804 | Popular sentence embedding family with relative-position attention and normalized pooling. |
| nomic_bert | nomic-embed | [nomic-ai/nomic-embed-text-v1.5](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5/tree/e9b6763023c676ca8431644204f50c2b100d9aab) | 546,938,168 | 12877830 | Popular rotary text embeddings; tensor encoder and normalized pooling only. |
| mamba | mamba-130m | [state-spaces/mamba-130m-hf](https://huggingface.co/state-spaces/mamba-130m-hf/tree/1e76775f628fbf1350fbe4dbb3d971ba64af25a1) | 516,567,560 | 273923 | Selective state-space recurrence and causal convolution, full-sequence forward without cache. |
| owlv2 | owlv2-base | [google/owlv2-base-patch16-ensemble](https://huggingface.co/google/owlv2-base-patch16-ensemble/tree/cfd3195ba4ea9592eec887ded089f4c08eff231d) | 619,918,824 | 2009909 | Text-conditioned object detection with per-patch boxes and objectness scores. |
| gpt_neox | pythia-160m | [EleutherAI/pythia-160m](https://huggingface.co/EleutherAI/pythia-160m/tree/50f5173d932e8e61f858120bcb800b97af589f46) | 374,998,696 | 3461088 | Popular Pythia checkpoint; parallel-residual rotary decoder, no cache. |
| qwen2 | qwen2-05b | [Qwen/Qwen2.5-0.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct/tree/7ae557604adf67be50417f59c2c2f167def9a775) | 988,097,824 | 7302712 | Popular Qwen2.5 checkpoint; grouped-query rotary decoder, no cache. |
| marian | marian-fr-en | [Helsinki-NLP/opus-mt-fr-en](https://huggingface.co/Helsinki-NLP/opus-mt-fr-en/tree/c4aed37b318c763fd177aa449b44e3b783cc6c02) | 300,803,608 | 839480 | Popular French-English translation with sinusoidal positions and teacher-forced decoder tensors. |
