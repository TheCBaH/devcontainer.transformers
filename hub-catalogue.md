# Hugging Face checkpoint catalogue

Transformers 5.18.0; scanned 2026-10-11T02:14:20.789413+00:00.

Every included checkpoint has published full safetensors weights totaling strictly less than 1,000,000,000 bytes across the entire repository. Configs and shard indices were downloaded; weights were not.

All 725 pinned AutoConfig architectures are considered. Search examines up to 100 checkpoints per architecture, ordered by Hub downloads, and stops at the first qualifying checkpoint. Discovery uses architecture tags. Untagged checkpoints and private/gated repositories are outside this scan. A search limit or missing candidate is not proof that no qualifying checkpoint exists. Published tiny random test checkpoints and quantized checkpoints are included. Task type comes from Hub pipeline metadata; absent metadata is unspecified. Eligibility does not establish graph-export support or pretrained quality.

| Scan result | Architectures |
| --- | ---: |
| eligible | 599 |
| no-qualifying-checkpoint | 120 |
| search-limit | 6 |

## any-to-any

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| gemma4_assistant | [google/gemma-4-31B-it-assistant](https://huggingface.co/google/gemma-4-31B-it-assistant/tree/627c5ec1458b9086b841a91e0512fd31fd2fbbf1) | Gemma4AssistantForCausalLM | 939,042,560 |
| gemma4_unified_assistant | [google/gemma-4-12B-it-assistant](https://huggingface.co/google/gemma-4-12B-it-assistant/tree/46d4c6f13f0ac0ad827b915669b8df9b81c64c51) | Gemma4UnifiedAssistantForCausalLM | 845,719,296 |
| qwen2_5_omni | [tiny-random/qwen2.5-omni](https://huggingface.co/tiny-random/qwen2.5-omni/tree/ecb05fbb904eacaa048960cfc0d608b073cb4bb1) | Qwen2_5OmniForConditionalGeneration | 11,240,320 |

## audio-classification

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| audio-spectrogram-transformer | [MIT/ast-finetuned-audioset-10-10-0.4593](https://huggingface.co/MIT/ast-finetuned-audioset-10-10-0.4593/tree/f826b80d28226b62986cc218e5cec390b1096902) | ASTForAudioClassification | 346,404,948 |
| clap | [laion/clap-htsat-fused](https://huggingface.co/laion/clap-htsat-fused/tree/365dea6ef167def6676140ed93bbc43f84dabb28) | ClapModel | 614,496,152 |
| data2vec-audio | [VasilisAsim/data2vec-finetuned-CREMA-D](https://huggingface.co/VasilisAsim/data2vec-finetuned-CREMA-D/tree/51b95f49d8d89082883d55e563a102e4381ae14f) | Data2VecAudioForSequenceClassification | 373,480,528 |
| qwen3_asr | [aufklarer/Qwen3-ForcedAligner-0.6B-4bit](https://huggingface.co/aufklarer/Qwen3-ForcedAligner-0.6B-4bit/tree/f0e9f12a0ddbcb5f1e1b7f0339090628f1cede1d) | Qwen3ASRForConditionalGeneration | 978,674,048 |
| unispeech-sat | [VasilisAsim/unispeech_sat-finetuned-IEMOCAP](https://huggingface.co/VasilisAsim/unispeech_sat-finetuned-IEMOCAP/tree/f3ebfec084e537374bf4107f9ef71197b4b6d8e3) | UniSpeechSatForSequenceClassification | 378,305,424 |
| wavlm | [abhishtagatya/wavlm-base-960h-itw-deepfake](https://huggingface.co/abhishtagatya/wavlm-base-960h-itw-deepfake/tree/1a9795f0ce971f9a1e2a512c443dbd889777cf50) | WavLMForSequenceClassification | 378,347,256 |

## automatic-speech-recognition

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| cohere_asr | [MarkChen1214/cohere-transcribe-03-2026-MLX-Mixed-3bit4bit](https://huggingface.co/MarkChen1214/cohere-transcribe-03-2026-MLX-Mixed-3bit4bit/tree/103799cb62be5f57dedc5b88ea64d38b251de826) | CohereAsrForConditionalGeneration | 931,566,235 |
| granite_speech | [onnx-internal-testing/tiny-random-GraniteSpeechForConditionalGeneration](https://huggingface.co/onnx-internal-testing/tiny-random-GraniteSpeechForConditionalGeneration/tree/73332fe065545fcc2be24a0f68c647884f24ee67) | GraniteSpeechForConditionalGeneration | 51,787,248 |
| granite_speech5_ctc | [ibm-granite/granite-speech-5.0-470m-turboctc](https://huggingface.co/ibm-granite/granite-speech-5.0-470m-turboctc/tree/947f59af40db9791170a0628cf0f3f4812d720f1) | GraniteSpeech5ForCTC | 946,180,704 |
| lasr_ctc | [samwell/medasr-ghana](https://huggingface.co/samwell/medasr-ghana/tree/94d86ad384152ea073e9a9b4d07672cdfeec26d9) | LasrForCTC | 421,172,456 |
| moonshine | [moonshine-ai/moonshine-tiny](https://huggingface.co/moonshine-ai/moonshine-tiny/tree/390624ed33d594443aa4aa221f5b9f283b545b5a) | MoonshineForConditionalGeneration | 108,389,192 |
| moonshine_streaming | [moonshine-ai/moonshine-streaming-tiny](https://huggingface.co/moonshine-ai/moonshine-streaming-tiny/tree/f8e9dfd8c562c257c151a907b7b7f2fe8ff8511a) | unspecified | 176,237,308 |
| parakeet_ctc | [ctaguchi/parakeet-hf-ctc-110m-en](https://huggingface.co/ctaguchi/parakeet-hf-ctc-110m-en/tree/a755f5a4398ebe44292169d4fceea34e3c02b759) | ParakeetForCTC | 437,298,244 |
| parakeet_rnnt | [linagora/linto_stt_fr_fastconformer_pc](https://huggingface.co/linagora/linto_stt_fr_fastconformer_pc/tree/b37566382e88e99f8625450081c3420d4e1a0c4b) | ParakeetForRNNT | 456,529,908 |
| parakeet_tdt | [moondream/parakeet-redux](https://huggingface.co/moondream/parakeet-redux/tree/2bf128600aac4b16946f7ed8372e56117fe5e23b) | unspecified | 177,774,490 |
| seamless_m4t | [badaoui/tiny-random-seamless-m4t](https://huggingface.co/badaoui/tiny-random-seamless-m4t/tree/c28f42493d810774b475004007b510ae2519e6ec) | SeamlessM4TModel | 108 |
| sew-d | [optimum-intel-internal-testing/sew-d-tiny-100k-ft-ls100h](https://huggingface.co/optimum-intel-internal-testing/sew-d-tiny-100k-ft-ls100h/tree/65384f55f667b8af9669f2e2e661b34103b62a05) | SEWDForCTC | 96,537,316 |
| speech_to_text | [facebook/s2t-small-librispeech-asr](https://huggingface.co/facebook/s2t-small-librispeech-asr/tree/256e91a603c013ae09aa1e4c09cfc3f8acdf8d19) | Speech2TextForConditionalGeneration | 118,185,584 |
| voxtral_realtime | [onnx-internal-testing/tiny-random-VoxtralRealtimeForConditionalGeneration](https://huggingface.co/onnx-internal-testing/tiny-random-VoxtralRealtimeForConditionalGeneration/tree/cb79c8896184e5b5ebf5eb2e9cf4fe84a96e442b) | VoxtralRealtimeForConditionalGeneration | 34,221,080 |
| wav2vec2 | [facebook/wav2vec2-base-960h](https://huggingface.co/facebook/wav2vec2-base-960h/tree/22aad52d435eb6dbaf354bdad9b0da84ce7d6156) | Wav2Vec2ForCTC | 377,607,901 |
| wav2vec2-conformer | [42MARU/ko-spelling-wav2vec2-conformer-del-1s](https://huggingface.co/42MARU/ko-spelling-wav2vec2-conformer-del-1s/tree/174ec0b917167569c2d4b248d4892802018535ef) | Wav2Vec2ConformerForCTC | 719,424,586 |
| whisper | [openai/whisper-small](https://huggingface.co/openai/whisper-small/tree/973afd24965f72e36ca33b3055d56a652f456b4d) | WhisperForConditionalGeneration | 966,995,080 |

## depth-estimation

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| depth_anything | [depth-anything/Depth-Anything-V2-Small-hf](https://huggingface.co/depth-anything/Depth-Anything-V2-Small-hf/tree/5426e4f0f36572d16453bbda7a8389317b1bef99) | DepthAnythingForDepthEstimation | 99,173,660 |
| dpt | [Intel/dpt-swinv2-tiny-256](https://huggingface.co/Intel/dpt-swinv2-tiny-256/tree/f7f350e1a10a5ea58671b68ab5f49dc18ec00483) | DPTForDepthEstimation | 163,760,876 |
| glpn | [vinvino02/glpn-nyu](https://huggingface.co/vinvino02/glpn-nyu/tree/cb8ce03174424af9a3315da175ead88667f0578c) | GLPNForDepthEstimation | 244,998,965 |
| prompt_depth_anything | [depth-anything/prompt-depth-anything-vits-hf](https://huggingface.co/depth-anything/prompt-depth-anything-vits-hf/tree/6f3768a5383d95a904ec00d2a7ca3bd186f8797e) | PromptDepthAnythingForDepthEstimation | 100,368,820 |
| tipsv2_dpt | [google/tipsv2-b14-dpt](https://huggingface.co/google/tipsv2-b14-dpt/tree/da81b552538c453432e7a1efea39737c89580424) | TIPSv2DPTModel | 632,066,716 |

## document-question-answering

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| layoutlm | [impira/layoutlm-document-qa](https://huggingface.co/impira/layoutlm-document-qa/tree/beed3c4d02d86017ebca5bd0fdf210046b907aa6) | LayoutLMForQuestionAnswering | 511,200,628 |

## feature-extraction

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| bart | [facebook/bart-base](https://huggingface.co/facebook/bart-base/tree/aadd2ab0ae0c8268c7c9693540e9904811f36177) | BartModel | 557,709,915 |
| bigbird_pegasus | [optimum-intel-internal-testing/tiny-random-bigbird_pegasus](https://huggingface.co/optimum-intel-internal-testing/tiny-random-bigbird_pegasus/tree/e15fb7606b3c7e20e1f6cdf2c713d303fe4a9937) | BigBirdPegasusModel | 336,368 |
| blt | [nliampi/blt-model](https://huggingface.co/nliampi/blt-model/tree/0718b433e362026e2e841b454233a0f88e7efd28) | BltModel | 696 |
| canine | [google/canine-c](https://huggingface.co/google/canine-c/tree/dc0eaffdff3fa9161613311c7096eeb3e133ee19) | CanineModel | 528,491,046 |
| clip_vision_model | [tanganke/clip-vit-base-patch32_sun397](https://huggingface.co/tanganke/clip-vit-base-patch32_sun397/tree/4628de77c6c97ba178c65a0bdf5ce8f5c3045d63) | CLIPVisionModel | 349,847,824 |
| convbert | [dbmdz/convbert-base-turkish-cased](https://huggingface.co/dbmdz/convbert-base-turkish-cased/tree/ba09bc2348482fd46dea9083345a9e7aaffeaa7d) | ConvBertModel | 427,299,768 |
| dac | [descript/dac_44khz](https://huggingface.co/descript/dac_44khz/tree/c1bc521685adf9cfe247bc39a5ca58917eda1ac4) | DacModel | 306,507,276 |
| deberta | [peft-internal-testing/tiny-random-DebertaModel](https://huggingface.co/peft-internal-testing/tiny-random-DebertaModel/tree/2d3b963750756c1af21143dd770f225b22983111) | DebertaModel | 341,356 |
| dpr | [deepset/bert-small-mm_retrieval-question_encoder](https://huggingface.co/deepset/bert-small-mm_retrieval-question_encoder/tree/9c9246a3391607da77a5dad17dfbed601a09c8c3) | DPRQuestionEncoder | 115,068,616 |
| encodec | [facebook/encodec_24khz](https://huggingface.co/facebook/encodec_24khz/tree/c1dbe2ae3f1de713481a3b3e7c47f357092ee040) | EncodecModel | 93,119,608 |
| funnel | [funnel-transformer/intermediate](https://huggingface.co/funnel-transformer/intermediate/tree/8bce9f1c64e9c066f52956ff2a6caf716e4d2470) | FunnelModel | 708,276,094 |
| gemma3_text | [microsoft/harrier-oss-v1-270m](https://huggingface.co/microsoft/harrier-oss-v1-270m/tree/31de22b673913c7d658c0f03f792d77c2dcf8ebd) | Gemma3TextModel | 536,221,640 |
| gemma4_audio | [rnagabh/gemma4-audio-encoder](https://huggingface.co/rnagabh/gemma4-audio-encoder/tree/e3fb768d7c9e7aff20429cafa5739f58d29d985f) | Gemma4AudioModel | 614,451,368 |
| groupvit | [nvidia/groupvit-gcc-redcaps](https://huggingface.co/nvidia/groupvit-gcc-redcaps/tree/681e10603ff58911e89d8c4cdfaa93499387c315) | GroupViTModel | 223,034,852 |
| hgnet_v2 | [ustc-community/hgnet-v2](https://huggingface.co/ustc-community/hgnet-v2/tree/7ebb5cb34d5a226666fa878c7879a46a9471c8be) | HGNetV2Backbone | 133,762,736 |
| higgs_audio_v2_tokenizer | [eustlb/higgs-audio-v2-tokenizer](https://huggingface.co/eustlb/higgs-audio-v2-tokenizer/tree/528e871c2a26c4f0f7773b9754e2e1acae20899d) | HiggsAudioV2TokenizerModel | 805,665,628 |
| hubert | [ntu-spml/distilhubert](https://huggingface.co/ntu-spml/distilhubert/tree/fa87d96265d6b7af66e112faff6ff44df419cec9) | HubertModel | 93,973,272 |
| kimi_k25 | [nikita-savelyev-cerebras/tiny-random-kimi-k2.5](https://huggingface.co/nikita-savelyev-cerebras/tiny-random-kimi-k2.5/tree/296f5ce879e6aabe24eb5aec8a3c760cc98066e4) | KimiK25ForConditionalGeneration | 6,489,880 |
| lilt | [SCUT-DLVCLab/lilt-roberta-en-base](https://huggingface.co/SCUT-DLVCLab/lilt-roberta-en-base/tree/96328faae824978e47bd0e8ea09f66b85efda5f5) | LiltModel | 523,070,632 |
| mimi | [kyutai/mimi](https://huggingface.co/kyutai/mimi/tree/89091b3e466eb6a9d11e537bf26b144f194978f7) | MimiModel | 384,649,828 |
| minimax | [badaoui/tiny-random-minimax](https://huggingface.co/badaoui/tiny-random-minimax/tree/f9ba110a455f9c4469cca1c70d7810cb6c879838) | MiniMaxModel | 757,759,880 |
| modernbert | [ibm-granite/granite-embedding-small-english-r2](https://huggingface.co/ibm-granite/granite-embedding-small-english-r2/tree/2ab6fa8ea2d674564defd37171ae19079b864b33) | ModernBertModel | 95,332,048 |
| modernvbert | [naver/v-splade-quality](https://huggingface.co/naver/v-splade-quality/tree/99bdc93f42460e595b2fb1e78b96edd44e898441) | BiModernVBert | 660,271,690 |
| neomme | [Hcompany/NeoMME-260M](https://huggingface.co/Hcompany/NeoMME-260M/tree/5ba79fb246e23776d2c2fcead975eae2775ed94b) | NeoMMEModel | 525,893,660 |
| sew | [asapp/sew-tiny-100k](https://huggingface.co/asapp/sew-tiny-100k/tree/085f3cbb05d02db02b7b4d575d4c9bb9d7689df9) | SEWModel | 162,859,852 |
| squeezebert | [optimum-intel-internal-testing/tiny-random-squeezebert](https://huggingface.co/optimum-intel-internal-testing/tiny-random-squeezebert/tree/76ca5835944d66d07d4e8019a8f0a31dfa7f2bfa) | SqueezeBertModel | 322,400 |
| videoprism | [sposiboh/videoprism-base-f16r288-pt](https://huggingface.co/sposiboh/videoprism-base-f16r288-pt/tree/82d97c3e1c42b1e960801857541892fb4d7e9aff) | VideoPrismModel | 457,495,776 |
| videoprism_vision_model | [MHRDYN7/videoprism-base-f16r288](https://huggingface.co/MHRDYN7/videoprism-base-f16r288/tree/c5bb17adeb575aaf1d46b56c5b9dfa1b00465c80) | VideoPrismVisionModel | 457,489,232 |
| vjepa2 | [davevanveen/vjepa2.1-vitb-fpc64-384](https://huggingface.co/davevanveen/vjepa2.1-vitb-fpc64-384/tree/a88952a8a55e278a1cc40eefdd63d1b6d1b24470) | VJEPA2Model | 438,855,416 |
| wav2vec2-bert | [taiqihe/test-w2v-bert-dummy](https://huggingface.co/taiqihe/test-w2v-bert-dummy/tree/80bbcb3006944e46fec60bb020dd9030a46082e8) | Wav2Vec2BertModel | 97,390,168 |

## fill-mask

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| albert | [albert/albert-base-v2](https://huggingface.co/albert/albert-base-v2/tree/8e2f239c5f8a2c0f253781ca60135db913e5c80c) | AlbertForMaskedLM | 47,372,894 |
| camembert | [almanach/camembert-base](https://huggingface.co/almanach/camembert-base/tree/a75967561c78f2aa81cc41045378d3b4ee25af9e) | CamembertForMaskedLM | 445,008,750 |
| distilbert | [distilbert/distilbert-base-uncased](https://huggingface.co/distilbert/distilbert-base-uncased/tree/12040accade4e8a0f71eabdb258fecc2e7e948be) | DistilBertForMaskedLM | 267,954,768 |
| esm | [facebook/esm2_t6_8M_UR50D](https://huggingface.co/facebook/esm2_t6_8M_UR50D/tree/c731040fcd8d73dceaa04b0a8e6329b345b0f5df) | EsmForMaskedLM | 31,384,292 |
| flaubert | [flaubert/flaubert_base_cased](https://huggingface.co/flaubert/flaubert_base_cased/tree/f681df336b523e136915ae97bc8bd0ef4933ae36) | FlaubertWithLMHeadModel | 553,227,860 |
| megatron-bert | [KBLab/megatron-bert-base-swedish-cased-600k](https://huggingface.co/KBLab/megatron-bert-base-swedish-cased-600k/tree/f1c26877cc1424c6679096a342f8bb2c9c050e5d) | MegatronBertForMaskedLM | 541,456,476 |
| nystromformer | [LennartKeller/nystromformer-gottbert-base-8192](https://huggingface.co/LennartKeller/nystromformer-gottbert-base-8192/tree/242e69da80897dca49d73616df4de13fff841c9b) | NystromformerForMaskedLM | 527,877,380 |
| perceiver | [deepmind/language-perceiver](https://huggingface.co/deepmind/language-perceiver/tree/47a1ba43d8198ea10cf9a158fce114953e9441a1) | PerceiverForMaskedLM | 804,491,840 |
| roberta | [FacebookAI/roberta-base](https://huggingface.co/FacebookAI/roberta-base/tree/e2da8e2f811d1448a5b465c236feacd80ffbac7b) | RobertaForMaskedLM | 498,818,054 |
| roberta-prelayernorm | [mist-models/mist-28M-ti624ev1](https://huggingface.co/mist-models/mist-28M-ti624ev1/tree/bfeebb7a2619a61d321de922b66376f5cb682eef) | RobertaPreLayerNormForMaskedLM | 106,494,268 |
| roformer | [alchemab/antiberta2](https://huggingface.co/alchemab/antiberta2/tree/3123350a3ee741c02a5dcf5efc771f3fb588ae77) | RoFormerForMaskedLM | 810,602,392 |
| tapas | [google/tapas-base-masklm](https://huggingface.co/google/tapas-base-masklm/tree/254978772d3361c322eb97deba0f627db9d563d7) | TapasForMaskedLM | 442,840,320 |
| xlm | [FacebookAI/xlm-mlm-ende-1024](https://huggingface.co/FacebookAI/xlm-mlm-ende-1024/tree/a5465ccf2e3c8a11425cd65a225cb8fc8c110f7c) | XLMWithLMHeadModel | 834,706,860 |
| xmod | [ZurichNLP/swissbert](https://huggingface.co/ZurichNLP/swissbert/tree/c1294db2e2eb48bfed66ee0b536861601164b92c) | XmodForMaskedLM | 640,671,888 |

## image-classification

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| beit | [NTQAI/pedestrian_gender_recognition](https://huggingface.co/NTQAI/pedestrian_gender_recognition/tree/5bbae752fe1c7793c43f727b94198f385e53e2a6) | BeitForImageClassification | 346,807,898 |
| bit | [MITLL/LADI-v2-classifier-small-reference](https://huggingface.co/MITLL/LADI-v2-classifier-small-reference/tree/6ba5a0300601284bc6b69dddb46c8991a8ac196c) | BitForImageClassification | 94,116,688 |
| convnext | [facebook/convnext-small-224](https://huggingface.co/facebook/convnext-small-224/tree/e0df91dcc78dbc0f56be8fbecff706128aee7c28) | ConvNextForImageClassification | 200,935,760 |
| convnextv2 | [facebook/convnextv2-base-22k-384](https://huggingface.co/facebook/convnextv2-base-22k-384/tree/53ec0af6e1bd11bf7eba3e9131d29b69625accf3) | ConvNextV2ForImageClassification | 354,917,376 |
| cvt | [microsoft/cvt-13](https://huggingface.co/microsoft/cvt-13/tree/84e365a5f6a5ca987486abb25f3d8e5265cdc44d) | CvtForImageClassification | 80,166,694 |
| data2vec-vision | [tigeryi/imagenet1k](https://huggingface.co/tigeryi/imagenet1k/tree/ed7e62641f4fefa8d05a4e062f0f1ca37737c6dd) | Data2VecVisionForImageClassification | 692,305,248 |
| deit | [facebook/deit-base-distilled-patch16-384](https://huggingface.co/facebook/deit-base-distilled-patch16-384/tree/d939597a763b570654d2cbb10a22d59ee21ecd7e) | DeiTForImageClassificationWithTeacher | 350,543,872 |
| dinat | [aaa12963337/msi-dinat-mini](https://huggingface.co/aaa12963337/msi-dinat-mini/tree/ecb685ae835277b8cba8d8d0b9d50ffb91a9beea) | DinatForImageClassification | 77,928,656 |
| efficientnet | [docling-project/DocumentFigureClassifier-v2.5](https://huggingface.co/docling-project/DocumentFigureClassifier-v2.5/tree/f859dfbff5c9916cd996942d4b0db7fa25808220) | EfficientNetForImageClassification | 16,378,200 |
| levit | [facebook/levit-128S](https://huggingface.co/facebook/levit-128S/tree/46576b0c1bead4e89d89eb42e0a1ad4cb236fb20) | LevitForImageClassificationWithTeacher | 32,075,976 |
| mobilenet_v1 | [yuleysi/autotrain-6gama-idpx7](https://huggingface.co/yuleysi/autotrain-6gama-idpx7/tree/f4bebb6e1adf37eecd2b17e5c99c72083284ae12) | MobileNetV1ForImageClassification | 14,712,272 |
| mobilenet_v2 | [google/mobilenet_v2_1.0_224](https://huggingface.co/google/mobilenet_v2_1.0_224/tree/75e607b00aeae1297cc89d026a118bce012f5c5a) | MobileNetV2ForImageClassification | 14,199,388 |
| mobilevitv2 | [nguyenkhoa/mobilevitv2_Liveness_detection_v1.0](https://huggingface.co/nguyenkhoa/mobilevitv2_Liveness_detection_v1.0/tree/61f430ba87ad8bbb3bb3bd4cd7038cc4953a05e6) | MobileViTV2ForImageClassification | 17,659,076 |
| poolformer | [sail/poolformer_s12](https://huggingface.co/sail/poolformer_s12/tree/01bcf57546aceaccba581172497434bb0b377749) | PoolFormerForImageClassification | 47,675,728 |
| pvt | [Xrenya/pvt-tiny-224](https://huggingface.co/Xrenya/pvt-tiny-224/tree/634950b5fe4a8bb8264f2f1b3c0a89068181f455) | PvtForImageClassification | 52,937,336 |
| pvt_v2 | [OpenGVLab/pvt_v2_b0](https://huggingface.co/OpenGVLab/pvt_v2_b0/tree/bafa29fe7664535848bf1b64b72ade2ab27b9360) | PvtV2ForImageClassification | 14,690,352 |
| regnet | [facebook/regnet-y-320](https://huggingface.co/facebook/regnet-y-320/tree/e4809f918e6e26564a4cfe8d095e50d904018699) | RegNetForImageClassification | 580,883,312 |
| resnet | [microsoft/resnet-18](https://huggingface.co/microsoft/resnet-18/tree/65a5785d9156231087c481e0c7dd33a5ff6f7e3e) | ResNetForImageClassification | 46,812,324 |
| swiftformer | [MBZUAI/swiftformer-xs](https://huggingface.co/MBZUAI/swiftformer-xs/tree/103d0c70fb0eecade81e47590d194efcd9e62bdf) | SwiftFormerForImageClassification | 13,964,912 |
| swin | [Organika/sdxl-detector](https://huggingface.co/Organika/sdxl-detector/tree/b37fede8562cb72b89ec201c0987f96ba21b518a) | SwinForImageClassification | 694,997,632 |
| swinv2 | [Modotte/AIRealNet](https://huggingface.co/Modotte/AIRealNet/tree/1aeca517d3cf8e5bd9d033a73c0644c36d04143e) | Swinv2ForImageClassification | 780,886,280 |
| timm_wrapper | [Freepik/nsfw_image_detector](https://huggingface.co/Freepik/nsfw_image_detector/tree/15b85477e4fd2000db76ae9aae0f89a72f95e2e3) | TimmWrapperForImageClassification | 172,725,672 |
| vit | [google/vit-base-patch16-224](https://huggingface.co/google/vit-base-patch16-224/tree/3f49326eb077187dfe1c2a2bb15fbd74e6ab91e3) | ViTForImageClassification | 346,293,852 |
| vit_msn | [Danx15/vit-msn-small-finetuned-custom-logo](https://huggingface.co/Danx15/vit-msn-small-finetuned-custom-logo/tree/04b1f73e27bdb5227a018c921c78d7e9ee0b2895) | ViTMSNForImageClassification | 87,432,468 |

## image-feature-extraction

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| dinov2 | [facebook/dinov2-base](https://huggingface.co/facebook/dinov2-base/tree/f9e44c814b77203eaa57a6bdbbd535f21ede1415) | Dinov2Model | 346,345,912 |
| dinov2_with_registers | [facebook/dinov2-with-registers-base](https://huggingface.co/facebook/dinov2-with-registers-base/tree/a1d738ccfa7ae170945f210395d99dde8adb1805) | Dinov2WithRegistersModel | 346,358,296 |
| dinov3_convnext | [dflorea/dinov3-convnext-tiny-pretrain-lvd1689m-andina](https://huggingface.co/dflorea/dinov3-convnext-tiny-pretrain-lvd1689m-andina/tree/4eaeaffcdd7e21c1f51b8d5136f21dcab1561dd5) | DINOv3ConvNextModel | 111,299,216 |
| dinov3_vit | [Tooony133/dinov3-vits16-pretrain-lvd1689m](https://huggingface.co/Tooony133/dinov3-vits16-pretrain-lvd1689m/tree/fc6921f7a0b44d5b33ab4482cfed5443db6ccd81) | DINOv3ViTModel | 86,406,384 |
| hiera | [facebook/hiera-tiny-224-hf](https://huggingface.co/facebook/hiera-tiny-224-hf/tree/0c4c06ac3760513079095ee4f400c3445fb1577a) | HieraModel | 108,582,048 |
| imagegpt | [vumichien/imagegpt-small](https://huggingface.co/vumichien/imagegpt-small/tree/6355519762d55cd474dc7dcf9c9e51508b913083) | ImageGPTModel | 330,872,720 |
| kimi_k25_vision | [Aquiles-ai/MoonViT-3D](https://huggingface.co/Aquiles-ai/MoonViT-3D/tree/e60a27ae8f52eb2609ad2f7fe0159a6b883f10ce) | Kimi_K25VisionModel | 833,774,680 |
| qwen3_5_vision | [immanuelpeter/Qwen3.8-27B-Vision](https://huggingface.co/immanuelpeter/Qwen3.8-27B-Vision/tree/60a1bf9336197d19458290fd43f3d527f6cf3078) | Qwen3_5VisionModel | 921,492,896 |
| sapiens2 | [facebook/sapiens2-pretrain-0.1b](https://huggingface.co/facebook/sapiens2-pretrain-0.1b/tree/b16fc30feddc2cf9330b2980a26a8cc91f51e697) | Sapiens2Model | 911,987,168 |
| textnet | [czczup/textnet-base](https://huggingface.co/czczup/textnet-base/tree/6d2531fd3c7cb367bbfd570ca94ea7a0784b3099) | TextNetBackbone | 54,291,592 |

## image-segmentation

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| clipseg | [CIDAS/clipseg-rd64-refined](https://huggingface.co/CIDAS/clipseg-rd64-refined/tree/999e0328d9e10b484360c477313983f9afdd7050) | CLIPSegForImageSegmentation | 603,049,496 |
| eomt | [tue-mps/coco_panoptic_eomt_small_640_2x](https://huggingface.co/tue-mps/coco_panoptic_eomt_small_640_2x/tree/10f5326794a8ce7e0e975791033ae1c13aec3767) | EomtForUniversalSegmentation | 95,927,796 |
| eomt_dinov3 | [tue-mps/eomt-dinov3-coco-panoptic-base-640](https://huggingface.co/tue-mps/eomt-dinov3-coco-panoptic-base-640/tree/589ed003c94fc387d0daae28f12e9e01fc846332) | EomtDinov3ForUniversalSegmentation | 369,723,620 |
| mask2former | [facebook/mask2former-swin-large-cityscapes-semantic](https://huggingface.co/facebook/mask2former-swin-large-cityscapes-semantic/tree/062c2c0cf95dd6080a50b56ffc1fe2ad2d63513e) | Mask2FormerForUniversalSegmentation | 865,916,864 |
| maskformer | [facebook/maskformer-swin-tiny-coco](https://huggingface.co/facebook/maskformer-swin-tiny-coco/tree/347b42f4c1c918246faf1e295fe350df3e5d718f) | MaskFormerForInstanceSegmentation | 167,310,960 |
| segformer | [mattmdjaga/segformer_b2_clothes](https://huggingface.co/mattmdjaga/segformer_b2_clothes/tree/584abc1e1d260e23c0fc627c5217a09b2b461046) | SegformerForSemanticSegmentation | 109,493,236 |
| upernet | [openmmlab/upernet-convnext-tiny](https://huggingface.co/openmmlab/upernet-convnext-tiny/tree/876ffc56b819a829448f7e81e9f8606deef6fb65) | UperNetForSemanticSegmentation | 241,053,050 |
| videomt | [tue-mps/videomt-dinov2-small-ytvis2019](https://huggingface.co/tue-mps/videomt-dinov2-small-ytvis2019/tree/a8c9855154c4825bbdc738e5496840cbfa48987c) | VideomtForUniversalSegmentation | 96,377,356 |

## image-text-to-text

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| blip | [Huiaaa/flickr30k-blip-caption](https://huggingface.co/Huiaaa/flickr30k-blip-caption/tree/3d4cd8f1945311c8ec1b3adab28d9983da2eb5a2) | BlipForConditionalGeneration | 895,947,208 |
| diffusion_gemma | [trl-internal-testing/tiny-DiffusionGemmaForBlockDiffusion](https://huggingface.co/trl-internal-testing/tiny-DiffusionGemmaForBlockDiffusion/tree/95af0b2bf27db2637cd62d086e27db3cc85c94ae) | DiffusionGemmaForBlockDiffusion | 8,554,464 |
| florence2 | [microsoft/Florence-2-base](https://huggingface.co/microsoft/Florence-2-base/tree/5ca5edf5bd017b9919c05d08aebef5e4c7ac3bac) | Florence2ForConditionalGeneration | 463,221,266 |
| gemma3 | [trl-internal-testing/tiny-Gemma3ForConditionalGeneration](https://huggingface.co/trl-internal-testing/tiny-Gemma3ForConditionalGeneration/tree/c412866df0d2e34e050f9281885892d276f508ad) | Gemma3ForConditionalGeneration | 8,640,680 |
| gemma4 | [trl-internal-testing/tiny-Gemma4ForConditionalGeneration](https://huggingface.co/trl-internal-testing/tiny-Gemma4ForConditionalGeneration/tree/0dc1746b7f9f623b748e735ed5a4302eb4baf346) | Gemma4ForConditionalGeneration | 25,415,228 |
| glm4v | [tiny-random/glm-4v](https://huggingface.co/tiny-random/glm-4v/tree/fe554c413e09fa1e470ad6f51b94f59a0a30ab4b) | Glm4vForConditionalGeneration | 19,984,480 |
| glm4v_moe | [tiny-random/glm-4v-moe](https://huggingface.co/tiny-random/glm-4v-moe/tree/68a7fbd906ec038e031a97d2c09b1a1753347f1d) | Glm4vMoeForConditionalGeneration | 11,758,344 |
| glm5_next | [inference-optimization/GLM-5.3-Flash-0.1B-A0.1B](https://huggingface.co/inference-optimization/GLM-5.3-Flash-0.1B-A0.1B/tree/8311399447eba9c9b215e3209ab6f25e59c7d21e) | Glm5NextForConditionalGeneration | 168,778,084 |
| glm_ocr | [tiny-random/glm-ocr](https://huggingface.co/tiny-random/glm-ocr/tree/c5282ed42fc8dc4491d3ff77fd16fdd6ef6feccc) | GlmOcrForConditionalGeneration | 3,978,120 |
| idefics | [ArthurFischel/tiny-random-idefics-smw_10k-300steps](https://huggingface.co/ArthurFischel/tiny-random-idefics-smw_10k-300steps/tree/d28b8580ca20053e9e1d6a131bd7e95b602e0334) | IdeficsForVisionText2Text | 12,843,324 |
| idefics2 | [trl-internal-testing/tiny-Idefics2ForConditionalGeneration](https://huggingface.co/trl-internal-testing/tiny-Idefics2ForConditionalGeneration/tree/9cacf64f03691daca2b445b6346d1f138d71d96b) | Idefics2ForConditionalGeneration | 14,647,936 |
| idefics3 | [HuggingFaceTB/SmolVLM-256M-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM-256M-Instruct/tree/7e3e67edbbed1bf9888184d9df282b700a323964) | Idefics3ForConditionalGeneration | 513,028,808 |
| inkling_mm_model | [yujiepan/inkling-tiny-random](https://huggingface.co/yujiepan/inkling-tiny-random/tree/63196aac74bf6bbbcd9cdc102e73f3e51b3294e4) | InklingForConditionalGeneration | 7,337,520 |
| internvl | [trl-internal-testing/tiny-InternVLForConditionalGeneration](https://huggingface.co/trl-internal-testing/tiny-InternVLForConditionalGeneration/tree/8ba51de653e16737a65cce56e057d7ddab90482e) | InternVLForConditionalGeneration | 13,956,416 |
| lfm2_vl | [LiquidAI/LFM2.5-VL-450M](https://huggingface.co/LiquidAI/LFM2.5-VL-450M/tree/fc6221ca597f3315e4f82fc2df606783267b34ba) | Lfm2VlForConditionalGeneration | 897,484,568 |
| llama4 | [optimum-intel-internal-testing/tiny-random-llama4](https://huggingface.co/optimum-intel-internal-testing/tiny-random-llama4/tree/0a5ec316e5c36565d5070e50e19a06d0c2a5be1d) | Llama4ForConditionalGeneration | 13,156,424 |
| llava | [optimum-intel-internal-testing/tiny-random-llava](https://huggingface.co/optimum-intel-internal-testing/tiny-random-llava/tree/47d46b90eb00e2190d510b59ccd0b649e590d5be) | LlavaForConditionalGeneration | 4,225,784 |
| minimax_m3_vl | [IlyasMoutawwakil/tiny-random-MiniMaxM3-MXFP8](https://huggingface.co/IlyasMoutawwakil/tiny-random-MiniMaxM3-MXFP8/tree/ae1af4974ab14a8b40474ba043bba8c18ef01259) | MiniMaxM3SparseForConditionalGeneration | 39,232,000 |
| mistral4 | [onnx-internal-testing/tiny-random-Mistral4ForCausalLM](https://huggingface.co/onnx-internal-testing/tiny-random-Mistral4ForCausalLM/tree/79536716a7c529105c6f6be0ae29f007700df9e2) | Mistral4ForCausalLM | 16,694,448 |
| muse_glimmer | [trl-internal-testing/tiny-MuseGlimmerForConditionalGeneration](https://huggingface.co/trl-internal-testing/tiny-MuseGlimmerForConditionalGeneration/tree/2daa66705814668209044d2b1c84e1413b308330) | MuseGlimmerForConditionalGeneration | 13,040,152 |
| paddleocr_vl | [mlx-community/PaddleOCR-VL-1.6-4bit](https://huggingface.co/mlx-community/PaddleOCR-VL-1.6-4bit/tree/c8987b277bdd8aaec8bd265d154f391bd03ad165) | PaddleOCRVLForConditionalGeneration | 703,562,705 |
| qwen2_5_vl | [trl-internal-testing/tiny-Qwen2_5_VLForConditionalGeneration](https://huggingface.co/trl-internal-testing/tiny-Qwen2_5_VLForConditionalGeneration/tree/62f13fe1c31492fb4195c72ec52cbb736f72fefb) | Qwen2_5_VLForConditionalGeneration | 7,721,168 |
| qwen2_vl | [trl-internal-testing/tiny-Qwen2VLForConditionalGeneration](https://huggingface.co/trl-internal-testing/tiny-Qwen2VLForConditionalGeneration/tree/61aad1a820880f84bc4af87262b05945610aa80d) | Qwen2VLForConditionalGeneration | 7,081,872 |
| qwen3_5 | [trl-internal-testing/tiny-Qwen3_5ForConditionalGeneration-NoThink](https://huggingface.co/trl-internal-testing/tiny-Qwen3_5ForConditionalGeneration-NoThink/tree/c21e64ab01a61fe5675253768d359262f6a19ab6) | Qwen3_5ForConditionalGeneration | 9,294,072 |
| qwen3_5_moe | [tiny-random/qwen3.5-moe](https://huggingface.co/tiny-random/qwen3.5-moe/tree/2ebfa8d9717238c5dda927008104fa172a149050) | Qwen3_5MoeForConditionalGeneration | 10,058,136 |
| qwen3_vl | [trl-internal-testing/tiny-Qwen3VLForConditionalGeneration](https://huggingface.co/trl-internal-testing/tiny-Qwen3VLForConditionalGeneration/tree/ba190cb38011bcda2f70f7781f2b8290627aef00) | Qwen3VLForConditionalGeneration | 6,837,528 |
| qwen3_vl_moe | [tiny-random/qwen3-vl-moe](https://huggingface.co/tiny-random/qwen3-vl-moe/tree/e888d213022a57608210c2fa170f49650b28dda0) | Qwen3VLMoeForConditionalGeneration | 6,339,592 |
| qwen4_exp | [inference-optimization/Qwen3.8-Flash-Next-0.2B-A0.2B](https://huggingface.co/inference-optimization/Qwen3.8-Flash-Next-0.2B-A0.2B/tree/6c4da2eb4901891cd1dbf6cb85be7b54e5db0804) | Qwen4ExpForConditionalGeneration | 327,820,608 |

## image-to-image

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| swin2sr | [caidas/swin2SR-classical-sr-x2-64](https://huggingface.co/caidas/swin2SR-classical-sr-x2-64/tree/cee1c923c6a37361c6e5650b65dcf4be821e5d52) | Swin2SRForImageSuperResolution | 48,460,660 |

## image-to-text

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| git | [microsoft/git-base](https://huggingface.co/microsoft/git-base/tree/1f7fe8444292beb4a259e3a5b6eba440cd5999d4) | GitForCausalLM | 706,526,022 |
| mgp-str | [alibaba-damo/mgp-str-base](https://huggingface.co/alibaba-damo/mgp-str-base/tree/5d06493b6b2a8c4c023d2c030175c03be30f4202) | MGPSTRModel | 591,828,084 |
| pp_lcnet | [PaddlePaddle/PP-LCNet_x1_0_doc_ori_safetensors](https://huggingface.co/PaddlePaddle/PP-LCNet_x1_0_doc_ori_safetensors/tree/b2716954d2e321dd4436400b37584fab641027ab) | unspecified | 6,769,728 |
| pp_ocrv5_mobile_det | [PaddlePaddle/PP-OCRv5_mobile_det_safetensors](https://huggingface.co/PaddlePaddle/PP-OCRv5_mobile_det_safetensors/tree/c5041d225cf951ff06900ab81a3c7d543c45e2ad) | unspecified | 14,330,820 |
| pp_ocrv5_server_det | [PaddlePaddle/PP-OCRv5_server_det_safetensors](https://huggingface.co/PaddlePaddle/PP-OCRv5_server_det_safetensors/tree/cbea9f3c3254c6ff7b0016cfbf90549e1ad4c5bb) | unspecified | 87,994,336 |
| pp_ocrv5_server_rec | [PaddlePaddle/PP-OCRv5_server_rec_safetensors](https://huggingface.co/PaddlePaddle/PP-OCRv5_server_rec_safetensors/tree/542979d7cc3791732bb12af35313a6840952d79f) | unspecified | 84,442,268 |
| pp_ocrv6_medium_det | [PaddlePaddle/PP-OCRv6_medium_det_safetensors](https://huggingface.co/PaddlePaddle/PP-OCRv6_medium_det_safetensors/tree/4236c2b61741a259c091fd879dcc4edc339e916c) | unspecified | 88,020,412 |
| pp_ocrv6_small_det | [PaddlePaddle/PP-OCRv6_small_det_safetensors](https://huggingface.co/PaddlePaddle/PP-OCRv6_small_det_safetensors/tree/eae2ee920a39fb3087637d3dbb58df1896ec1f24) | unspecified | 9,938,124 |
| pp_ocrv6_small_rec | [PaddlePaddle/PP-OCRv6_medium_rec_safetensors](https://huggingface.co/PaddlePaddle/PP-OCRv6_medium_rec_safetensors/tree/024cad6a831de75c2c3c26e711ba8c4a82ccd24b) | unspecified | 76,741,720 |
| pp_ocrv6_tiny_rec | [PaddlePaddle/PP-OCRv6_tiny_rec_safetensors](https://huggingface.co/PaddlePaddle/PP-OCRv6_tiny_rec_safetensors/tree/6f2d2d51b4b4226d7a2329a02f416f4994106f3a) | unspecified | 4,474,264 |
| slanext | [PaddlePaddle/SLANeXt_wired_safetensors](https://huggingface.co/PaddlePaddle/SLANeXt_wired_safetensors/tree/d97b77b5078951c313807747f77ec07beab07e4e) | unspecified | 181,945,252 |
| uvdoc | [PaddlePaddle/UVDoc_safetensors](https://huggingface.co/PaddlePaddle/UVDoc_safetensors/tree/bfa6aad03b549c7e2cf89cefd2fb02ba3bef2ae4) | unspecified | 31,667,380 |

## keypoint-detection

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| lightglue | [ETH-CVG/lightglue_superpoint](https://huggingface.co/ETH-CVG/lightglue_superpoint/tree/5f5f626efee99f37dbc9eafea879d24d297aeab8) | LightGlueForKeypointMatching | 55,016,112 |
| superpoint | [magic-leap-community/superpoint](https://huggingface.co/magic-leap-community/superpoint/tree/734450e9ffe229074f5998494ddc615475cdb20a) | SuperPointModel | 5,206,004 |
| vitpose | [usyd-community/vitpose-plus-base](https://huggingface.co/usyd-community/vitpose-plus-base/tree/92be54d7a29e42fad47b6e2ca01dd9e685a61e0d) | VitPoseForPoseEstimation | 501,627,628 |

## mask-generation

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| edgetam_video | [yonigozlan/EdgeTAM-hf](https://huggingface.co/yonigozlan/EdgeTAM-hf/tree/c266ce53b3fc00f0f495b583f6a116c4e57f53bb) | EdgeTamVideoModel | 55,912,824 |
| sam | [facebook/sam-vit-base](https://huggingface.co/facebook/sam-vit-base/tree/70c1a07f894ebb5b307fd9eaaee97b9dfc16068f) | SamModel | 374,979,480 |
| sam2_video | [facebook/sam2.1-hiera-large](https://huggingface.co/facebook/sam2.1-hiera-large/tree/665f8e2ad61cf5f53d65644ff27c8ee525124610) | Sam2VideoModel | 897,897,416 |
| sam3 | [tiny-random/sam3](https://huggingface.co/tiny-random/sam3/tree/718472c9de166b6fa52b5d8119b14722ebbbc3d1) | Sam3Model | 3,805,256 |
| sam_hq | [syscv-community/sam-hq-vit-base](https://huggingface.co/syscv-community/sam-hq-vit-base/tree/f906a2e3f60fda2f12eb717cef18614f66c43124) | SamHQModel | 379,266,384 |

## multiple-choice

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| fnet | [daze-unlv/google-fnet-base](https://huggingface.co/daze-unlv/google-fnet-base/tree/bfcde75d42f8926e4c11789d287e27bc3567c5fa) | FNetForMultipleChoice | 331,459,532 |

## object-detection

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| conditional_detr | [yainage90/fashion-object-detection](https://huggingface.co/yainage90/fashion-object-detection/tree/fb0a4ff27adfe56500ab4d36e2586436eb1d2979) | ConditionalDetrForObjectDetection | 174,081,852 |
| d_fine | [ustc-community/dfine-xlarge-coco](https://huggingface.co/ustc-community/dfine-xlarge-coco/tree/ea4f6be7350bbe3c199ec6febc74168346cb5a68) | DFineForObjectDetection | 251,619,400 |
| dab-detr | [IDEA-Research/dab-detr-resnet-50](https://huggingface.co/IDEA-Research/dab-detr-resnet-50/tree/d8e2856ee1f7a28088f0b8069ceebf2a44cb5042) | DabDetrForObjectDetection | 175,188,956 |
| deformable_detr | [SenseTime/deformable-detr](https://huggingface.co/SenseTime/deformable-detr/tree/83ecd26945199939cb82806f988debdb71e6f43e) | DeformableDetrForObjectDetection | 160,769,532 |
| detr | [TahaDouaji/detr-doc-table-detection](https://huggingface.co/TahaDouaji/detr-doc-table-detection/tree/14ed1f62a7b71629c187634e565d7abe3273b2c6) | DetrForObjectDetection | 166,496,396 |
| lw_detr | [AnnaZhang/lwdetr_small_60e_coco](https://huggingface.co/AnnaZhang/lwdetr_small_60e_coco/tree/deebf67dc6e174fe3f4c83d7d5f9ea7eaa651197) | LwDetrForObjectDetection | 58,297,008 |
| pp_doclayout_v2 | [PaddlePaddle/PP-DocLayoutV2_safetensors](https://huggingface.co/PaddlePaddle/PP-DocLayoutV2_safetensors/tree/880e8971b88938518611c54fc0f59ad57849c9d4) | PPDocLayoutV2ForObjectDetection | 214,798,436 |
| pp_doclayout_v3 | [PaddlePaddle/PP-DocLayoutV3_safetensors](https://huggingface.co/PaddlePaddle/PP-DocLayoutV3_safetensors/tree/e4f489dc536556fc1be02b973ba06756e0d4a2ac) | PPDocLayoutV3ForObjectDetection | 133,270,468 |
| rf_detr | [Roboflow/rf-detr-base](https://huggingface.co/Roboflow/rf-detr-base/tree/7b95b089788e6c7db56d5ea9b0a07ca08ea6ac0a) | RfDetrForObjectDetection | 128,757,944 |
| rt_detr | [PekingU/rtdetr_r101vd_coco_o365](https://huggingface.co/PekingU/rtdetr_r101vd_coco_o365/tree/ff44b69152a72cc752677665fb4539507d56a99d) | RTDetrForObjectDetection | 307,331,000 |
| table-transformer | [microsoft/table-transformer-structure-recognition](https://huggingface.co/microsoft/table-transformer-structure-recognition/tree/f4d4bdc85c3fe4b1fa49658882a5d38bbdd0f343) | TableTransformerForObjectDetection | 115,434,268 |
| yolos | [hustvl/yolos-small](https://huggingface.co/hustvl/yolos-small/tree/3d8f7130d3ce4907cb206fe1c8485dc8fe8703de) | YolosForObjectDetection | 122,763,274 |

## question-answering

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| ibert | [RyyDer/I-BERT_SQuAD](https://huggingface.co/RyyDer/I-BERT_SQuAD/tree/77273e0918e40876100843c9a80361899c29d649) | IBertForQuestionAnswering | 992,747,176 |
| mobilebert | [csarron/mobilebert-uncased-squad-v2](https://huggingface.co/csarron/mobilebert-uncased-squad-v2/tree/6d49c30d06c6042041039f6fe076b011f0c2053c) | MobileBertForQuestionAnswering | 98,470,130 |
| splinter | [DracolIA/Splinter-Context-based-QA](https://huggingface.co/DracolIA/Splinter-Context-based-QA/tree/cc8b42cc7ff8f10d37ce16f553816a662fb495c1) | SplinterForQuestionAnswering | 445,097,384 |
| visual_bert | [haophancs/visualbert-frcnn-phobert-viclevr](https://huggingface.co/haophancs/visualbert-frcnn-phobert-viclevr/tree/67fac0c2c2d49929f67a47c32e8333c3bc7fc665) | VisualBertForQuestionAnswering | 548,752,280 |

## reinforcement-learning

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| decision_transformer | [hishamcse/decision-transformer-halfcheetah-v4](https://huggingface.co/hishamcse/decision-transformer-halfcheetah-v4/tree/6155e0a5de2e1356adb13858817aa3b669deaae7) | TrainableDT | 5,034,448 |

## sentence-similarity

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| bert | [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/tree/1110a243fdf4706b3f48f1d95db1a4f5529b4d41) | BertModel | 90,868,376 |
| ernie | [shibing624/text2vec-base-chinese-paraphrase](https://huggingface.co/shibing624/text2vec-base-chinese-paraphrase/tree/e90c150a9c7fb55a67712a766d6820c55fb83cdd) | ErnieModel | 471,818,288 |
| gte | [alibaba-nlp-community/gte-multilingual-base](https://huggingface.co/alibaba-nlp-community/gte-multilingual-base/tree/fdaec56c6a50d6ebcf691f616ee83a166346b76c) | NewModel, NewForTokenClassification | 610,753,338 |
| luke | [pkshatech/GLuCoSE-base-ja-v2](https://huggingface.co/pkshatech/GLuCoSE-base-ja-v2/tree/a6cbdf4d0b7e1ab4f7ddd85249a4fb96cda54704) | LukeModel | 532,299,592 |
| mpnet | [sentence-transformers/all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2/tree/e8c3b32edf5434bc2275fc9bab85f82640a19130) | MPNetForMaskedLM | 437,971,872 |
| nomic_bert | [nomic-ai/nomic-embed-text-v1.5](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5/tree/e9b6763023c676ca8431644204f50c2b100d9aab) | NomicBertModel | 546,938,168 |

## summarization

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| led | [pszemraj/led-base-book-summary](https://huggingface.co/pszemraj/led-base-book-summary/tree/842ba9376965acac7e72cab2161ba21f5830be70) | LEDForConditionalGeneration | 647,614,118 |
| longt5 | [pszemraj/long-t5-tglobal-base-sci-simplify](https://huggingface.co/pszemraj/long-t5-tglobal-base-sci-simplify/tree/bf86a88089c7199d6dad4dc815ee4821e362070d) | LongT5ForConditionalGeneration | 990,386,200 |

## text-classification

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| markuplm | [tomlobato/prop_class](https://huggingface.co/tomlobato/prop_class/tree/6acb9c5f0f806f75bb4f795ecd763ef8ea75b183) | MarkupLMForSequenceClassification | 540,858,040 |
| roc_bert | [owen198/claude3_philosophy-ROCBERT](https://huggingface.co/owen198/claude3_philosophy-ROCBERT/tree/766bf718702d5f25a2735623aedb9fec65b1e33d) | RoCBertForSequenceClassification | 469,100,744 |

## text-generation

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| apertus | [swiss-ai/Apertus-v1.1-0.5B](https://huggingface.co/swiss-ai/Apertus-v1.1-0.5B/tree/1b7276176e564fc0cc7d7c3b991a8d653c8b8792) | ApertusForCausalLM | 876,729,616 |
| arcee | [optimum-intel-internal-testing/tiny-random-ArceeForCausalLM](https://huggingface.co/optimum-intel-internal-testing/tiny-random-ArceeForCausalLM/tree/996de545efd203f272e3d4287adc7b2b956775ab) | ArceeForCausalLM | 16,518,368 |
| bamba | [tiny-random/bamba](https://huggingface.co/tiny-random/bamba/tree/2a093641ec0d588529b28fc64e45a392c49f7b0f) | BambaForCausalLM | 8,226,720 |
| bloom | [trl-internal-testing/tiny-BloomForCausalLM](https://huggingface.co/trl-internal-testing/tiny-BloomForCausalLM/tree/fb6f154da5e58e70d7a62bafe35c0f0da99691cb) | BloomForCausalLM | 8,031,808 |
| cohere | [trl-internal-testing/tiny-CohereForCausalLM](https://huggingface.co/trl-internal-testing/tiny-CohereForCausalLM/tree/90bc56bd12c642f6bf5e710ebd7c626dd7c0201c) | CohereForCausalLM | 4,101,744 |
| data2vec-text | [dlwnsdnjs/my_awesome_eli5_clm-model](https://huggingface.co/dlwnsdnjs/my_awesome_eli5_clm-model/tree/ba9686d8c1d47b54932bca07ea9c59181fe87dd2) | Data2VecTextForCausalLM | 498,815,140 |
| dbrx | [trl-internal-testing/tiny-DbrxForCausalLM](https://huggingface.co/trl-internal-testing/tiny-DbrxForCausalLM/tree/9b8efa12d99cf8c94c6b2afc7026c18d32b95104) | DbrxForCausalLM | 9,754,448 |
| deepseek_v2 | [hmellor/tiny-random-DeepseekV2ForCausalLM](https://huggingface.co/hmellor/tiny-random-DeepseekV2ForCausalLM/tree/c0146ef3550ef77c6520211184cf41184b92346a) | DeepseekV2ForCausalLM | 119,572,560 |
| deepseek_v3 | [trl-internal-testing/tiny-DeepseekV3ForCausalLM](https://huggingface.co/trl-internal-testing/tiny-DeepseekV3ForCausalLM/tree/0626191666ec78e25374b8d4bf9b9490119d92a5) | DeepseekV3ForCausalLM | 7,634,864 |
| deepseek_v32 | [hyper-accel/tiny-random-deepseek-v32](https://huggingface.co/hyper-accel/tiny-random-deepseek-v32/tree/530ff1ae90ee8fcceccba2604dec89dd8be6e106) | DeepseekV32ForCausalLM | 546,248,736 |
| deepseek_v4 | [HuggingFaceTB/nanowhale-100m-base](https://huggingface.co/HuggingFaceTB/nanowhale-100m-base/tree/8ea74cc04bebfe7feeec74b29018884eec0265d3) | DeepseekV4ForCausalLM | 441,506,996 |
| doge | [SmallDoge/Doge-320M](https://huggingface.co/SmallDoge/Doge-320M/tree/2249aa221c3a526eeb261b7ded3f46b6211c3efa) | DogeForCausalLM | 109,174,080 |
| ernie4_5 | [baidu/ERNIE-4.5-0.3B-PT](https://huggingface.co/baidu/ERNIE-4.5-0.3B-PT/tree/b565cf6caebdb7a1eadf00100857b1ed5e044f12) | Ernie4_5ForCausalLM | 721,514,672 |
| ernie4_5_moe | [yujiepan/ernie-4.5-moe-tiny-random](https://huggingface.co/yujiepan/ernie-4.5-moe-tiny-random/tree/bc63b89653e292529a787669dff2969bf087a6b6) | Ernie4_5_MoeForCausalLM | 1,833,328 |
| falcon_h1 | [tiiuae/Falcon-H1-Tiny-90M-Instruct](https://huggingface.co/tiiuae/Falcon-H1-Tiny-90M-Instruct/tree/e6389502a0b12cd8da894b395ba5bf7436873b16) | FalconH1ForCausalLM | 182,304,120 |
| falcon_mamba | [tiiuae/falcon-mamba-tiny-dev](https://huggingface.co/tiiuae/falcon-mamba-tiny-dev/tree/f22d33f72a4cc27c1827f3020a6df28c5097fd06) | FalconMambaForCausalLM | 35,064,616 |
| gemma | [trl-internal-testing/tiny-GemmaForCausalLM](https://huggingface.co/trl-internal-testing/tiny-GemmaForCausalLM/tree/276d183fbb0d5f634047f87e6419ec47e48a1d6e) | GemmaForCausalLM | 4,102,016 |
| gemma2 | [hmellor/tiny-random-Gemma2ForCausalLM](https://huggingface.co/hmellor/tiny-random-Gemma2ForCausalLM/tree/7551e53abee9dd16896a86847cd137cbfe41764f) | Gemma2ForCausalLM | 16,887,504 |
| glm4_moe | [trl-internal-testing/tiny-Glm4MoeForCausalLM](https://huggingface.co/trl-internal-testing/tiny-Glm4MoeForCausalLM/tree/19b382257595016963b60289ba295e33abad6834) | Glm4MoeForCausalLM | 4,864,680 |
| glm4_moe_lite | [tiny-random/glm-4.7-flash](https://huggingface.co/tiny-random/glm-4.7-flash/tree/587e67bc8078808039583899f41781f437771c05) | Glm4MoeLiteForCausalLM | 11,585,784 |
| glm_moe_dsa | [tiny-random/glm-5.2](https://huggingface.co/tiny-random/glm-5.2/tree/d81c5b8a604cfa3a12622d8899153f7ac2b7220c) | GlmMoeDsaForCausalLM | 26,675,712 |
| gpt2 | [openai-community/gpt2](https://huggingface.co/openai-community/gpt2/tree/607a30d783dfa663caf39e06633721c8d4cfcd7e) | GPT2LMHeadModel | 548,105,171 |
| gpt_bigcode | [bigcode/tiny_starcoder_py](https://huggingface.co/bigcode/tiny_starcoder_py/tree/8547527bef0bc927268c1653cce6948c5c242dd1) | GPTBigCodeForCausalLM | 656,601,304 |
| gpt_neo | [EleutherAI/gpt-neo-125m](https://huggingface.co/EleutherAI/gpt-neo-125m/tree/21def0189f5705e2521767faed922f1f15e7d7db) | GPTNeoForCausalLM | 525,979,192 |
| gpt_neox | [EleutherAI/pythia-160m](https://huggingface.co/EleutherAI/pythia-160m/tree/50f5173d932e8e61f858120bcb800b97af589f46) | GPTNeoXForCausalLM | 374,998,696 |
| gpt_oss | [trl-internal-testing/tiny-GptOssForCausalLM](https://huggingface.co/trl-internal-testing/tiny-GptOssForCausalLM/tree/e82685101216af1953707faa42567d232a5e4d45) | GptOssForCausalLM | 6,479,008 |
| gptj | [peft-internal-testing/tiny-random-GPTJForCausalLM](https://huggingface.co/peft-internal-testing/tiny-random-GPTJForCausalLM/tree/aee41a2b0d93232814bd6c4f4f63244c78f4f4ba) | GPTJForCausalLM | 522,024 |
| hrm_text | [yujiepan/hrm-text-tiny-random](https://huggingface.co/yujiepan/hrm-text-tiny-random/tree/ab6ffa28ec02739c8e4b368f3dd285b532927640) | HrmTextForCausalLM | 2,317,704 |
| hy_v3 | [yujiepan/hy-v3-tiny-random](https://huggingface.co/yujiepan/hy-v3-tiny-random/tree/5125f710db917c3ca33a7801a8af1685be12e7fd) | HYV3ForCausalLM | 5,401,352 |
| kimi_linear | [yujiepan/kimi-linear-tiny-random](https://huggingface.co/yujiepan/kimi-linear-tiny-random/tree/a8e383cb67f27aad25167d44e5c1824755ec7275) | KimiLinearForCausalLM | 11,691,928 |
| kosmos_2_5_text_model | [Fireblossom/kosmos-2.5-4bit-text](https://huggingface.co/Fireblossom/kosmos-2.5-4bit-text/tree/fd0053d3df5e8a6f525062ad9312d3ff4d18cf47) | Kosmos2_5TextForCausalLM | 717,140,144 |
| lfm2 | [trl-internal-testing/tiny-Lfm2ForCausalLM](https://huggingface.co/trl-internal-testing/tiny-Lfm2ForCausalLM/tree/7794b0799cb903f98f5ad0501f96d4b7aafd9ccf) | Lfm2ForCausalLM | 1,054,096 |
| llama | [HuggingFaceTB/SmolLM2-135M](https://huggingface.co/HuggingFaceTB/SmolLM2-135M/tree/93efa2f097d58c2a74874c7e644dbc9b0cee75a2) | LlamaForCausalLM | 269,060,552 |
| llama4_text | [trl-internal-testing/tiny-Llama4ForCausalLM](https://huggingface.co/trl-internal-testing/tiny-Llama4ForCausalLM/tree/7e26be57fb240ba4b7d388ad120e820ce96f1be5) | Llama4ForCausalLM | 13,079,624 |
| longcat_flash | [tiny-random/longcat-flash](https://huggingface.co/tiny-random/longcat-flash/tree/35f4a5f89881786c95fe82fbe4623149d2047a38) | LongcatFlashForCausalLM | 8,904,024 |
| mamba | [state-spaces/mamba-130m-hf](https://huggingface.co/state-spaces/mamba-130m-hf/tree/1e76775f628fbf1350fbe4dbb3d971ba64af25a1) | MambaForCausalLM | 516,567,560 |
| minimax_m2 | [tiny-random/minimax-m2](https://huggingface.co/tiny-random/minimax-m2/tree/f1bbfc4e55e328418921ddb396c2d508553a4c2b) | MiniMaxM2ForCausalLM | 6,652,456 |
| ministral3 | [yujiepan/devstral-2-tiny-random](https://huggingface.co/yujiepan/devstral-2-tiny-random/tree/4620f9626f8913d3e238bec27f6b96cab55ca17d) | Ministral3ForCausalLM | 2,130,064 |
| mistral | [trl-internal-testing/tiny-MistralForCausalLM-0.2](https://huggingface.co/trl-internal-testing/tiny-MistralForCausalLM-0.2/tree/383a4a9262997cf8e2a05ed6aa3476de5f8bdb22) | MistralForCausalLM | 1,030,096 |
| modernbert-decoder | [onnx-internal-testing/tiny-random-ModernBertDecoderForCausalLM](https://huggingface.co/onnx-internal-testing/tiny-random-ModernBertDecoderForCausalLM/tree/0668913bbb02bebd030c43d4165ff36e9216f6b0) | ModernBertDecoderForCausalLM | 6,712,824 |
| mpt | [yujiepan/mpt-tiny-random](https://huggingface.co/yujiepan/mpt-tiny-random/tree/1062e3257a3af790e3cd72bb9e919b4c2975b766) | MptForCausalLM | 811,528 |
| nemotron | [badaoui/tiny-random-NemotronForCausalLM](https://huggingface.co/badaoui/tiny-random-NemotronForCausalLM/tree/27313228240bbdf42a69c8086cbe180f43687374) | NemotronForCausalLM | 8,605,368 |
| nemotron_h | [trl-internal-testing/tiny-NemotronHForCausalLM-nano](https://huggingface.co/trl-internal-testing/tiny-NemotronHForCausalLM-nano/tree/fd6746d3f4f5c3950d43c6c4adc909d5fd5dd483) | NemotronHForCausalLM | 8,456,616 |
| olmo3 | [trl-internal-testing/tiny-Olmo3ForCausalLM](https://huggingface.co/trl-internal-testing/tiny-Olmo3ForCausalLM/tree/64fc0036c7e9eedc05dce80244eaf385cfac0ee5) | Olmo3ForCausalLM | 3,215,480 |
| openai-gpt | [openai-community/openai-gpt](https://huggingface.co/openai-community/openai-gpt/tree/1e0d4f3028acbffb47fe933cea64619c5ec1a002) | OpenAIGPTLMHeadModel | 478,736,214 |
| opt | [peft-internal-testing/tiny-random-OPTForCausalLM](https://huggingface.co/peft-internal-testing/tiny-random-OPTForCausalLM/tree/6dbfc797d40268c2f04755d6dddcb462f6e30d79) | OPTForCausalLM | 3,258,736 |
| phi3 | [trl-internal-testing/tiny-Phi3ForCausalLM](https://huggingface.co/trl-internal-testing/tiny-Phi3ForCausalLM/tree/d78e80724a57db5553131d3a3a50173e0189c608) | Phi3ForCausalLM | 1,029,840 |
| phimoe | [optimum-intel-internal-testing/phi-3.5-moe-tiny-random](https://huggingface.co/optimum-intel-internal-testing/phi-3.5-moe-tiny-random/tree/c6586c0685a7e397b978018f729812608444a393) | PhiMoEForCausalLM | 2,234,992 |
| plbart | [thealper2/plbart-docstring-generation](https://huggingface.co/thealper2/plbart-docstring-generation/tree/cdaeab08796ec99e2a3acab400372b934955899e) | PLBartForConditionalGeneration | 557,112,860 |
| qwen2 | [Qwen/Qwen2.5-0.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct/tree/7ae557604adf67be50417f59c2c2f167def9a775) | Qwen2ForCausalLM | 988,097,824 |
| qwen3 | [openbmb/MiniCPM5-2B-DSpark](https://huggingface.co/openbmb/MiniCPM5-2B-DSpark/tree/114a20fdbf53220712c7fbdd7dccddbf1dedebb4) | Qwen3DSparkModel | 647,558,522 |
| qwen3_5_moe_text | [crumbs-playground/test-bf-moe](https://huggingface.co/crumbs-playground/test-bf-moe/tree/b04ab92f2317289c0325765fae38a1184d68444d) | Qwen3_5MoeForCausalLM | 97,514,272 |
| qwen3_moe | [trl-internal-testing/tiny-Qwen3MoeForCausalLM](https://huggingface.co/trl-internal-testing/tiny-Qwen3MoeForCausalLM/tree/6db57163fa56fa0e00d4b820169908ac0d3a219d) | Qwen3MoeForCausalLM | 5,212,168 |
| qwen3_next | [tiny-random/qwen3-next-moe](https://huggingface.co/tiny-random/qwen3-next-moe/tree/fab38e08d8f4bbd84232043239b06bb6034d9c15) | Qwen3NextForCausalLM | 5,740,400 |
| qwen4_exp_text | [qikp/tiny-random-Qwen4-Exp_Qwen3.8-Flash-Next](https://huggingface.co/qikp/tiny-random-Qwen4-Exp_Qwen3.8-Flash-Next/tree/d49cb5156b0dad4016f33b55e142a390da88e9fa) | Qwen4ExpForCausalLM | 124,468,800 |
| recurrent_gemma | [pszemraj/griffin-1024-llama3t-8layer-simplewiki-silu](https://huggingface.co/pszemraj/griffin-1024-llama3t-8layer-simplewiki-silu/tree/2403c8dacfcd3c116a1b6ad5c4c882c5570cf668) | RecurrentGemmaForCausalLM | 934,876,808 |
| reformer | [kaizerBox/ReFormer-summarization](https://huggingface.co/kaizerBox/ReFormer-summarization/tree/d80634a7a3a5865aba17ccd1bfb253d314a822c8) | ReformerModelWithLMHead | 27,605,172 |
| rwkv | [jmichaelov/parc-rwkv-seed0](https://huggingface.co/jmichaelov/parc-rwkv-seed0/tree/7e2ce6194ce73fab874bd9a1292434cdeba2c9b6) | RwkvForCausalLM | 677,393,760 |
| seed_oss | [tiny-random/seed-oss](https://huggingface.co/tiny-random/seed-oss/tree/6860befd78b678885f7a52bbf41d7fd0671af2db) | SeedOssForCausalLM | 4,996,944 |
| solar_open | [onnx-internal-testing/tiny-random-SolarOpenForCausalLM](https://huggingface.co/onnx-internal-testing/tiny-random-SolarOpenForCausalLM/tree/a135965020ca4505f77fa20b7a832ee179349a28) | SolarOpenForCausalLM | 100,893,424 |
| t5gemma | [jordimas/t5gemma-s-s-ul2](https://huggingface.co/jordimas/t5gemma-s-s-ul2/tree/40c99423281545bab24762d48cea3fa09e19071f) | T5GemmaForConditionalGeneration | 625,063,080 |
| voxtral | [yujiepan/voxtral-tiny-random](https://huggingface.co/yujiepan/voxtral-tiny-random/tree/94148b82ed65e10f1f158a9ce29a0f129c66b3fd) | VoxtralForConditionalGeneration | 17,438,688 |
| xglm | [KoboldAI/fairseq-dense-125M](https://huggingface.co/KoboldAI/fairseq-dense-125M/tree/7ed81ed9d8d0bead584f5bc6b78889fc6d921fd2) | XGLMForCausalLM | 324,534,618 |
| xlstm | [stefan-it/xlstm-german-wikipedia](https://huggingface.co/stefan-it/xlstm-german-wikipedia/tree/ee8442e5d75e620567c657a86c1dadd89524e66e) | xLSTMForCausalLM | 444,504,408 |

## text-ranking

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| electra | [cross-encoder/ms-marco-electra-base](https://huggingface.co/cross-encoder/ms-marco-electra-base/tree/8b9301757513f8a695920c334c3a9f365ebeb357) | ElectraForSequenceClassification | 437,960,356 |
| xlm-roberta | [cross-encoder/mmarco-mMiniLMv2-L12-H384-v1](https://huggingface.co/cross-encoder/mmarco-mMiniLMv2-L12-H384-v1/tree/1427fd652930e4ba29e8149678df786c240d8825) | XLMRobertaForSequenceClassification | 470,592,698 |

## text-to-audio

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| csm | [Marvis-AI/marvis-tts-250m-v0.2-MLX-8bit](https://huggingface.co/Marvis-AI/marvis-tts-250m-v0.2-MLX-8bit/tree/f564ede427b7ec816b229b8c1c2f129817dc4a95) | CsmForConditionalGeneration | 665,515,046 |

## text-to-speech

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| speecht5 | [thealper2/speecht5-tts-turkish](https://huggingface.co/thealper2/speecht5-tts-turkish/tree/5a32b9fb7d865191cb22bda3b039a1eff6214651) | SpeechT5ForTextToSpeech | 577,844,616 |
| vits | [facebook/mms-tts-bam](https://huggingface.co/facebook/mms-tts-bam/tree/11905f69c2982bf15106044f035d957815aafb1d) | VitsModel | 145,225,976 |

## time-series-forecasting

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| patchtst | [ibm-granite/granite-timeseries-patchtst](https://huggingface.co/ibm-granite/granite-timeseries-patchtst/tree/7fe295d8bc8fbac8041b60ab351882634165517f) | PatchTSTForPrediction | 2,472,368 |
| time_series_transformer | [huggingface/time-series-transformer-tourism-monthly](https://huggingface.co/huggingface/time-series-transformer-tourism-monthly/tree/2a40ad41f6ffe61e7bef6099b08c6c2fce36ac35) | TimeSeriesTransformerForPrediction | 132,652 |
| timesfm | [google/timesfm-2.5-200m-pytorch](https://huggingface.co/google/timesfm-2.5-200m-pytorch/tree/1d952420fba87f3c6dee4f240de0f1a0fbc790e3) | TimesFmModelForPrediction | 925,181,104 |
| timesfm2_5 | [google/timesfm-2.5-200m-transformers](https://huggingface.co/google/timesfm-2.5-200m-transformers/tree/5a9806b9b291fad9233b5249d88263f1846304d3) | TimesFm2_5ModelForPrediction | 925,187,448 |

## token-classification

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| big_bird | [adibvafa/CodonTransformer](https://huggingface.co/adibvafa/CodonTransformer/tree/9744dcc920d813066391fc828d7a590207f148e8) | BigBirdForMaskedLM | 358,342,232 |
| bros | [adamadam111/bros-funsd-finetuned](https://huggingface.co/adamadam111/bros-funsd-finetuned/tree/c81385da95edcce7ea7568336a8ac216d22686df) | BrosForTokenClassification | 438,027,804 |
| eurobert | [OpenMed/OpenMed-NER-ChemicalDetect-EuroMed-212M](https://huggingface.co/OpenMed/OpenMed-NER-ChemicalDetect-EuroMed-212M/tree/5ab702762c0b54489e3274695c5a241900b172f7) | EuroBertForTokenClassification | 423,549,134 |
| layoutlmv2 | [nielsr/layoutlmv2-finetuned-funsd](https://huggingface.co/nielsr/layoutlmv2-finetuned-funsd/tree/405e52225928302d4c3c239ad71db42e15da2670) | LayoutLMv2ForTokenClassification | 802,070,356 |
| longformer | [OpenMed/OpenMed-PII-Italian-ClinicalLongformer-Base-149M-v1](https://huggingface.co/OpenMed/OpenMed-PII-Italian-ClinicalLongformer-Base-149M-v1/tree/2c664f6b974502da9853ac4eae996d9d212562e9) | LongformerForTokenClassification | 592,543,232 |
| openai_privacy_filter | [yujiepan/openai-privacy-filter-tiny-random](https://huggingface.co/yujiepan/openai-privacy-filter-tiny-random/tree/02f3e27ee09825ac72748cb3db3e8e13e6f1159f) | OpenAIPrivacyFilterForTokenClassification | 4,132,058 |
| yoso | [SKNahin/NER_YOSO2](https://huggingface.co/SKNahin/NER_YOSO2/tree/49e9ef31f6eb2f13057e1851ad759fb60329575a) | YosoForTokenClassification | 507,293,540 |

## translation

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| marian | [Helsinki-NLP/opus-mt-fr-en](https://huggingface.co/Helsinki-NLP/opus-mt-fr-en/tree/c4aed37b318c763fd177aa449b44e3b783cc6c02) | MarianMTModel | 300,803,608 |
| pegasus | [TigreGotico/nos-mt-es-arg-onnx](https://huggingface.co/TigreGotico/nos-mt-es-arg-onnx/tree/69e5b1f046e7ae63fd664b24282942ce2a0b960d) | PegasusForConditionalGeneration | 418,174,264 |
| t5 | [google-t5/t5-small](https://huggingface.co/google-t5/t5-small/tree/df1b051c49625cf57a3d0d8d3863ed4d13564fe4) | T5ForConditionalGeneration | 242,043,056 |
| umt5 | [B-K/umt5-thai-g2p-v2-0.5k](https://huggingface.co/B-K/umt5-thai-g2p-v2-0.5k/tree/95d40d35d62b3b57372785bc99ab962608accca6) | UMT5ForConditionalGeneration | 178,331,440 |

## unspecified

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| afmoe | [optimum-intel-internal-testing/tiny-random-trinity](https://huggingface.co/optimum-intel-internal-testing/tiny-random-trinity/tree/2d4c4b66a4f1459ca5b4b987c860fb0333b8119d) | AfmoeForCausalLM | 30,565,352 |
| aimv2 | [lucasjin/aimv2-large-patch14-224](https://huggingface.co/lucasjin/aimv2-large-patch14-224/tree/052bc03c332350903097f50b2f0fadd42e2cac6f) | AIMv2Model | 618,413,824 |
| aimv2_vision_model | [hf-tiny-v2/tiny-random-Aimv2VisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-Aimv2VisionModel/tree/c0e79d4d16ccd5c8d1fa11c46afcf8202a594f2e) | Aimv2VisionModel | 107,672 |
| align | [hf-tiny-v2/tiny-random-AlignModel](https://huggingface.co/hf-tiny-v2/tiny-random-AlignModel/tree/e31777c5f31b068e7923578e92dd98c21fa72207) | AlignModel | 6,699,820 |
| altclip | [hf-tiny-v2/tiny-random-AltCLIPModel](https://huggingface.co/hf-tiny-v2/tiny-random-AltCLIPModel/tree/558deda0f953b18aa5912829453a8e248ae8e76c) | AltCLIPModel | 32,236,540 |
| aria | [hf-tiny-v2/tiny-random-AriaForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-AriaForConditionalGeneration/tree/07f8f56a71cd38c59405ca87f1330e3e62d0e3b4) | AriaForConditionalGeneration | 25,876,664 |
| aria_text | [hf-tiny-v2/tiny-random-AriaTextForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-AriaTextForCausalLM/tree/088fe1aff414786ccadd554cb4e2f98f7d9967dc) | AriaTextForCausalLM | 25,764,360 |
| audioflamingo3 | [hf-tiny-v2/tiny-random-AudioFlamingo3ForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-AudioFlamingo3ForConditionalGeneration/tree/15b94ef171569d8e23079eb8eca3a71981e698f3) | AudioFlamingo3ForConditionalGeneration | 39,001,576 |
| audioflamingo3_encoder | [hf-tiny-v2/tiny-random-AudioFlamingo3Encoder](https://huggingface.co/hf-tiny-v2/tiny-random-AudioFlamingo3Encoder/tree/8c3e832196e5e8c5a02bcee2c8a923d1d8627c12) | AudioFlamingo3Encoder | 123,888 |
| autoformer | [thesven/BTC-Autoformer-v1](https://huggingface.co/thesven/BTC-Autoformer-v1/tree/754eeb547b37779f598a809303bc50fe4b9a2c3d) | AutoformerForPrediction | 443,492 |
| axk1 | [hf-tiny-v2/tiny-random-AXK1ForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-AXK1ForCausalLM/tree/47e582eea340e6c1ede778819d42f705c7f04f52) | AXK1ForCausalLM | 42,092,600 |
| axk2 | [hf-tiny-v2/tiny-random-AXK2Model](https://huggingface.co/hf-tiny-v2/tiny-random-AXK2Model/tree/d372f8ae5dce29ae16d07ba167029c9dfda25de0) | AXK2Model | 21,261,984 |
| aya_vision | [hf-tiny-v2/tiny-random-AyaVisionForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-AyaVisionForConditionalGeneration/tree/d0f59ceff5e176cfca27e4f232c12402529d77f6) | AyaVisionForConditionalGeneration | 131,460,832 |
| bark | [hf-tiny-v2/tiny-random-BarkModel](https://huggingface.co/hf-tiny-v2/tiny-random-BarkModel/tree/618ae4dc045ef3fa8d7799a2c20a4c6f1e80af89) | BarkModel | 934,372 |
| biogpt | [Sepideh2027/biogpt-clinvar-finetuned](https://huggingface.co/Sepideh2027/biogpt-clinvar-finetuned/tree/c1544847deb603ec065cd9a0264e75f363ce3b01) | BioGptForCausalLM | 693,569,168 |
| bitnet | [optimum-intel-internal-testing/tiny-random-bitnet](https://huggingface.co/optimum-intel-internal-testing/tiny-random-bitnet/tree/3e052b2aaf2bc9d53665f0dcc4a02103c77c8a57) | BitNetForCausalLM | 528,951,400 |
| blenderbot | [hf-tiny-v2/tiny-random-BlenderbotForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-BlenderbotForConditionalGeneration/tree/7f50e4cd2916752d3011b308b8fe67405213c278) | BlenderbotForConditionalGeneration | 609,916 |
| blenderbot-small | [lordtt13/blenderbot_small-news](https://huggingface.co/lordtt13/blenderbot_small-news/tree/0db9d766dcbeecf97b63d72a2bfcd5c57359e98b) | BlenderbotSmallForConditionalGeneration | 350,295,176 |
| blip-2 | [hf-tiny-v2/tiny-random-Blip2Model](https://huggingface.co/hf-tiny-v2/tiny-random-Blip2Model/tree/4e8085f861f55eef8df337bb9ca02bc95ddef799) | Blip2Model | 6,749,288 |
| blip_2_qformer | [hf-tiny-v2/tiny-random-Blip2QFormerModel](https://huggingface.co/hf-tiny-v2/tiny-random-Blip2QFormerModel/tree/0aa8d7890c47971186ede7b0185e5dd79fc5cb65) | Blip2QFormerModel | 76,464 |
| bridgetower | [hf-tiny-v2/tiny-random-BridgeTowerModel](https://huggingface.co/hf-tiny-v2/tiny-random-BridgeTowerModel/tree/3759a5bfb0b90900f84224056ef489b688edf588) | BridgeTowerModel | 14,782,104 |
| canary | [hf-tiny-v2/tiny-random-CanaryForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-CanaryForConditionalGeneration/tree/bd0c8ad02e9bf3d858634adf7685291f46c4db25) | CanaryForConditionalGeneration | 1,209,888 |
| chameleon | [hf-tiny-v2/tiny-random-ChameleonForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-ChameleonForConditionalGeneration/tree/61b09b095a1be7325d547f81496e73d287e779d7) | ChameleonForConditionalGeneration | 18,240,736 |
| chameleon_vqgan | [leloy/Anole-7b-v0.1-vqvae-hf](https://huggingface.co/leloy/Anole-7b-v0.1-vqvae-hf/tree/72d00ee787d15e29b0c84a908e47b1e68d052a93) | ChameleonVQVAE | 274,904,108 |
| chinese_clip | [sharkMeow/train_V2](https://huggingface.co/sharkMeow/train_V2/tree/3760fbfe0e3859a70df67db67b7f94e08bdd420b) | ChineseCLIPDualTextModel | 816,611,916 |
| chinese_clip_vision_model | [hf-tiny-v2/tiny-random-ChineseCLIPVisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-ChineseCLIPVisionModel/tree/f246e06f95f855ba3af40ced796d62b411c165b9) | ChineseCLIPVisionModel | 89,192 |
| chmv2 | [hf-tiny-v2/tiny-random-CHMv2ForDepthEstimation](https://huggingface.co/hf-tiny-v2/tiny-random-CHMv2ForDepthEstimation/tree/e5bfcd2a3c04f55c06f5888580f424d5ab543c30) | CHMv2ForDepthEstimation | 303,376 |
| clap_audio_model | [NGDtuanh/abook-music-student](https://huggingface.co/NGDtuanh/abook-music-student/tree/2374dab847a5a1356948a7e6b741997de25ebbbd) | ClapAudioModelWithProjection | 808,457,800 |
| clap_text_model | [werent4/larger_clap_general_text_model](https://huggingface.co/werent4/larger_clap_general_text_model/tree/1e05882ab89b0ac25f7ca96424974699e27e9e0a) | ClapTextModel | 498,613,304 |
| clip_text_model | [peft-internal-testing/tiny-clip-text-2](https://huggingface.co/peft-internal-testing/tiny-clip-text-2/tree/4fbb8d27f0fdda658bc80bbccbd3d749044ace78) | CLIPTextModelWithProjection | 287,396 |
| clvp | [hf-tiny-v2/tiny-random-ClvpModelForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-ClvpModelForConditionalGeneration/tree/0e6c025a205ef4c1c1d7ab14de6429b25963e8dc) | ClvpModelForConditionalGeneration | 4,215,404 |
| codegen | [optimum-intel-internal-testing/tiny-random-codegen2](https://huggingface.co/optimum-intel-internal-testing/tiny-random-codegen2/tree/6123a493729d9939515a7c5b4835f347337f2387) | CodeGenForCausalLM | 13,938,896 |
| cohere2 | [optimum-intel-internal-testing/tiny-random-aya-base](https://huggingface.co/optimum-intel-internal-testing/tiny-random-aya-base/tree/e85478d37f912454b23ff2a9c7af16a960837644) | Cohere2ForCausalLM | 4,262,232 |
| cohere2_moe | [hf-tiny-v2/tiny-random-Cohere2MoeForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-Cohere2MoeForCausalLM/tree/f106c1d9dc22f0caabfb09e1142318b26cd924de) | Cohere2MoeForCausalLM | 65,386,456 |
| cohere2_vision | [hf-tiny-v2/tiny-random-Cohere2VisionForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-Cohere2VisionForConditionalGeneration/tree/ca5be3c9df07de3d3df3b5b016e11ee5f03e3591) | Cohere2VisionForConditionalGeneration | 131,385,728 |
| cohere_compass | [hf-tiny-v2/tiny-random-CohereCompassForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-CohereCompassForConditionalGeneration/tree/ff8162be0e78ad81664c7541ab59cd4fdd4a6eeb) | CohereCompassForConditionalGeneration | 66,095,920 |
| cohere_compass_text | [hf-tiny-v2/tiny-random-CohereCompassTextForSequenceClassification](https://huggingface.co/hf-tiny-v2/tiny-random-CohereCompassTextForSequenceClassification/tree/94552d9d91aa6ed78efdc3e9f78483804ec26c6a) | CohereCompassTextForSequenceClassification | 32,720,848 |
| cohere_compass_vision | [hf-tiny-v2/tiny-random-CohereCompassVisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-CohereCompassVisionModel/tree/b200261b9296137dfb7e37ddb14fc4c4b2b243d5) | CohereCompassVisionModel | 729,896 |
| colmodernvbert | [hf-tiny-v2/tiny-random-ColModernVBertForRetrieval](https://huggingface.co/hf-tiny-v2/tiny-random-ColModernVBertForRetrieval/tree/f8b6c00ec931c53a5f0e69350c74722f306c95b0) | ColModernVBertForRetrieval | 328,336 |
| colpali | [hf-tiny-v2/tiny-random-ColPaliForRetrieval](https://huggingface.co/hf-tiny-v2/tiny-random-ColPaliForRetrieval/tree/13e511487c7541ec6c22aaf8f815af417d0f8539) | ColPaliForRetrieval | 33,088,132 |
| colqwen2 | [hf-tiny-v2/tiny-random-ColQwen2ForRetrieval](https://huggingface.co/hf-tiny-v2/tiny-random-ColQwen2ForRetrieval/tree/6c6905be8f41adac54e4da17903c78a2c4afd757) | ColQwen2ForRetrieval | 441,840 |
| cosmos3_edge | [hf-tiny-v2/tiny-random-Cosmos3EdgeModel](https://huggingface.co/hf-tiny-v2/tiny-random-Cosmos3EdgeModel/tree/83ad2ab245b78cec61c6b381dadaa1241b20573b) | Cosmos3EdgeModel | 16,954,296 |
| cosmos3_edge_text | [hf-tiny-v2/tiny-random-Cosmos3EdgeTextModel](https://huggingface.co/hf-tiny-v2/tiny-random-Cosmos3EdgeTextModel/tree/d34ad5c59a80a452e5c3f4ba0c9eaccbed57f5e2) | Cosmos3EdgeTextModel | 16,837,008 |
| cosmos3_edge_vision | [hf-tiny-v2/tiny-random-Cosmos3EdgeVisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-Cosmos3EdgeVisionModel/tree/842a1c58cdc77520d766be9a75e470f0d55e7e24) | Cosmos3EdgeVisionModel | 74,384 |
| cosmos3_omni | [hf-tiny-v2/tiny-random-Cosmos3OmniForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-Cosmos3OmniForConditionalGeneration/tree/480d857bc7412a9988443d7c965ba4e5bd077f5f) | Cosmos3OmniForConditionalGeneration | 39,160,352 |
| cpmant | [hf-tiny-v2/tiny-random-CpmAntForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-CpmAntForCausalLM/tree/9d2a600aca051a389366a5b746ac4a2708d2fce1) | CpmAntForCausalLM | 4,498,912 |
| ctrl | [hf-tiny-v2/tiny-random-CTRLLMHeadModel](https://huggingface.co/hf-tiny-v2/tiny-random-CTRLLMHeadModel/tree/a1bd395616dc09388ca3811657b59d8c9ec25601) | CTRLLMHeadModel | 32,600,752 |
| cwm | [hf-tiny-v2/tiny-random-CwmForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-CwmForCausalLM/tree/e0acc36e9533b85c5af948f7662edbd88012a2f3) | CwmForCausalLM | 32,893,752 |
| deepseek_ocr2 | [optimum-intel-internal-testing/tiny-random-deepseek-ocr-2](https://huggingface.co/optimum-intel-internal-testing/tiny-random-deepseek-ocr-2/tree/305824b485e408f24a816fcf2e508ce1e6115224) | DeepseekOcr2ForConditionalGeneration | 137,882,712 |
| deepseek_vl | [hf-tiny-v2/tiny-random-DeepseekVLForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-DeepseekVLForConditionalGeneration/tree/73e5d402612eb5fcd9649f1100d2b5611b33a57a) | DeepseekVLForConditionalGeneration | 25,736,704 |
| deepseek_vl_hybrid | [hf-tiny-v2/tiny-random-DeepseekVLHybridForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-DeepseekVLHybridForConditionalGeneration/tree/c1d29daeb78a8b7b97ea1c5b18a9909114c546ca) | DeepseekVLHybridForConditionalGeneration | 6,682,120 |
| deimv2 | [harshaljanjani/DEIMv2_DINOv3_S_COCO_Transformers](https://huggingface.co/harshaljanjani/DEIMv2_DINOv3_S_COCO_Transformers/tree/598fb1fce3a7f0b55c744854ca5ba74864d996b0) | Deimv2ForObjectDetection | 39,421,512 |
| depth_pro | [hf-tiny-v2/tiny-random-DepthProModel](https://huggingface.co/hf-tiny-v2/tiny-random-DepthProModel/tree/f261db1274b4b57f4e48f534e3fa8ccdb8b3c958) | DepthProModel | 158,456 |
| dia | [hf-tiny-v2/tiny-random-DiaForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-DiaForConditionalGeneration/tree/b1bff3285db79f4e1130ba61933fb4e7be177378) | DiaForConditionalGeneration | 162,968 |
| diffllama | [hf-tiny-v2/tiny-random-DiffLlamaForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-DiffLlamaForCausalLM/tree/8dfe645c46bdd4bf557f06b4afec2b234b592f7f) | DiffLlamaForCausalLM | 32,898,648 |
| donut-swin | [hsarfraz/donut-irs-tax-docs-classifier](https://huggingface.co/hsarfraz/donut-irs-tax-docs-classifier/tree/176bacd4f5fc16153d9f527acc5bc20d3c64178a) | DonutForImageClassification | 298,460,480 |
| dots1 | [Goekdeniz-Guelmez/Dots1-Dev](https://huggingface.co/Goekdeniz-Guelmez/Dots1-Dev/tree/992d899c56feb8e04aa08913808af0ef5a29a05d) | Dots1ForCausalLM | 162,814,432 |
| edgetam | [hf-tiny-v2/tiny-random-EdgeTamModel](https://huggingface.co/hf-tiny-v2/tiny-random-EdgeTamModel/tree/5afdbb9953fd7928230d2236da6e3e16179bab23) | EdgeTamModel | 1,624,724 |
| edgetam_vision_model | [hf-tiny-v2/tiny-random-EdgeTamVisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-EdgeTamVisionModel/tree/61600bf9da3818f28b69a4af35f9738a5d9c8bec) | EdgeTamVisionModel | 1,421,384 |
| efficientloftr | [zju-community/efficientloftr](https://huggingface.co/zju-community/efficientloftr/tree/face1a79050ffa3e9da28720d1cf93aaf2e8f421) | EfficientLoFTRForKeypointMatching | 64,263,488 |
| emu3 | [hf-tiny-v2/tiny-random-Emu3ForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-Emu3ForConditionalGeneration/tree/8e322dfe440ae27d9e88808e00a27371d6cec1b4) | Emu3ForConditionalGeneration | 50,329,812 |
| emu3_text_model | [hf-tiny-v2/tiny-random-Emu3TextModel](https://huggingface.co/hf-tiny-v2/tiny-random-Emu3TextModel/tree/55376ae92397bb23d622c379fe83d8387df523c5) | Emu3TextModel | 23,695,464 |
| encoder-decoder | [optimum-internal-testing/tiny-random-encoder-decoder-gpt2-bert](https://huggingface.co/optimum-internal-testing/tiny-random-encoder-decoder-gpt2-bert/tree/c33d2b7ac989b8d01fc29e3f9eeb83dcb6979c46) | EncoderDecoderModel | 906,124 |
| ernie4_5_vl_moe | [hf-tiny-v2/tiny-random-Ernie4_5_VLMoeForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-Ernie4_5_VLMoeForConditionalGeneration/tree/cd75e655d0d4f58225317dfbdcf3a2c569eb92d5) | Ernie4_5_VLMoeForConditionalGeneration | 6,903,104 |
| esmc | [hf-tiny-v2/tiny-random-EsmcForMaskedLM](https://huggingface.co/hf-tiny-v2/tiny-random-EsmcForMaskedLM/tree/8352ec45d70c8c3c5ff959e679b8909129370532) | EsmcForMaskedLM | 99,932 |
| esmfold2 | [biohub/ESMFold2-Experimental-Fast-Cutoff2025](https://huggingface.co/biohub/ESMFold2-Experimental-Fast-Cutoff2025/tree/13f892d3bc9de27aa475e8a12ec76dba4054f4a2) | ESMFold2ExperimentalModel | 717,341,848 |
| exaone4 | [optimum-intel-internal-testing/tiny-random-exaone4](https://huggingface.co/optimum-intel-internal-testing/tiny-random-exaone4/tree/d0bcb89ba2b3d1a80d8ade88c9bc0ffa6a28f90c) | Exaone4ForCausalLM | 27,167,128 |
| exaone4_5 | [hf-tiny-v2/tiny-random-Exaone4_5_ForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-Exaone4_5_ForConditionalGeneration/tree/2f80b130d89358109d5d8d85732127af30dabdfb) | Exaone4_5_ForConditionalGeneration | 39,634,096 |
| exaone4_5_vision | [hf-tiny-v2/tiny-random-Exaone4_5_VisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-Exaone4_5_VisionModel/tree/ec32a0e54c554f0b6759bbb247ef10629960d8a9) | Exaone4_5_VisionModel | 259,008 |
| exaone_moe | [hf-tiny-v2/tiny-random-ExaoneMoeForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-ExaoneMoeForCausalLM/tree/a9b83a69112f2d4a303ea6b78d04edd9d561fef1) | ExaoneMoeForCausalLM | 39,429,552 |
| falcon | [optimum-intel-internal-testing/tiny-random-falcon-40b](https://huggingface.co/optimum-intel-internal-testing/tiny-random-falcon-40b/tree/77958ea0d3ea684a0894bdd50f1acb0ada7a65a8) | FalconForCausalLM | 34,741,144 |
| fast_vlm | [hf-tiny-v2/tiny-random-FastVlmForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-FastVlmForConditionalGeneration/tree/a6c8104507807dd09d5b183d3847d08e18971c81) | FastVlmForConditionalGeneration | 38,946,968 |
| fastspeech2_conformer | [hf-tiny-v2/tiny-random-FastSpeech2ConformerModel](https://huggingface.co/hf-tiny-v2/tiny-random-FastSpeech2ConformerModel/tree/cba0929b93f31e0e1b7ea55e2ddfbe7f06ee663b) | FastSpeech2ConformerModel | 1,284,220 |
| fastspeech2_conformer_with_hifigan | [hf-tiny-v2/tiny-random-FastSpeech2ConformerWithHifiGan](https://huggingface.co/hf-tiny-v2/tiny-random-FastSpeech2ConformerWithHifiGan/tree/8991d0f5e58ad3c15d479c5bee1c475ec472e7b4) | FastSpeech2ConformerWithHifiGan | 2,171,896 |
| flava | [hf-tiny-v2/tiny-random-FlavaModel](https://huggingface.co/hf-tiny-v2/tiny-random-FlavaModel/tree/3d06db5a79fa417814354394530db91adba45483) | FlavaModel | 4,211,644 |
| flex_olmo | [hf-tiny-v2/tiny-random-FlexOlmoForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-FlexOlmoForCausalLM/tree/4829dee9d6d67210bdc6d9a60976b8a93660fa18) | FlexOlmoForCausalLM | 25,911,480 |
| focalnet | [nostrbuild/nsfw-image-detection-large](https://huggingface.co/nostrbuild/nsfw-image-detection-large/tree/05b20904ceff042e3bcc095fa58360b5e732b5b6) | FocalNetForImageClassification | 348,556,636 |
| fsmt | [hf-tiny-v2/tiny-random-FSMTForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-FSMTForConditionalGeneration/tree/7a64d4ccd276130784f2574351dd17cd5d67c495) | FSMTForConditionalGeneration | 6,088,080 |
| fun_asr_nano | [hf-tiny-v2/tiny-random-FunAsrNanoForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-FunAsrNanoForConditionalGeneration/tree/c5947e22000a6308b8be73bf743fa86e9cde3880) | FunAsrNanoForConditionalGeneration | 39,440,208 |
| fun_asr_nano_encoder | [hf-tiny-v2/tiny-random-FunAsrNanoEncoder](https://huggingface.co/hf-tiny-v2/tiny-random-FunAsrNanoEncoder/tree/f2778bda5757e9cc9701023b369b233e64ae3caf) | FunAsrNanoEncoder | 221,288 |
| fuyu | [hf-tiny-v2/tiny-random-FuyuForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-FuyuForCausalLM/tree/aa23bea3ea4297562181a52f137fc1e8f152fe6f) | FuyuForCausalLM | 67,514,008 |
| gemma3n | [optimum-intel-internal-testing/tiny-random-gemma3n](https://huggingface.co/optimum-intel-internal-testing/tiny-random-gemma3n/tree/51b23b5d6882b25cc74d8b87620a91b408285f2a) | Gemma3nForConditionalGeneration | 73,145,268 |
| gemma3n_audio | [hf-tiny-v2/tiny-random-Gemma3nAudioEncoder](https://huggingface.co/hf-tiny-v2/tiny-random-Gemma3nAudioEncoder/tree/c30a1dee96c657e32d773dd9cf76a0dd11c36bbc) | Gemma3nAudioEncoder | 218,480 |
| gemma3n_text | [optimum-intel-internal-testing/tiny-random-gemma3n-text](https://huggingface.co/optimum-intel-internal-testing/tiny-random-gemma3n-text/tree/2ff44619e6ee2426b377115a103493e54d0e08c7) | Gemma3nForCausalLM | 69,672,564 |
| gemma4_text | [AlexKoff88/gemma4_tinystories](https://huggingface.co/AlexKoff88/gemma4_tinystories/tree/493ce1a28e362719c47a4442d21ffa6d3c0a6f5d) | Gemma4ForCausalLM | 76,073,598 |
| gemma4_unified | [optimum-intel-internal-testing/tiny-random-gemma4-unified](https://huggingface.co/optimum-intel-internal-testing/tiny-random-gemma4-unified/tree/bb0990a1377dbcacbb790ace3bdebca0a7467692) | Gemma4UnifiedForConditionalGeneration | 34,751,696 |
| gemma4_unified_text | [hf-tiny-v2/tiny-random-Gemma4UnifiedTextModel](https://huggingface.co/hf-tiny-v2/tiny-random-Gemma4UnifiedTextModel/tree/caa74ce6d31ba6c9566a85825c93772ef43a5599) | Gemma4UnifiedTextModel | 33,685,320 |
| gemma4_vision | [hf-tiny-v2/tiny-random-Gemma4VisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-Gemma4VisionModel/tree/f75e1954421b0a08f91c0f43c78879c6e41720a2) | Gemma4VisionModel | 2,828,408 |
| glm | [optimum-intel-internal-testing/tiny-random-glm-edge](https://huggingface.co/optimum-intel-internal-testing/tiny-random-glm-edge/tree/f35c762b8c2b57ddedbe1999df1d012b147f48dc) | GlmForCausalLM | 145,180,176 |
| glm4 | [optimum-intel-internal-testing/tiny-random-glm4](https://huggingface.co/optimum-intel-internal-testing/tiny-random-glm4/tree/4776f2b0005734eff6ad66ffc583059c176a108d) | Glm4Model | 29,946,272 |
| glm46v | [hf-tiny-v2/tiny-random-Glm46VModel](https://huggingface.co/hf-tiny-v2/tiny-random-Glm46VModel/tree/81b0f2aba9bc19d217b7725eaab0b2e3c5c12761) | Glm46VModel | 10,146,216 |
| glm4v_moe_text | [hf-tiny-v2/tiny-random-Glm4vMoeTextModel](https://huggingface.co/hf-tiny-v2/tiny-random-Glm4vMoeTextModel/tree/863c43ad9959eb182ffc2206b36f1c5473f124f1) | Glm4vMoeTextModel | 12,134,904 |
| glm4v_moe_vision | [hf-tiny-v2/tiny-random-Glm4vMoeVisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-Glm4vMoeVisionModel/tree/dfd10243e69e9be6cacff487ac1675954e059665) | Glm4vMoeVisionModel | 440,832 |
| glm4v_text | [hf-tiny-v2/tiny-random-Glm4vTextModel](https://huggingface.co/hf-tiny-v2/tiny-random-Glm4vTextModel/tree/f4b61c8650212401f942d83cf9c59e7be0d807e2) | Glm4vTextModel | 9,704,720 |
| glm4v_vision | [hf-tiny-v2/tiny-random-Glm4vVisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-Glm4vVisionModel/tree/ddeb6348f6dadd2efbb8b922e0bf7b7497d8fd18) | Glm4vVisionModel | 440,832 |
| glm5_next_text | [hf-tiny-v2/tiny-random-Glm5NextTextModel](https://huggingface.co/hf-tiny-v2/tiny-random-Glm5NextTextModel/tree/5364a87fea5789711858117babcb54e8dda50e0a) | Glm5NextTextModel | 29,998,648 |
| glm5_next_vision | [hf-tiny-v2/tiny-random-Glm5NextVisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-Glm5NextVisionModel/tree/e6f5d06e7578f1ff99a37285b953992c465f4ae3) | Glm5NextVisionModel | 427,064 |
| glm_image | [hf-tiny-v2/tiny-random-GlmImageModel](https://huggingface.co/hf-tiny-v2/tiny-random-GlmImageModel/tree/54e7acffd4da2b1048419b8ca2e8c4abd5bacb48) | GlmImageModel | 10,936,984 |
| glm_image_text | [hf-tiny-v2/tiny-random-GlmImageTextModel](https://huggingface.co/hf-tiny-v2/tiny-random-GlmImageTextModel/tree/fd57f74fff7e51b678d807a03c259d1a1f6a8cc4) | GlmImageTextModel | 10,761,544 |
| glm_image_vision | [hf-tiny-v2/tiny-random-GlmImageVisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-GlmImageVisionModel/tree/ce8a384c5681b23aa1949379e9ac827d29bacef7) | GlmImageVisionModel | 155,456 |
| glm_image_vqmodel | [hf-tiny-v2/tiny-random-GlmImageVQVAE](https://huggingface.co/hf-tiny-v2/tiny-random-GlmImageVQVAE/tree/dd07155f5be908ea4b21e9bf538f65043332b5a9) | GlmImageVQVAE | 19,208 |
| glm_ocr_text | [hf-tiny-v2/tiny-random-GlmOcrTextModel](https://huggingface.co/hf-tiny-v2/tiny-random-GlmOcrTextModel/tree/dcae3b6dbe56515ceb7736480dc4c74fb8e85c70) | GlmOcrTextModel | 3,811,416 |
| glm_ocr_vision | [hf-tiny-v2/tiny-random-GlmOcrVisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-GlmOcrVisionModel/tree/67e1629060806aca5a3b270e3c1ffe175f247319) | GlmOcrVisionModel | 345,304 |
| glmasr | [hf-tiny-v2/tiny-random-GlmAsrForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-GlmAsrForConditionalGeneration/tree/3603f29292ee0cdd33517165f2ba9c2b2f306a81) | GlmAsrForConditionalGeneration | 7,745,560 |
| glmasr_encoder | [hf-tiny-v2/tiny-random-GlmAsrEncoder](https://huggingface.co/hf-tiny-v2/tiny-random-GlmAsrEncoder/tree/27f18b83a4436de2808c2c7d95ca66b4f2bbcb6a) | GlmAsrEncoder | 98,208 |
| got_ocr2 | [optimum-intel-internal-testing/tiny-random-got-ocr2-hf](https://huggingface.co/optimum-intel-internal-testing/tiny-random-got-ocr2-hf/tree/20ec62496705640b61c40f8930c1ff0e9b695b2a) | GotOcr2ForConditionalGeneration | 20,107,840 |
| gpt_neox_japanese | [hf-tiny-v2/tiny-random-GPTNeoXJapaneseModel](https://huggingface.co/hf-tiny-v2/tiny-random-GPTNeoXJapaneseModel/tree/d3ba479de5c1896c6cf82a85b677566dd942d107) | GPTNeoXJapaneseModel | 4,197,720 |
| granite | [optimum-intel-internal-testing/tiny-random-granite](https://huggingface.co/optimum-intel-internal-testing/tiny-random-granite/tree/4d299557bdac1039e208ff71c25a73ea9ee185ad) | GraniteForCausalLM | 6,668,040 |
| granite4_vision | [inference-optimization/granite-vision-4.1-0.2B-tiny](https://huggingface.co/inference-optimization/granite-vision-4.1-0.2B-tiny/tree/8d5f5812a58046b01b3dab6fe7a99d9b38ca3523) | Granite4VisionForConditionalGeneration | 325,012,776 |
| granite_speech5_encoder | [hf-tiny-v2/tiny-random-GraniteSpeech5Encoder](https://huggingface.co/hf-tiny-v2/tiny-random-GraniteSpeech5Encoder/tree/f02d12cb385dfc312a1cff0dcdcb7afe7f2024a0) | GraniteSpeech5Encoder | 4,480,176 |
| granite_speech_plus | [hf-tiny-v2/tiny-random-GraniteSpeechPlusForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-GraniteSpeechPlusForConditionalGeneration/tree/e7de20b8d51a90e535ba518758613278e8e8ff0f) | GraniteSpeechPlusForConditionalGeneration | 13,499,304 |
| granite_swa | [hf-tiny-v2/tiny-random-GraniteSWAForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-GraniteSWAForCausalLM/tree/295078a174399e57aa50d9c1327375d26bc013f1) | GraniteSWAForCausalLM | 25,750,536 |
| granitemoe | [optimum-intel-internal-testing/tiny-random-granite-moe](https://huggingface.co/optimum-intel-internal-testing/tiny-random-granite-moe/tree/70a5c7ff177b73147efb591b8c36d02e45fed425) | GraniteMoeForCausalLM | 13,186,216 |
| granitemoe_swa | [hf-tiny-v2/tiny-random-GraniteMoeSWAForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-GraniteMoeSWAForCausalLM/tree/0245cfe8271acf3d7d71bec5ab04498911967db2) | GraniteMoeSWAForCausalLM | 25,924,704 |
| granitemoehybrid | [optimum-intel-internal-testing/tiny-random-granitemoehybrid](https://huggingface.co/optimum-intel-internal-testing/tiny-random-granitemoehybrid/tree/a668c67a10c7fa4f0ea88b5762904adbe4826d34) | GraniteMoeHybridForCausalLM | 27,482,000 |
| granitemoeshared | [hf-tiny-v2/tiny-random-GraniteMoeSharedForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-GraniteMoeSharedForCausalLM/tree/1774e594784e06181e6097d1344e490ea00c7cd7) | GraniteMoeSharedForCausalLM | 13,001,584 |
| helium | [hf-tiny-v2/tiny-random-HeliumForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-HeliumForCausalLM/tree/91ca023afafc7dca3aef6830a239f6d779bbe46b) | HeliumForCausalLM | 12,348,208 |
| higgs_audio_v2 | [hf-tiny-v2/tiny-random-HiggsAudioV2ForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-HiggsAudioV2ForConditionalGeneration/tree/93901d1429b8ff3de4f8bb695830a86a6070d40b) | HiggsAudioV2ForConditionalGeneration | 16,519,168 |
| hunyuan_v1_dense | [optimum-intel-internal-testing/tiny-random-hunyuan-v1-dense](https://huggingface.co/optimum-intel-internal-testing/tiny-random-hunyuan-v1-dense/tree/7a5e67c9dfd91d72f85bdfedc01ed7a1e79f5e77) | HunYuanDenseV1ForCausalLM | 452,632 |
| hunyuan_v1_moe | [hf-tiny-v2/tiny-random-HunYuanMoEV1ForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-HunYuanMoEV1ForCausalLM/tree/68fc9e9fd12277763e15600d739593055684d3d5) | HunYuanMoEV1ForCausalLM | 33,075,832 |
| hunyuan_vl | [hf-tiny-v2/tiny-random-HunYuanVLForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-HunYuanVLForConditionalGeneration/tree/8fa772eb005e1f3f0236b8d69776631730dcea22) | HunYuanVLForConditionalGeneration | 62,897,976 |
| hunyuan_vl_text | [hf-tiny-v2/tiny-random-HunYuanVLTextModel](https://huggingface.co/hf-tiny-v2/tiny-random-HunYuanVLTextModel/tree/7ed24fb6705b29de54895ae056a79ad848344757) | HunYuanVLTextModel | 31,261,080 |
| hunyuan_vl_vision | [hf-tiny-v2/tiny-random-HunYuanVLVisionTransformer](https://huggingface.co/hf-tiny-v2/tiny-random-HunYuanVLVisionTransformer/tree/3e139fe7bba65af4ce39cc3553bc39e5e11cb36b) | HunYuanVLVisionTransformer | 706,824 |
| hy_v4 | [hf-tiny-v2/tiny-random-HYV4ForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-HYV4ForCausalLM/tree/122429951a115aabfd73c510c5ad267945f00228) | HYV4ForCausalLM | 31,049,724 |
| hyperclovax | [hf-tiny-v2/tiny-random-HyperCLOVAXForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-HyperCLOVAXForCausalLM/tree/f03fa0ea60e003abbbae945090d6176b38d69a4d) | HyperCLOVAXForCausalLM | 28,355,264 |
| hyperclovax_vision_v2 | [hf-tiny-v2/tiny-random-HyperCLOVAXVisionV2Model](https://huggingface.co/hf-tiny-v2/tiny-random-HyperCLOVAXVisionV2Model/tree/6c9ab67b320f69221a7005805a4a6afb77c9c79a) | HyperCLOVAXVisionV2Model | 16,704,320 |
| idefics3_vision | [hf-tiny-v2/tiny-random-Idefics3VisionTransformer](https://huggingface.co/hf-tiny-v2/tiny-random-Idefics3VisionTransformer/tree/8c55bf54522973c1c1beff8474f3c8b5a5706887) | Idefics3VisionTransformer | 63,896 |
| ijepa | [hf-tiny-v2/tiny-random-IJepaModel](https://huggingface.co/hf-tiny-v2/tiny-random-IJepaModel/tree/f1d0b90a6e9260ecf879df7da13b37c354fd1177) | IJepaModel | 88,848 |
| informer | [JLB-JLB/EEG_Informer_336_history_96_horizon](https://huggingface.co/JLB-JLB/EEG_Informer_336_history_96_horizon/tree/39fab1c701981d27cf5bf49daabb51705c3277f5) | InformerForPrediction | 97,471,320 |
| inkling_text | [hf-tiny-v2/tiny-random-InklingTextModel](https://huggingface.co/hf-tiny-v2/tiny-random-InklingTextModel/tree/473bad6738683b2a889a810f56df9fd5bf8feaff) | InklingTextModel | 25,881,480 |
| instructblip | [hf-tiny-v2/tiny-random-InstructBlipForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-InstructBlipForConditionalGeneration/tree/c0c25f998cce6cf8069c0652ee1b4c18086a75ff) | InstructBlipForConditionalGeneration | 2,351,512 |
| instructblipvideo | [hf-tiny-v2/tiny-random-InstructBlipVideoForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-InstructBlipVideoForConditionalGeneration/tree/082804b707752901d3020bea91cd622c5c7126ab) | InstructBlipVideoForConditionalGeneration | 2,351,512 |
| internvl_vision | [hf-tiny-v2/tiny-random-InternVLVisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-InternVLVisionModel/tree/f8f5e52e9d4cc4255b0879fee5d5b069d8148e4f) | InternVLVisionModel | 144,048 |
| jais2 | [hf-tiny-v2/tiny-random-Jais2ForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-Jais2ForCausalLM/tree/6156dd68bd73bde130853e3c5f241db17aabe0e3) | Jais2ForCausalLM | 38,512,552 |
| jamba | [ai21labs/Jamba-tiny-dev](https://huggingface.co/ai21labs/Jamba-tiny-dev/tree/ed303361004ac875426a61675edecf8e9d976882) | JambaForCausalLM | 637,428,728 |
| janus | [hf-tiny-v2/tiny-random-JanusForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-JanusForConditionalGeneration/tree/e0e4657405742a400c9d62ba1adb302ffe4a829c) | JanusForConditionalGeneration | 14,335,060 |
| jetmoe | [hf-tiny-v2/tiny-random-JetMoeForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-JetMoeForCausalLM/tree/236ca328ccfedeb09989bfb2188b6fbb0cae5afc) | JetMoeForCausalLM | 8,352,568 |
| jina_embeddings_v3 | [hf-tiny-v2/tiny-random-JinaEmbeddingsV3ForQuestionAnswering](https://huggingface.co/hf-tiny-v2/tiny-random-JinaEmbeddingsV3ForQuestionAnswering/tree/55bbd95c07c2cda17fb2cef0eb70f284ccf54b30) | JinaEmbeddingsV3ForQuestionAnswering | 16,018,200 |
| kosmos-2 | [hf-tiny-v2/tiny-random-Kosmos2ForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-Kosmos2ForConditionalGeneration/tree/16ff91ba61c528ac8829208e2b90a37ca2aaa777) | Kosmos2ForConditionalGeneration | 8,481,984 |
| kosmos-2.5 | [hf-tiny-v2/tiny-random-Kosmos2_5ForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-Kosmos2_5ForConditionalGeneration/tree/08a7d7b67e9d2707222422779aefd385aa09d7fc) | Kosmos2_5ForConditionalGeneration | 15,350,000 |
| kosmos_2_5_vision_model | [Fireblossom/kosmos-2.5-4bit-vision](https://huggingface.co/Fireblossom/kosmos-2.5-4bit-vision/tree/2936494b439796d0073cfef454940d55b22bf870) | Kosmos2_5VisionModel | 306,710,574 |
| kyutai_speech_to_text | [hf-tiny-v2/tiny-random-KyutaiSpeechToTextModel](https://huggingface.co/hf-tiny-v2/tiny-random-KyutaiSpeechToTextModel/tree/03b794c9706e6d555d0e67091ad469b606b349d5) | KyutaiSpeechToTextModel | 2,660,144 |
| laguna | [hf-tiny-v2/tiny-random-LagunaForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-LagunaForCausalLM/tree/dd1f1c4abf2cf6fe06fac6af0e67a6d13203ec48) | LagunaForCausalLM | 25,782,280 |
| lasr_encoder | [hf-tiny-v2/tiny-random-LasrEncoder](https://huggingface.co/hf-tiny-v2/tiny-random-LasrEncoder/tree/bc31950d400e810c7a99646e4dca205c48a08f34) | LasrEncoder | 919,952 |
| layoutlmv3 | [microsoft/layoutlmv3-base](https://huggingface.co/microsoft/layoutlmv3-base/tree/cfbbbff0762e6aab37086fdd4739ad14fe7d5db4) | unspecified | 501,338,056 |
| lfm2_moe | [optimum-intel-internal-testing/tiny-random-lfm2-moe](https://huggingface.co/optimum-intel-internal-testing/tiny-random-lfm2-moe/tree/02c3a7a04fbf627a14929e8f55e98e2c5328e7b5) | Lfm2MoeForCausalLM | 4,659,904 |
| lighton_ocr | [hf-tiny-v2/tiny-random-LightOnOcrForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-LightOnOcrForConditionalGeneration/tree/0b6ef6386f00833797ae19a899e85a350e582c63) | LightOnOcrForConditionalGeneration | 19,635,192 |
| llava_next | [optimum-intel-internal-testing/tiny-random-llava-next](https://huggingface.co/optimum-intel-internal-testing/tiny-random-llava-next/tree/0396be1d2d24cfc4cbbddcec0eaab582d856d55e) | LlavaNextForConditionalGeneration | 4,225,912 |
| llava_next_video | [optimum-intel-internal-testing/tiny-random-llava-next-video](https://huggingface.co/optimum-intel-internal-testing/tiny-random-llava-next-video/tree/bd9472e12c4851b650e277e7247c280b4e4e9aa5) | LlavaNextVideoForConditionalGeneration | 4,229,880 |
| llava_onevision | [hf-tiny-v2/tiny-random-LlavaOnevisionForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-LlavaOnevisionForConditionalGeneration/tree/daaab174fdc52c9658e9839009e83afe016155bb) | LlavaOnevisionForConditionalGeneration | 39,009,028 |
| lw_detr_vit | [hf-tiny-v2/tiny-random-LwDetrViTBackbone](https://huggingface.co/hf-tiny-v2/tiny-random-LwDetrViTBackbone/tree/bb2c5113dcb8e8de0808600a26587350a6d31688) | LwDetrViTBackbone | 121,600 |
| lxmert | [hf-tiny-v2/tiny-random-LxmertForQuestionAnswering](https://huggingface.co/hf-tiny-v2/tiny-random-LxmertForQuestionAnswering/tree/e23bd2c9fcc57500362c22d18a0df8a8abff7d14) | LxmertForQuestionAnswering | 3,645,464 |
| m2m_100 | [stefan7/pocket_polyglot_mzansi_50M_6langs](https://huggingface.co/stefan7/pocket_polyglot_mzansi_50M_6langs/tree/ca5f449945c340bd83587a589447173fc65d5f02) | M2M100ForConditionalGeneration | 197,071,520 |
| mamba2 | [AntonV/mamba2-130m-hf](https://huggingface.co/AntonV/mamba2-130m-hf/tree/05e8773fc4ac1cd067e8a18a5c45372ce5178405) | unspecified | 515,981,536 |
| mbart | [akreal/tiny-random-mbart](https://huggingface.co/akreal/tiny-random-mbart/tree/b416556f12c0346cf524c0a1a48953abc86d664c) | unspecified | 121,272 |
| mellum | [hf-tiny-v2/tiny-random-MellumForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-MellumForCausalLM/tree/98cece457dadd04bff5cfdc4204e34111e2804c9) | MellumForCausalLM | 25,267,128 |
| mimo_v2_flash | [hf-tiny-v2/tiny-random-MiMoV2FlashForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-MiMoV2FlashForCausalLM/tree/5573196d9fe70dc6fc268c4e11bcc435294cf1bb) | MiMoV2FlashForCausalLM | 38,924,224 |
| minicpm3 | [optimum-intel-internal-testing/tiny-random-minicpm3](https://huggingface.co/optimum-intel-internal-testing/tiny-random-minicpm3/tree/cab33fd70c4342003f2b5e9397f4b9299938d705) | MiniCPM3ForCausalLM | 79,239,744 |
| minicpmv4_6 | [hf-tiny-v2/tiny-random-MiniCPMV4_6ForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-MiniCPMV4_6ForConditionalGeneration/tree/a62e987e0152d227246e2166ddf1e73f5b8f6256) | MiniCPMV4_6ForConditionalGeneration | 128,675,400 |
| minicpmv4_7 | [optimum-intel-internal-testing/tiny-random-minicpmv47](https://huggingface.co/optimum-intel-internal-testing/tiny-random-minicpmv47/tree/fde0780039c3ac635b69c2769a49f71c86992dc4) | MiniCPMV4_7ForConditionalGeneration | 8,494,616 |
| minicpmv4_7_vision | [hf-tiny-v2/tiny-random-MiniCPMV4_7VisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-MiniCPMV4_7VisionModel/tree/b9990fb9c0c38603ceb32bcf3ef87760b1415718) | MiniCPMV4_7VisionModel | 1,053,768 |
| minimax_m3_vl_text | [hf-tiny-v2/tiny-random-MiniMaxM3VLTextModel](https://huggingface.co/hf-tiny-v2/tiny-random-MiniMaxM3VLTextModel/tree/70a8831e4077d9de5c3542dcffe6a544215023fa) | MiniMaxM3VLTextModel | 25,876,920 |
| mistral3 | [optimum-intel-internal-testing/tiny-random-mistral3](https://huggingface.co/optimum-intel-internal-testing/tiny-random-mistral3/tree/42f8d5400fdfd254f7c2b6dfb41b14ff24872887) | Mistral3ForConditionalGeneration | 67,988,584 |
| mixtral | [axolotl-ai-co/tiny-mixtral-30m](https://huggingface.co/axolotl-ai-co/tiny-mixtral-30m/tree/99512191d2561cb631b0d3176e59ade2d76b287b) | MixtralForCausalLM | 59,280,856 |
| mlcd_vision_model | [hf-tiny-v2/tiny-random-MLCDVisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-MLCDVisionModel/tree/4667ce0ca2052bb1ec71592b16da72366866da8e) | MLCDVisionModel | 60,232 |
| mllama | [axolotl-ai-co/Llama-3.2-39M-Vision](https://huggingface.co/axolotl-ai-co/Llama-3.2-39M-Vision/tree/ff80962141b4b914badbbf9f858dcf4ce68dea47) | MllamaForConditionalGeneration | 77,950,994 |
| mllama_text_model | [hf-tiny-v2/tiny-random-MllamaTextModel](https://huggingface.co/hf-tiny-v2/tiny-random-MllamaTextModel/tree/b9a1ed783875fb82d4ed64686029fdd1c1eeffe0) | MllamaTextModel | 16,482,232 |
| mllama_vision_model | [hf-tiny-v2/tiny-random-MllamaVisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-MllamaVisionModel/tree/65ea7100f2299209c3618e6bb47440c273d7980b) | MllamaVisionModel | 584,996 |
| mobilevit | [Abalogun96/mobilevit-finetuned](https://huggingface.co/Abalogun96/mobilevit-finetuned/tree/1d5f02f5c514c1bade079a2d2ab72de52ab8d366) | CustomResearchModel | 99,808 |
| moshi | [hf-tiny-v2/tiny-random-MoshiModel](https://huggingface.co/hf-tiny-v2/tiny-random-MoshiModel/tree/5f1056303743dbb49c496d02af68adc7414c5e1d) | MoshiModel | 4,143,648 |
| mra | [hf-tiny-v2/tiny-random-MraModel](https://huggingface.co/hf-tiny-v2/tiny-random-MraModel/tree/378b175263d483641bf02e113feb08df99152a38) | MraModel | 38,744 |
| mt5 | [optimum-internal-testing/tiny-random-mt5](https://huggingface.co/optimum-internal-testing/tiny-random-mt5/tree/aba7ae71634f55ad4b33b0d5ac9b72627fc67ca6) | MT5ForConditionalGeneration | 32,832,904 |
| muse_glimmer_assistant | [optimum-intel-internal-testing/tiny-random-muse-glimmer-assistant](https://huggingface.co/optimum-intel-internal-testing/tiny-random-muse-glimmer-assistant/tree/b27d71a25738d20091a8078bd21b347d65470354) | MuseGlimmerAssistantModel | 528,488 |
| muse_glimmer_text | [hf-tiny-v2/tiny-random-MuseGlimmerTextModel](https://huggingface.co/hf-tiny-v2/tiny-random-MuseGlimmerTextModel/tree/99fb634141b32f27db3b597bf2ff76e198db8979) | MuseGlimmerTextModel | 25,935,336 |
| muse_glimmer_vision | [hf-tiny-v2/tiny-random-MuseGlimmerVisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-MuseGlimmerVisionModel/tree/5dbba401b63a0dc7f68ed126008cc31f831a404a) | MuseGlimmerVisionModel | 63,208 |
| musicflamingo | [hf-tiny-v2/tiny-random-MusicFlamingoForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-MusicFlamingoForConditionalGeneration/tree/58b31893b3fcbca78a47bf7537f7999a33cf1ec6) | MusicFlamingoForConditionalGeneration | 39,001,576 |
| musicgen | [hf-tiny-v2/tiny-random-MusicgenForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-MusicgenForConditionalGeneration/tree/4606e560821ed4c10d76d6a6513c893ec3cf2ae0) | MusicgenForConditionalGeneration | 6,098,268 |
| musicgen_decoder | [hf-tiny-v2/tiny-random-MusicgenForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-MusicgenForCausalLM/tree/7b515183563e548e50ddb6c4c960e400c4c65d23) | MusicgenForCausalLM | 73,680 |
| musicgen_melody | [hf-tiny-v2/tiny-random-MusicgenMelodyForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-MusicgenMelodyForConditionalGeneration/tree/e29d40dcaa0587b15acbc636c1bd95618bf016eb) | MusicgenMelodyForConditionalGeneration | 6,089,324 |
| musicgen_melody_decoder | [hf-tiny-v2/tiny-random-MusicgenMelodyModel](https://huggingface.co/hf-tiny-v2/tiny-random-MusicgenMelodyModel/tree/713a05225a15cbda38fe8c55d16564d01dce96e3) | MusicgenMelodyModel | 38,048 |
| mvp | [hf-tiny-v2/tiny-random-MvpForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-MvpForConditionalGeneration/tree/f81637b0b75f40e80b85279bfe004a6f4b732ec9) | MvpForConditionalGeneration | 3,483,932 |
| nemotron3_5_asr | [hf-tiny-v2/tiny-random-Nemotron3_5AsrForRNNT](https://huggingface.co/hf-tiny-v2/tiny-random-Nemotron3_5AsrForRNNT/tree/3072ff616f7f0eebb80ac5f43509f6d9efb20d20) | Nemotron3_5AsrForRNNT | 4,379,172 |
| nemotron3_diarization_audio | [hf-tiny-v2/tiny-random-Nemotron3DiarizationAudioModel](https://huggingface.co/hf-tiny-v2/tiny-random-Nemotron3DiarizationAudioModel/tree/d110ef8a25bfdadc578c04e869c3e74630970a00) | Nemotron3DiarizationAudioModel | 62,400 |
| nemotron_asr_streaming | [hf-tiny-v2/tiny-random-NemotronAsrStreamingForRNNT](https://huggingface.co/hf-tiny-v2/tiny-random-NemotronAsrStreamingForRNNT/tree/df43199d652caf06ab35d8bdf1525259bec45910) | NemotronAsrStreamingForRNNT | 1,233,200 |
| nemotron_asr_streaming_encoder | [hf-tiny-v2/tiny-random-NemotronAsrStreamingEncoder](https://huggingface.co/hf-tiny-v2/tiny-random-NemotronAsrStreamingEncoder/tree/4fc444f6348591a523db420f663b3d3428cd9373) | NemotronAsrStreamingEncoder | 918,408 |
| nemotron_h_omni | [hf-tiny-v2/tiny-random-NemotronH_Omni_Reasoning_V3](https://huggingface.co/hf-tiny-v2/tiny-random-NemotronH_Omni_Reasoning_V3/tree/7033d558a1e04777c0172efb6659d554c6aa32cc) | NemotronH_Omni_Reasoning_V3 | 34,300,080 |
| neucodec | [hf-tiny-v2/tiny-random-NeuCodecModel](https://huggingface.co/hf-tiny-v2/tiny-random-NeuCodecModel/tree/c332ac745e6389f169c32f26b48d9828876b81b5) | NeuCodecModel | 3,877,816 |
| nllb-moe | [hf-tiny-v2/tiny-random-NllbMoeForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-NllbMoeForConditionalGeneration/tree/e138eaa9f2500e7dabf4226c10e7ffe482bfac98) | NllbMoeForConditionalGeneration | 16,447,272 |
| olmo | [optimum-intel-internal-testing/tiny-random-olmo-hf](https://huggingface.co/optimum-intel-internal-testing/tiny-random-olmo-hf/tree/2955c77d34355afee2f5e02c6c156d1931ff295c) | OlmoForCausalLM | 26,152,632 |
| olmo2 | [optimum-intel-internal-testing/tiny-random-olmo2](https://huggingface.co/optimum-intel-internal-testing/tiny-random-olmo2/tree/bcbd58e6547eda039f5afd2426de37e33193a443) | Olmo2ForCausalLM | 25,775,856 |
| olmo_hybrid | [hf-tiny-v2/tiny-random-OlmoHybridForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-OlmoHybridForCausalLM/tree/8dd30beef0c93c5f6cee1a97759eb0330ba00dc2) | OlmoHybridForCausalLM | 25,739,560 |
| olmoe | [hf-tiny-v2/tiny-random-OlmoeForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-OlmoeForCausalLM/tree/232ebf7e9097347b24527b877c9f9eb5e29fd4e1) | OlmoeForCausalLM | 13,013,656 |
| oneformer | [mieszkok/shi-labs_oneformer_ade20k_swin_large_geopose3k_original_images900_epochs5](https://huggingface.co/mieszkok/shi-labs_oneformer_ade20k_swin_large_geopose3k_original_images900_epochs5/tree/c480c80d18ba4d601f0884588044c11cd6477c4d) | OneFormerForUniversalSegmentation | 949,532,288 |
| ovis2 | [hf-tiny-v2/tiny-random-Ovis2ForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-Ovis2ForConditionalGeneration/tree/d61830ef46a36e0553dc752c941b149da21f84ae) | Ovis2ForConditionalGeneration | 39,442,704 |
| paligemma | [michaelfeil/colpali-v12-random-testing](https://huggingface.co/michaelfeil/colpali-v12-random-testing/tree/2c336fbceba2d8794c5bd396ec77156947487f4e) | ColPali | 16,845,392 |
| parakeet_encoder | [hf-tiny-v2/tiny-random-ParakeetEncoder](https://huggingface.co/hf-tiny-v2/tiny-random-ParakeetEncoder/tree/de18459224d4b420e1f27da81e3a41c7f0433935) | ParakeetEncoder | 911,680 |
| patchtsmixer | [ibm-research/patchtsmixer-etth1-pretrain](https://huggingface.co/ibm-research/patchtsmixer-etth1-pretrain/tree/05513838aadc1ab6b4fa2a851a29c6aceff354b7) | PatchTSMixerForPretraining | 202,200 |
| pe_audio | [hf-tiny-v2/tiny-random-PeAudioModel](https://huggingface.co/hf-tiny-v2/tiny-random-PeAudioModel/tree/92014d5d9f5964533ad7fcecc2b131d87a69861f) | PeAudioModel | 7,933,096 |
| pe_audio_encoder | [hf-tiny-v2/tiny-random-PeAudioEncoder](https://huggingface.co/hf-tiny-v2/tiny-random-PeAudioEncoder/tree/6da7982e13c906f299109f2bb85a5668c59a1c2d) | PeAudioEncoder | 1,411,832 |
| pe_audio_video_encoder | [hf-tiny-v2/tiny-random-PeAudioVideoEncoder](https://huggingface.co/hf-tiny-v2/tiny-random-PeAudioVideoEncoder/tree/5f647cc653e1c627e52932af93dffd5339098a6f) | PeAudioVideoEncoder | 2,849,640 |
| pe_video | [hf-tiny-v2/tiny-random-PeVideoModel](https://huggingface.co/hf-tiny-v2/tiny-random-PeVideoModel/tree/9bf11d27aaded0ee0e1397fc74ea50f133158bb3) | PeVideoModel | 7,379,360 |
| pe_video_encoder | [hf-tiny-v2/tiny-random-PeVideoEncoder](https://huggingface.co/hf-tiny-v2/tiny-random-PeVideoEncoder/tree/ce49848e29fdb776221b21efa3dfc16399def04a) | PeVideoEncoder | 858,232 |
| pegasus_x | [hf-tiny-v2/tiny-random-PegasusXForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-PegasusXForConditionalGeneration/tree/c0f6d6a3ba9d6663fc341e2f0b54a8d1d85a7238) | PegasusXForConditionalGeneration | 6,188,744 |
| perception_lm | [hf-tiny-v2/tiny-random-PerceptionLMModel](https://huggingface.co/hf-tiny-v2/tiny-random-PerceptionLMModel/tree/e1808685fbd6919f2ddbd5c2456c45a8b973e4b6) | PerceptionLMModel | 17,050,288 |
| persimmon | [hf-tiny-v2/tiny-random-PersimmonForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-PersimmonForCausalLM/tree/9f3c5cee2ed8e295df17f11cc42e3aebd58fbd19) | PersimmonForCausalLM | 67,165,216 |
| phi | [optimum-intel-internal-testing/tiny-random-PhiForCausalLM](https://huggingface.co/optimum-intel-internal-testing/tiny-random-PhiForCausalLM/tree/912e42c2101dd10c07c155d2c0ad49cb5b84a9d3) | PhiForCausalLM | 323,520 |
| phi4_multimodal | [hf-tiny-v2/tiny-random-Phi4MultimodalForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-Phi4MultimodalForCausalLM/tree/baa55fd1c85c7a535c8aae3249f80adfa7bf090d) | Phi4MultimodalForCausalLM | 52,990,704 |
| pixio | [hf-tiny-v2/tiny-random-PixioModel](https://huggingface.co/hf-tiny-v2/tiny-random-PixioModel/tree/f5602708f345e37ffa0ad582d6542833d322adf5) | PixioModel | 136,440 |
| pixtral | [nebulette/mistral-small-4-pixtral-vision-module](https://huggingface.co/nebulette/mistral-small-4-pixtral-vision-module/tree/0d67239d3be605f44990614d8175b4ed192af84e) | unspecified | 806,637,224 |
| pop2piano | [hf-tiny-v2/tiny-random-Pop2PianoForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-Pop2PianoForConditionalGeneration/tree/94c03982ef88e187b97daeecf8f153e51fa5875e) | Pop2PianoForConditionalGeneration | 1,752,304 |
| pp_formulanet | [PaddlePaddle/PP-FormulaNet_plus-L_safetensors](https://huggingface.co/PaddlePaddle/PP-FormulaNet_plus-L_safetensors/tree/6cc004a8e91ea3f3819b05317f40b290cbe99c2b) | unspecified | 727,633,048 |
| pp_lcnet_v3 | [hf-tiny-v2/tiny-random-PPLCNetV3Backbone](https://huggingface.co/hf-tiny-v2/tiny-random-PPLCNetV3Backbone/tree/d50e58a5feb5cd2e0242f164f5ee01eb4dfe8ae9) | PPLCNetV3Backbone | 577,528 |
| pp_lcnet_v4 | [hf-tiny-v2/tiny-random-PPLCNetV4Backbone](https://huggingface.co/hf-tiny-v2/tiny-random-PPLCNetV4Backbone/tree/a06b2adb778c3278e551814a362d3ad0e6f95485) | PPLCNetV4Backbone | 74,784 |
| pp_ocrv5_mobile_rec | [PaddlePaddle/korean_PP-OCRv5_mobile_rec_safetensors](https://huggingface.co/PaddlePaddle/korean_PP-OCRv5_mobile_rec_safetensors/tree/6ef525a357645ce46495c7ed1fef622c4e009e7a) | unspecified | 28,035,900 |
| prophetnet | [hf-tiny-v2/tiny-random-ProphetNetForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-ProphetNetForConditionalGeneration/tree/dc105124ec8a4129ed8e96fb31ea45bddf45b0ab) | ProphetNetForConditionalGeneration | 2,052,496 |
| qianfan_ocr | [hf-tiny-v2/tiny-random-QianfanOCRForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-QianfanOCRForConditionalGeneration/tree/da507fd542c7c01feeeacfd6a7514bd57c04734d) | QianfanOCRForConditionalGeneration | 157,792,584 |
| qianfan_ocr_vision | [hf-tiny-v2/tiny-random-QianfanOCRVisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-QianfanOCRVisionModel/tree/cae65f6f148764590f68e53ae2ac4cd59fec1f3f) | QianfanOCRVisionModel | 120,560 |
| qwen2_5_omni_bigvgan | [Ryan241005/scail-2](https://huggingface.co/Ryan241005/scail-2/tree/d60dadee5ffc0c9ec4d24d1d254ea114a2f727c3) | Qwen2_5OmniToken2WavBigVGANModel | 461,819,280 |
| qwen2_5_omni_thinker | [hf-tiny-v2/tiny-random-Qwen2_5OmniThinkerForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-Qwen2_5OmniThinkerForConditionalGeneration/tree/e55a0f8f25b0c2d4829c3320f4a166169d48dbcd) | Qwen2_5OmniThinkerForConditionalGeneration | 39,179,728 |
| qwen2_5_vl_text | [hf-tiny-v2/tiny-random-Qwen2_5_VLTextModel](https://huggingface.co/hf-tiny-v2/tiny-random-Qwen2_5_VLTextModel/tree/3d88ac2485f48cc590e717ba208662768db347e9) | Qwen2_5_VLTextModel | 19,468,848 |
| qwen2_5_vl_vision | [hf-tiny-v2/tiny-random-Qwen2_5_VisionTransformerPretrainedModel](https://huggingface.co/hf-tiny-v2/tiny-random-Qwen2_5_VisionTransformerPretrainedModel/tree/59c32e10413469ea4ede7bb78d00ee679ec7b7f6) | Qwen2_5_VisionTransformerPretrainedModel | 221,376 |
| qwen2_audio | [trl-internal-testing/tiny-Qwen2AudioForConditionalGeneration](https://huggingface.co/trl-internal-testing/tiny-Qwen2AudioForConditionalGeneration/tree/7bff21b2d3ceb00ee2addca1d99166121e62e093) | Qwen2AudioForConditionalGeneration | 10,074,096 |
| qwen2_audio_encoder | [hf-tiny-v2/tiny-random-Qwen2AudioEncoder](https://huggingface.co/hf-tiny-v2/tiny-random-Qwen2AudioEncoder/tree/d0393c20144b15b1ccba576968abc22d24783ac5) | Qwen2AudioEncoder | 123,888 |
| qwen2_moe | [optimum-intel-internal-testing/tiny-random-qwen1.5-moe](https://huggingface.co/optimum-intel-internal-testing/tiny-random-qwen1.5-moe/tree/ced93ed465ea0a1833d5efe342b6be11596245a6) | Qwen2MoeForCausalLM | 39,543,400 |
| qwen2_vl_text | [hf-tiny-v2/tiny-random-Qwen2VLTextModel](https://huggingface.co/hf-tiny-v2/tiny-random-Qwen2VLTextModel/tree/8e524159e711c11ee700c298ed55d773bc95328e) | Qwen2VLTextModel | 19,468,848 |
| qwen3_5_moe_vision | [hf-tiny-v2/tiny-random-Qwen3_5MoeVisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-Qwen3_5MoeVisionModel/tree/4e0006af514b9274f75c3402b877a19feca78e64) | Qwen3_5MoeVisionModel | 262,056 |
| qwen3_5_text | [fromziro/ZeroS-v0.1-150M](https://huggingface.co/fromziro/ZeroS-v0.1-150M/tree/023a2d5a56f79f11951e55e77565591473f77387) | Qwen3_5ForCausalLM | 606,594,536 |
| qwen3_asr_encoder | [hf-tiny-v2/tiny-random-Qwen3ASREncoder](https://huggingface.co/hf-tiny-v2/tiny-random-Qwen3ASREncoder/tree/4564641d4cd43e2bc1400cc06e54f159ad905eb7) | Qwen3ASREncoder | 11,136 |
| qwen3_omni_moe | [optimum-intel-internal-testing/tiny-random-qwen3-omni](https://huggingface.co/optimum-intel-internal-testing/tiny-random-qwen3-omni/tree/3a9fc2b3412a8da231d5a5b25d2b548a62d5b52f) | Qwen3OmniMoeForConditionalGeneration | 12,939,316 |
| qwen3_omni_moe_thinker | [hf-tiny-v2/tiny-random-Qwen3OmniMoeThinkerForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-Qwen3OmniMoeThinkerForConditionalGeneration/tree/687ec6cbe4aedb316c4901c7cad93113712cc785) | Qwen3OmniMoeThinkerForConditionalGeneration | 40,004,920 |
| qwen3_vl_moe_text | [hf-tiny-v2/tiny-random-Qwen3VLMoeTextModel](https://huggingface.co/hf-tiny-v2/tiny-random-Qwen3VLMoeTextModel/tree/91ca84943de9940ae33f0fccdfddd2d4e1542298) | Qwen3VLMoeTextModel | 19,541,752 |
| qwen3_vl_moe_vision | [hf-tiny-v2/tiny-random-Qwen3VLMoeVisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-Qwen3VLMoeVisionModel/tree/1424ff75616c81c32ce8e19e9e0f2e4790c91156) | Qwen3VLMoeVisionModel | 280,664 |
| qwen3_vl_text | [hf-tiny-v2/tiny-random-Qwen3VLTextModel](https://huggingface.co/hf-tiny-v2/tiny-random-Qwen3VLTextModel/tree/4fe68dbd01f01b2e33885dab8eff5212541a10b4) | Qwen3VLTextModel | 19,465,968 |
| qwen3_vl_vision | [hf-tiny-v2/tiny-random-Qwen3VLVisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-Qwen3VLVisionModel/tree/9b719df815e0872e5c0a17a2eac72a6851df1075) | Qwen3VLVisionModel | 280,664 |
| radio | [hf-tiny-v2/tiny-random-RadioModel](https://huggingface.co/hf-tiny-v2/tiny-random-RadioModel/tree/6649a51405d781bfcfcbf4ac1b3285d9ab4f6a8d) | RadioModel | 29,064 |
| rembert | [hf-tiny-v2/tiny-random-RemBertModel](https://huggingface.co/hf-tiny-v2/tiny-random-RemBertModel/tree/271dc96cb6f178bcb167b2e90bb12aa4192c100a) | RemBertModel | 18,125,128 |
| rf_detr_dinov2 | [hf-tiny-v2/tiny-random-RfDetrDinov2Backbone](https://huggingface.co/hf-tiny-v2/tiny-random-RfDetrDinov2Backbone/tree/febcd9390c3a8ec081e8c1200b0204cea0a2d470) | RfDetrDinov2Backbone | 344,064 |
| rt_detr_resnet | [hf-tiny-v2/tiny-random-RTDetrResNetBackbone](https://huggingface.co/hf-tiny-v2/tiny-random-RTDetrResNetBackbone/tree/89aee0111cd56603132cc5bc12a1a958d6d11412) | RTDetrResNetBackbone | 162,348 |
| rt_detr_v2 | [docling-project/docling-layout-heron](https://huggingface.co/docling-project/docling-layout-heron/tree/8f39ad3c0b4c58e9c2d2c84a38465abf757272d8) | RTDetrV2ForObjectDetection | 171,658,996 |
| sam2 | [facebook/sam2-hiera-base-plus-hf](https://huggingface.co/facebook/sam2-hiera-base-plus-hf/tree/ce622d7f03acbcf90e80483d094c2268437988ce) | Sam2Model | 323,407,992 |
| sam2_hiera_det_model | [hf-tiny-v2/tiny-random-Sam2HieraDetModel](https://huggingface.co/hf-tiny-v2/tiny-random-Sam2HieraDetModel/tree/4f280589ecf94801935e0a5ff96007614672034b) | Sam2HieraDetModel | 1,729,696 |
| sam2_vision_model | [hf-tiny-v2/tiny-random-Sam2VisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-Sam2VisionModel/tree/38ecebfa31a1e60ead6345d6277ebe27ac4c7a72) | Sam2VisionModel | 1,755,328 |
| sam3_lite_text | [hf-tiny-v2/tiny-random-Sam3LiteTextModel](https://huggingface.co/hf-tiny-v2/tiny-random-Sam3LiteTextModel/tree/891074ccedb40668fcc43dff3a198d79885355c3) | Sam3LiteTextModel | 7,310,760 |
| sam3_lite_text_text_model | [hf-tiny-v2/tiny-random-Sam3LiteTextTextModel](https://huggingface.co/hf-tiny-v2/tiny-random-Sam3LiteTextTextModel/tree/519e005a7bf45c32c81b723a9f4e5508185cfb10) | Sam3LiteTextTextModel | 6,426,048 |
| sam3_tracker | [hf-tiny-v2/tiny-random-Sam3TrackerModel](https://huggingface.co/hf-tiny-v2/tiny-random-Sam3TrackerModel/tree/efca257b1f94aed0db091f539eeb4d324d492532) | Sam3TrackerModel | 549,236 |
| sam3_video | [mlx-community/sam3-4bit](https://huggingface.co/mlx-community/sam3-4bit/tree/53c009b4ef4cfa5b1d9fa4549e7b153e881b5636) | Sam3VideoModel | 620,400,791 |
| sam3_vision_model | [hf-tiny-v2/tiny-random-Sam3VisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-Sam3VisionModel/tree/94cf25e199df4984d3885b5e13ff73f96ac2d7fb) | Sam3VisionModel | 310,880 |
| sam3_vit_model | [hf-tiny-v2/tiny-random-Sam3ViTModel](https://huggingface.co/hf-tiny-v2/tiny-random-Sam3ViTModel/tree/df8e3ac7ec020e3f93f97351a0db98919dd917e8) | Sam3ViTModel | 220,944 |
| sam_hq_vision_model | [hf-tiny-v2/tiny-random-SamHQVisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-SamHQVisionModel/tree/b8ae0ead2ba30ca372eba6cbf71c4afcfbe5e1cc) | SamHQVisionModel | 874,040 |
| sam_vision_model | [hf-tiny-v2/tiny-random-SamVisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-SamVisionModel/tree/10617976eb87d8d859a00863665674356245aff6) | SamVisionModel | 200,432 |
| seamless_m4t_v2 | [hf-tiny-v2/tiny-random-SeamlessM4Tv2ForSpeechToText](https://huggingface.co/hf-tiny-v2/tiny-random-SeamlessM4Tv2ForSpeechToText/tree/a345db8ba4e159ca35a675a002e20d08428733c0) | SeamlessM4Tv2ForSpeechToText | 6,187,672 |
| seggpt | [hf-tiny-v2/tiny-random-SegGptModel](https://huggingface.co/hf-tiny-v2/tiny-random-SegGptModel/tree/eda2b7bb97b1bd2d783f67d0d9b0237eece89f23) | SegGptModel | 114,944 |
| siglip2_vision_model | [hf-tiny-v2/tiny-random-Siglip2VisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-Siglip2VisionModel/tree/c18e32edfe2b6098634cf0d28f093f77b9670e54) | Siglip2VisionModel | 273,052 |
| siglip_text_model | [carsonpoole/binary-siglip-text](https://huggingface.co/carsonpoole/binary-siglip-text/tree/9791d56ba6e0a498e27fe35d6320ca4fe3434151) | SiglipTextModel | 908,812,128 |
| siglip_vision_model | [jingyaogong/siglip2-base-p32-256-ve](https://huggingface.co/jingyaogong/siglip2-base-p32-256-ve/tree/9465d1dc89db6bc6227c5b6b0e0ca9b940325d62) | SiglipVisionModel | 189,129,296 |
| slanet | [PaddlePaddle/SLANet_plus_safetensors](https://huggingface.co/PaddlePaddle/SLANet_plus_safetensors/tree/e44d12b3fe695792170dd46623075f63d8544461) | unspecified | 7,442,848 |
| smollm3 | [optimum-intel-internal-testing/tiny-random-smollm3](https://huggingface.co/optimum-intel-internal-testing/tiny-random-smollm3/tree/900f28f5d02cb30217eb94e0bb16196b5ca2143a) | SmolLM3ForCausalLM | 16,493,280 |
| smolvlm | [optimum-intel-internal-testing/tiny-random-smolvlm2](https://huggingface.co/optimum-intel-internal-testing/tiny-random-smolvlm2/tree/1f845a69959bb8c6a743228aa59936a4a83d49e5) | SmolVLMForConditionalGeneration | 27,718,504 |
| smolvlm_vision | [hf-tiny-v2/tiny-random-SmolVLMVisionTransformer](https://huggingface.co/hf-tiny-v2/tiny-random-SmolVLMVisionTransformer/tree/cb5d884a431b1513034a251b5213c62972e2e123) | SmolVLMVisionTransformer | 63,896 |
| speech-encoder-decoder | [hf-tiny-v2/tiny-random-SpeechEncoderDecoderModel-wav2vec2-bert](https://huggingface.co/hf-tiny-v2/tiny-random-SpeechEncoderDecoderModel-wav2vec2-bert/tree/3c3928bc6d2e32d9d23551975b547b9cacedf17c) | SpeechEncoderDecoderModel | 4,297,432 |
| stablelm | [optimum-intel-internal-testing/tiny-random-StableLmForCausalLM](https://huggingface.co/optimum-intel-internal-testing/tiny-random-StableLmForCausalLM/tree/9e45ffb429225f634c2719ea78d67610d1326907) | StableLmForCausalLM | 717,384 |
| starcoder2 | [optimum-intel-internal-testing/tiny-random-Starcoder2ForCausalLM](https://huggingface.co/optimum-intel-internal-testing/tiny-random-Starcoder2ForCausalLM/tree/30fa0238c4ce6faae10b5b2f6d9a89d2ad1ccd0b) | Starcoder2ForCausalLM | 180,688 |
| step3p7 | [hf-tiny-v2/tiny-random-Step3p7ForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-Step3p7ForConditionalGeneration/tree/c9db19ad894803e5a2fd62c2667a272668b4d3d9) | Step3p7ForConditionalGeneration | 16,545,472 |
| superglue | [magic-leap-community/superglue_indoor](https://huggingface.co/magic-leap-community/superglue_indoor/tree/413dc1d8a2b02aabea6ea6e24c62d9dcf1857705) | SuperGlueForKeypointMatching | 53,413,232 |
| switch_transformers | [hf-tiny-v2/tiny-random-SwitchTransformersForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-SwitchTransformersForConditionalGeneration/tree/aea93cf78d123ed3c4e254ccbd137f7ec9d9a037) | SwitchTransformersForConditionalGeneration | 4,251,856 |
| t5gemma2 | [hf-tiny-v2/tiny-random-T5Gemma2ForSequenceClassification](https://huggingface.co/hf-tiny-v2/tiny-random-T5Gemma2ForSequenceClassification/tree/b0ea72cdfe6d488602a528816a189c9f9d5079a3) | T5Gemma2ForSequenceClassification | 231,684 |
| t5gemma2_encoder | [hf-tiny-v2/tiny-random-T5Gemma2Encoder](https://huggingface.co/hf-tiny-v2/tiny-random-T5Gemma2Encoder/tree/bb396604413b6b9f61b4434f82919e83a7a33469) | T5Gemma2Encoder | 33,715,028 |
| t5gemma2_text | [amanchoudhri/t5-gemma-2-270m-text-encoder](https://huggingface.co/amanchoudhri/t5-gemma-2-270m-text-encoder/tree/361b981af65ce58d99193887961c401d0ce5ec2f) | T5Gemma2TextEncoder | 536,223,144 |
| timm_backbone | [hf-tiny-v2/tiny-random-TimmBackbone](https://huggingface.co/hf-tiny-v2/tiny-random-TimmBackbone/tree/677e52b22abbaf2777f29693365ffe372b67832a) | TimmBackbone | 44,756,448 |
| tipsv2_text_model | [hf-tiny-v2/tiny-random-Tipsv2TextModel](https://huggingface.co/hf-tiny-v2/tiny-random-Tipsv2TextModel/tree/362359b58ef830ff784a1ea333ad78f30e735d4e) | Tipsv2TextModel | 2,068,696 |
| tipsv2_vision_model | [hf-tiny-v2/tiny-random-Tipsv2VisionBackbone](https://huggingface.co/hf-tiny-v2/tiny-random-Tipsv2VisionBackbone/tree/118221bde4d6a595bf77aab666bfadbda8862741) | Tipsv2VisionBackbone | 59,352 |
| trocr | [optimum-internal-testing/tiny-random-TrocrForCausalLM](https://huggingface.co/optimum-internal-testing/tiny-random-TrocrForCausalLM/tree/c6f97c59ea3eef37d23f370b7ccb4634b13e4dd5) | TrOCRForCausalLM | 4,127,728 |
| tvp | [hf-tiny-v2/tiny-random-TvpModel](https://huggingface.co/hf-tiny-v2/tiny-random-TvpModel/tree/e94fe0efcc3e9231c67fb3da1bf960654e059753) | TvpModel | 7,681,208 |
| udop | [hf-tiny-v2/tiny-random-UdopForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-UdopForConditionalGeneration/tree/807c1e4f957ab18b59b2beba37fd4a525ad90586) | UdopForConditionalGeneration | 4,855,832 |
| unispeech | [hf-tiny-v2/tiny-random-UniSpeechModel](https://huggingface.co/hf-tiny-v2/tiny-random-UniSpeechModel/tree/881849537ef977431cfb91932e1f307189bac14a) | UniSpeechModel | 97,144 |
| univnet | [hf-tiny-v2/tiny-random-UnivNetModel](https://huggingface.co/hf-tiny-v2/tiny-random-UnivNetModel/tree/68c6e6d6a8757c018d4792e4b5ad5e9a937e31d0) | UnivNetModel | 535,452 |
| uvdoc_backbone | [hf-tiny-v2/tiny-random-UVDocBackbone](https://huggingface.co/hf-tiny-v2/tiny-random-UVDocBackbone/tree/2dad6d52bd120cf1bcde4d9e5f404b6aee7d7e2f) | UVDocBackbone | 1,595,544 |
| vaultgemma | [hf-tiny-v2/tiny-random-VaultGemmaForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-VaultGemmaForCausalLM/tree/a87c179d7b48c9fbd2ff0b6298f7aee6d6b74160) | VaultGemmaForCausalLM | 65,596,216 |
| vibevoice_acoustic_tokenizer | [hf-tiny-v2/tiny-random-VibeVoiceAcousticTokenizerModel](https://huggingface.co/hf-tiny-v2/tiny-random-VibeVoiceAcousticTokenizerModel/tree/a599ccfe8bf5930242bcf61bc3c86753661c8866) | VibeVoiceAcousticTokenizerModel | 459,316 |
| vibevoice_acoustic_tokenizer_decoder | [hf-tiny-v2/tiny-random-VibeVoiceAcousticTokenizerDecoderModel](https://huggingface.co/hf-tiny-v2/tiny-random-VibeVoiceAcousticTokenizerDecoderModel/tree/135420f1c994a2b5e93e96944ec5f6b2f18e2e7a) | VibeVoiceAcousticTokenizerDecoderModel | 229,388 |
| vibevoice_acoustic_tokenizer_encoder | [hf-tiny-v2/tiny-random-VibeVoiceAcousticTokenizerEncoderModel](https://huggingface.co/hf-tiny-v2/tiny-random-VibeVoiceAcousticTokenizerEncoderModel/tree/255a58bf008b59684051c06436c6f8f17442ca1b) | VibeVoiceAcousticTokenizerEncoderModel | 229,536 |
| vibevoice_asr | [hf-tiny-v2/tiny-random-VibeVoiceAsrForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-VibeVoiceAsrForConditionalGeneration/tree/d6d185dc1f3aa1720a3bbaf2fe372e55cd840328) | VibeVoiceAsrForConditionalGeneration | 39,355,864 |
| video_llama_3 | [hf-tiny-v2/tiny-random-VideoLlama3ForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-VideoLlama3ForConditionalGeneration/tree/5dcec0a11dad39d1201df24d64f036c361d11d8f) | VideoLlama3ForConditionalGeneration | 19,627,648 |
| video_llama_3_vision | [hf-tiny-v2/tiny-random-VideoLlama3VisionModel](https://huggingface.co/hf-tiny-v2/tiny-random-VideoLlama3VisionModel/tree/85b4907a209a71330c927e8ab8fdf0db0006c1b7) | VideoLlama3VisionModel | 181,240 |
| video_llava | [hf-tiny-v2/tiny-random-VideoLlavaModel](https://huggingface.co/hf-tiny-v2/tiny-random-VideoLlavaModel/tree/a694bf6f071230de91446483de1a44641d05ba02) | VideoLlavaModel | 4,316,096 |
| vipllava | [hf-tiny-v2/tiny-random-VipLlavaForConditionalGeneration](https://huggingface.co/hf-tiny-v2/tiny-random-VipLlavaForConditionalGeneration/tree/6d0ea3e9800f59488d95538994fa4ccb75570b4f) | VipLlavaForConditionalGeneration | 8,346,656 |
| vision-encoder-decoder | [vikp/surya_order](https://huggingface.co/vikp/surya_order/tree/7b727d0a2c942cdc8596d186115f65c12c812bd8) | OrderVisionEncoderDecoderModel | 550,040,752 |
| vision-text-dual-encoder | [hf-tiny-v2/tiny-random-VisionTextDualEncoderModel-vit-bert](https://huggingface.co/hf-tiny-v2/tiny-random-VisionTextDualEncoderModel-vit-bert/tree/5f0a6ff7d948c143495850486aa735315e1f06c6) | VisionTextDualEncoderModel | 4,263,268 |
| vit_mae | [facebook/vit-mae-base](https://huggingface.co/facebook/vit-mae-base/tree/25b184bea5538bf5c4c852c79d221195fdd2778d) | ViTMAEForPreTraining | 447,670,680 |
| vitdet | [hf-tiny-v2/tiny-random-VitDetModel](https://huggingface.co/hf-tiny-v2/tiny-random-VitDetModel/tree/0f5b683bebef5519fc56d0242ae7f3e00edc5369) | VitDetModel | 134,784 |
| vitmatte | [hustvl/vitmatte-small-composition-1k](https://huggingface.co/hustvl/vitmatte-small-composition-1k/tree/6a58ad7646403c1df626fbd746900aec7361ea1d) | VitMatteForImageMatting | 103,294,572 |
| vitpose_backbone | [hf-tiny-v2/tiny-random-VitPoseBackbone](https://huggingface.co/hf-tiny-v2/tiny-random-VitPoseBackbone/tree/ee6ef913081d819114e652c5c34f5e9d9ff57fc8) | VitPoseBackbone | 155,088 |
| vivit | [yehiawp4/ViViT-b-16x2-ShopLifting-Dataset](https://huggingface.co/yehiawp4/ViViT-b-16x2-ShopLifting-Dataset/tree/c04314bb8b6d2e7514c2b1a2f89abb0984d00b8d) | VivitForVideoClassification | 354,615,376 |
| voxtral_encoder | [hf-tiny-v2/tiny-random-VoxtralEncoder](https://huggingface.co/hf-tiny-v2/tiny-random-VoxtralEncoder/tree/b9b0f6ab5532838ad072b5442330a2d7aa417e9f) | VoxtralEncoder | 123,888 |
| voxtral_realtime_encoder | [hf-tiny-v2/tiny-random-VoxtralRealtimeEncoder](https://huggingface.co/hf-tiny-v2/tiny-random-VoxtralRealtimeEncoder/tree/4af85d273a25af0acabfe2801e7d05fb7f2ee69e) | VoxtralRealtimeEncoder | 88,496 |
| voxtral_realtime_text | [hf-tiny-v2/tiny-random-VoxtralRealtimeTextModel](https://huggingface.co/hf-tiny-v2/tiny-random-VoxtralRealtimeTextModel/tree/08a1aa34eab785b37125c50e57c00e68a9b7ca4d) | VoxtralRealtimeTextModel | 72,960 |
| xcodec | [Manel/X-Codec](https://huggingface.co/Manel/X-Codec/tree/12c89aed4c2c6ea9df96ca67e6d3848f8df8069d) | unspecified | 709,991,220 |
| xcodec2 | [hf-tiny-v2/tiny-random-Xcodec2Model](https://huggingface.co/hf-tiny-v2/tiny-random-Xcodec2Model/tree/5c5636af4f3faf681eb70724127ad6b4fc63848c) | Xcodec2Model | 3,873,592 |
| xlm-roberta-xl | [hf-tiny-v2/tiny-random-XLMRobertaXLForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-XLMRobertaXLForCausalLM/tree/92f76cab70ca66ff34443ed9100d9067a37ea150) | XLMRobertaXLForCausalLM | 33,131,640 |
| xlnet | [akreal/tiny-random-xlnet](https://huggingface.co/akreal/tiny-random-xlnet/tree/9c098808149fb254a433941530d58fa5501bcf3d) | unspecified | 611,108 |
| youtu | [hf-tiny-v2/tiny-random-YoutuForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-YoutuForCausalLM/tree/772b3121b720685781588dfbda128a03e6e93dd2) | YoutuForCausalLM | 32,948,088 |
| zamba | [hf-tiny-v2/tiny-random-ZambaForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-ZambaForCausalLM/tree/bb103f722a39cf88558f692bf11d9933df5d13ed) | ZambaForCausalLM | 9,288,112 |
| zamba2 | [hf-tiny-v2/tiny-random-Zamba2ForCausalLM](https://huggingface.co/hf-tiny-v2/tiny-random-Zamba2ForCausalLM/tree/8b1f0ed8cc6a90f855f5ccc0ed8905fe87fd42f1) | Zamba2ForCausalLM | 2,125,704 |
| zaya | [onnx-internal-testing/tiny-random-ZayaForCausalLM](https://huggingface.co/onnx-internal-testing/tiny-random-ZayaForCausalLM/tree/0189238443a2f5ec5e6a318a651696a500064c40) | ZayaForCausalLM | 16,874,908 |
| zoedepth | [hf-tiny-v2/tiny-random-ZoeDepthForDepthEstimation](https://huggingface.co/hf-tiny-v2/tiny-random-ZoeDepthForDepthEstimation/tree/7d0cce9eb45099e7e896e36c7ff00075fa85e6e6) | ZoeDepthForDepthEstimation | 798,708 |

## video-classification

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| timesformer | [Shawon16/timesformer_wlasl_100_20ep_coR_](https://huggingface.co/Shawon16/timesformer_wlasl_100_20ep_coR_/tree/b6c2bde988f7e4d462ac7676dc6098cbf2a271f8) | TimesformerForVideoClassification | 485,373,720 |
| videomae | [MCG-NJU/videomae-base](https://huggingface.co/MCG-NJU/videomae-base/tree/dc740ceda42fce44faed2ea03c6d447db72f6af9) | VideoMAEForPreTraining | 376,873,760 |
| xclip | [microsoft/xclip-base-patch16-zero-shot](https://huggingface.co/microsoft/xclip-base-patch16-zero-shot/tree/6746d6a5202bf24300cd9bf36f457f174483d41b) | XCLIPModel | 779,838,804 |

## visual-question-answering

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| pix2struct | [google/pix2struct-ai2d-base](https://huggingface.co/google/pix2struct-ai2d-base/tree/0d6b2606efe05c77c1d0670647740802a9e68eef) | Pix2StructForConditionalGeneration | 564,606,744 |
| vilt | [Atul8827/vilt_finetuned_200](https://huggingface.co/Atul8827/vilt_finetuned_200/tree/4ac42ef403e97f158483078c71bf2dcaecb00f8c) | ViltForQuestionAnswering | 452,764,944 |

## voice-activity-detection

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| nemotron3_diarization | [nvidia/Nemotron-3-Diarization](https://huggingface.co/nvidia/Nemotron-3-Diarization/tree/f667ed73aee57d40cc39428eb768b4fd87a0a29e) | Nemotron3DiarizationForAudioFrameClassification | 396,954,592 |

## zero-shot-classification

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| deberta-v2 | [MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7](https://huggingface.co/MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7/tree/b5113eb38ab63efdd7f280f8c144ea8b13f978ce) | DebertaV2ForSequenceClassification | 557,652,046 |

## zero-shot-image-classification

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| clip | [patrickjohncyh/fashion-clip](https://huggingface.co/patrickjohncyh/fashion-clip/tree/7e3ba62ce16b379a1ab479346b66f192e76f51b7) | CLIPModel | 605,157,890 |
| metaclip_2 | [vladislavbro/hf-internal-testing-metaclip-2-tiny](https://huggingface.co/vladislavbro/hf-internal-testing-metaclip-2-tiny/tree/75fd9b2fd7ab99ffbc3515b2da0cb3faef3bac95) | MetaClip2Model | 471,043,484 |
| siglip | [google/siglip-base-patch16-224](https://huggingface.co/google/siglip-base-patch16-224/tree/7fd15f0689c79d79e38b1c2e2e2370a7bf2761ed) | SiglipModel | 812,672,320 |
| tipsv2 | [google/tipsv2-b14](https://huggingface.co/google/tipsv2-b14/tree/ed1e4dc6b74bf3935ae099e9d5eb30fa96528454) | TIPSv2Model | 783,830,160 |

## zero-shot-object-detection

| Architecture | Checkpoint | Model classes | Safetensors bytes |
| --- | --- | --- | ---: |
| grounding-dino | [IDEA-Research/grounding-dino-base](https://huggingface.co/IDEA-Research/grounding-dino-base/tree/12bdfa3120f3e7ec7b434d90674b3396eccf88eb) | GroundingDinoForObjectDetection | 933,400,872 |
| mm-grounding-dino | [iSEE-Laboratory/llmdet_base](https://huggingface.co/iSEE-Laboratory/llmdet_base/tree/3537869413e7dca01cfd86d6ab10553b72e4fe29) | MMGroundingDinoForObjectDetection | 936,057,092 |
| omdet-turbo | [omlab/omdet-turbo-swin-tiny-hf](https://huggingface.co/omlab/omdet-turbo-swin-tiny-hf/tree/7fe93cecfb770c4d76cf71163956221249cab566) | OmDetTurboForObjectDetection | 461,822,656 |
| owlv2 | [google/owlv2-base-patch16-ensemble](https://huggingface.co/google/owlv2-base-patch16-ensemble/tree/cfd3195ba4ea9592eec887ded089f4c08eff231d) | Owlv2ForObjectDetection | 619,918,824 |
| owlvit | [google/owlvit-base-patch32](https://huggingface.co/google/owlvit-base-patch32/tree/cbc355fb364588351c5d51c7f74465e8e7ec6f72) | OwlViTForObjectDetection | 612,983,940 |

## Architecture scan inventory

| Architecture | Config class | Result | Candidates checked |
| --- | --- | --- | ---: |
| EvollaModel | EvollaConfig | no-qualifying-checkpoint | 2 |
| afmoe | AfmoeConfig | eligible | 1 |
| aimv2 | Aimv2Config | eligible | 5 |
| aimv2_text_model | Aimv2TextConfig | no-qualifying-checkpoint | 0 |
| aimv2_vision_model | Aimv2VisionConfig | eligible | 9 |
| albert | AlbertConfig | eligible | 1 |
| align | AlignConfig | eligible | 1 |
| align_text_model | AlignTextConfig | no-qualifying-checkpoint | 0 |
| align_vision_model | AlignVisionConfig | no-qualifying-checkpoint | 0 |
| altclip | AltCLIPConfig | eligible | 1 |
| altclip_text_model | AltCLIPTextConfig | no-qualifying-checkpoint | 0 |
| altclip_vision_model | AltCLIPVisionConfig | no-qualifying-checkpoint | 0 |
| apertus | ApertusConfig | eligible | 7 |
| arcee | ArceeConfig | eligible | 1 |
| aria | AriaConfig | eligible | 20 |
| aria_text | AriaTextConfig | eligible | 1 |
| audio-spectrogram-transformer | ASTConfig | eligible | 1 |
| audioflamingo3 | AudioFlamingo3Config | eligible | 3 |
| audioflamingo3_encoder | AudioFlamingo3EncoderConfig | eligible | 1 |
| autoformer | AutoformerConfig | eligible | 1 |
| axk1 | AXK1Config | eligible | 2 |
| axk2 | AXK2Config | eligible | 5 |
| aya_vision | AyaVisionConfig | eligible | 21 |
| bamba | BambaConfig | eligible | 2 |
| bark | BarkConfig | eligible | 2 |
| bart | BartConfig | eligible | 3 |
| beit | BeitConfig | eligible | 1 |
| bert | BertConfig | eligible | 1 |
| bert-generation | BertGenerationConfig | no-qualifying-checkpoint | 2 |
| big_bird | BigBirdConfig | eligible | 1 |
| bigbird_pegasus | BigBirdPegasusConfig | eligible | 1 |
| biogpt | BioGptConfig | eligible | 2 |
| bit | BitConfig | eligible | 1 |
| bitnet | BitNetConfig | eligible | 7 |
| blenderbot | BlenderbotConfig | eligible | 11 |
| blenderbot-small | BlenderbotSmallConfig | eligible | 1 |
| blip | BlipConfig | eligible | 3 |
| blip-2 | Blip2Config | eligible | 13 |
| blip_2_qformer | Blip2QFormerConfig | eligible | 1 |
| blip_2_vision_model | Blip2VisionConfig | no-qualifying-checkpoint | 2 |
| blip_text_model | BlipTextConfig | no-qualifying-checkpoint | 0 |
| blip_vision_model | BlipVisionConfig | no-qualifying-checkpoint | 0 |
| bloom | BloomConfig | eligible | 3 |
| blt | BltConfig | eligible | 19 |
| blt_global_transformer | BltGlobalTransformerConfig | no-qualifying-checkpoint | 0 |
| blt_local_decoder | BltLocalDecoderConfig | no-qualifying-checkpoint | 0 |
| blt_local_encoder | BltLocalEncoderConfig | no-qualifying-checkpoint | 0 |
| blt_patcher | BltPatcherConfig | no-qualifying-checkpoint | 0 |
| bridgetower | BridgeTowerConfig | eligible | 3 |
| bridgetower_text_model | BridgeTowerTextConfig | no-qualifying-checkpoint | 0 |
| bridgetower_vision_model | BridgeTowerVisionConfig | no-qualifying-checkpoint | 0 |
| bros | BrosConfig | eligible | 1 |
| camembert | CamembertConfig | eligible | 1 |
| canary | CanaryConfig | eligible | 13 |
| canary_decoder | CanaryDecoderConfig | no-qualifying-checkpoint | 0 |
| canine | CanineConfig | eligible | 1 |
| chameleon | ChameleonConfig | eligible | 5 |
| chameleon_vqgan | ChameleonVQVAEConfig | eligible | 1 |
| chinese_clip | ChineseCLIPConfig | eligible | 5 |
| chinese_clip_text_model | ChineseCLIPTextConfig | no-qualifying-checkpoint | 0 |
| chinese_clip_vision_model | ChineseCLIPVisionConfig | eligible | 1 |
| chmv2 | CHMv2Config | eligible | 4 |
| clap | ClapConfig | eligible | 1 |
| clap_audio_model | ClapAudioConfig | eligible | 1 |
| clap_text_model | ClapTextConfig | eligible | 1 |
| clip | CLIPConfig | eligible | 4 |
| clip_text_model | CLIPTextConfig | eligible | 1 |
| clip_vision_model | CLIPVisionConfig | eligible | 1 |
| clipseg | CLIPSegConfig | eligible | 1 |
| clipseg_text_model | CLIPSegTextConfig | no-qualifying-checkpoint | 0 |
| clipseg_vision_model | CLIPSegVisionConfig | no-qualifying-checkpoint | 0 |
| clvp | ClvpConfig | eligible | 1 |
| clvp_decoder | ClvpDecoderConfig | no-qualifying-checkpoint | 0 |
| clvp_encoder | ClvpEncoderConfig | no-qualifying-checkpoint | 0 |
| codegen | CodeGenConfig | eligible | 1 |
| cohere | CohereConfig | eligible | 1 |
| cohere2 | Cohere2Config | eligible | 1 |
| cohere2_moe | Cohere2MoeConfig | eligible | 18 |
| cohere2_vision | Cohere2VisionConfig | eligible | 5 |
| cohere_asr | CohereAsrConfig | eligible | 28 |
| cohere_compass | CohereCompassConfig | eligible | 17 |
| cohere_compass_text | CohereCompassTextConfig | eligible | 1 |
| cohere_compass_vision | CohereCompassVisionConfig | eligible | 1 |
| colmodernvbert | ColModernVBertConfig | eligible | 1 |
| colpali | ColPaliConfig | eligible | 73 |
| colqwen2 | ColQwen2Config | eligible | 10 |
| conditional_detr | ConditionalDetrConfig | eligible | 1 |
| convbert | ConvBertConfig | eligible | 1 |
| convnext | ConvNextConfig | eligible | 1 |
| convnextv2 | ConvNextV2Config | eligible | 1 |
| cosmos3_edge | Cosmos3EdgeConfig | eligible | 7 |
| cosmos3_edge_text | Cosmos3EdgeTextConfig | eligible | 1 |
| cosmos3_edge_vision | Cosmos3EdgeVisionConfig | eligible | 1 |
| cosmos3_omni | Cosmos3OmniConfig | eligible | 12 |
| cpmant | CpmAntConfig | eligible | 1 |
| csm | CsmConfig | eligible | 12 |
| csm_depth_decoder_model | CsmDepthDecoderConfig | no-qualifying-checkpoint | 0 |
| ctrl | CTRLConfig | eligible | 5 |
| cvt | CvtConfig | eligible | 1 |
| cwm | CwmConfig | eligible | 3 |
| d_fine | DFineConfig | eligible | 1 |
| dab-detr | DabDetrConfig | eligible | 1 |
| dac | DacConfig | eligible | 1 |
| data2vec-audio | Data2VecAudioConfig | eligible | 1 |
| data2vec-text | Data2VecTextConfig | eligible | 1 |
| data2vec-vision | Data2VecVisionConfig | eligible | 2 |
| dbrx | DbrxConfig | eligible | 1 |
| deberta | DebertaConfig | eligible | 4 |
| deberta-v2 | DebertaV2Config | eligible | 2 |
| decision_transformer | DecisionTransformerConfig | eligible | 1 |
| deepseek_ocr2 | DeepseekOcr2Config | eligible | 1 |
| deepseek_ocr2_encoder | DeepseekOcr2VisionEncoderConfig | no-qualifying-checkpoint | 0 |
| deepseek_ocr2_sam_vision_model | DeepseekOcr2SamVisionConfig | no-qualifying-checkpoint | 0 |
| deepseek_ocr2_text | DeepseekOcr2TextConfig | no-qualifying-checkpoint | 0 |
| deepseek_ocr2_vision | DeepseekOcr2VisionConfig | no-qualifying-checkpoint | 0 |
| deepseek_v2 | DeepseekV2Config | eligible | 8 |
| deepseek_v3 | DeepseekV3Config | eligible | 9 |
| deepseek_v32 | DeepseekV32Config | eligible | 10 |
| deepseek_v4 | DeepseekV4Config | eligible | 52 |
| deepseek_vl | DeepseekVLConfig | eligible | 3 |
| deepseek_vl_hybrid | DeepseekVLHybridConfig | eligible | 2 |
| deformable_detr | DeformableDetrConfig | eligible | 1 |
| deimv2 | Deimv2Config | eligible | 1 |
| deit | DeiTConfig | eligible | 1 |
| depth_anything | DepthAnythingConfig | eligible | 1 |
| depth_pro | DepthProConfig | eligible | 4 |
| detr | DetrConfig | eligible | 1 |
| dia | DiaConfig | eligible | 15 |
| dia_decoder | DiaDecoderConfig | no-qualifying-checkpoint | 0 |
| dia_encoder | DiaEncoderConfig | no-qualifying-checkpoint | 0 |
| diffllama | DiffLlamaConfig | eligible | 4 |
| diffusion_gemma | DiffusionGemmaConfig | eligible | 5 |
| diffusion_gemma_text | DiffusionGemmaTextConfig | no-qualifying-checkpoint | 0 |
| dinat | DinatConfig | eligible | 1 |
| dinov2 | Dinov2Config | eligible | 1 |
| dinov2_with_registers | Dinov2WithRegistersConfig | eligible | 1 |
| dinov3_convnext | DINOv3ConvNextConfig | eligible | 5 |
| dinov3_vit | DINOv3ViTConfig | eligible | 11 |
| distilbert | DistilBertConfig | eligible | 1 |
| doge | DogeConfig | eligible | 1 |
| donut-swin | DonutSwinConfig | eligible | 1 |
| dots1 | Dots1Config | eligible | 5 |
| dpr | DPRConfig | eligible | 1 |
| dpt | DPTConfig | eligible | 2 |
| edgetam | EdgeTamConfig | eligible | 1 |
| edgetam_video | EdgeTamVideoConfig | eligible | 1 |
| edgetam_vision_model | EdgeTamVisionConfig | eligible | 1 |
| efficientloftr | EfficientLoFTRConfig | eligible | 1 |
| efficientnet | EfficientNetConfig | eligible | 1 |
| electra | ElectraConfig | eligible | 1 |
| emu3 | Emu3Config | eligible | 6 |
| emu3_text_model | Emu3TextConfig | eligible | 1 |
| emu3_vqgan | Emu3VQVAEConfig | no-qualifying-checkpoint | 0 |
| encodec | EncodecConfig | eligible | 1 |
| encoder-decoder | EncoderDecoderConfig | eligible | 1 |
| eomt | EomtConfig | eligible | 6 |
| eomt_dinov3 | EomtDinov3Config | eligible | 1 |
| ernie | ErnieConfig | eligible | 1 |
| ernie4_5 | Ernie4_5Config | eligible | 1 |
| ernie4_5_moe | Ernie4_5_MoeConfig | eligible | 7 |
| ernie4_5_vl_moe | Ernie4_5_VLMoeConfig | eligible | 1 |
| ernie4_5_vl_moe_text | Ernie4_5_VLMoeTextConfig | no-qualifying-checkpoint | 0 |
| ernie4_5_vl_moe_vision | Ernie4_5_VLMoeVisionConfig | no-qualifying-checkpoint | 0 |
| esm | EsmConfig | eligible | 2 |
| esmc | EsmcConfig | eligible | 29 |
| esmfold2 | EsmFold2Config | eligible | 2 |
| eurobert | EuroBertConfig | eligible | 1 |
| evolla | EvollaConfig | no-qualifying-checkpoint | 0 |
| exaone4 | Exaone4Config | eligible | 2 |
| exaone4_5 | Exaone4_5_Config | eligible | 5 |
| exaone4_5_vision | Exaone4_5_VisionConfig | eligible | 1 |
| exaone_moe | ExaoneMoeConfig | eligible | 8 |
| falcon | FalconConfig | eligible | 3 |
| falcon_h1 | FalconH1Config | eligible | 11 |
| falcon_mamba | FalconMambaConfig | eligible | 1 |
| fast_vlm | FastVlmConfig | eligible | 4 |
| fastspeech2_conformer | FastSpeech2ConformerConfig | eligible | 1 |
| fastspeech2_conformer_hifigan | FastSpeech2ConformerHifiGanConfig | no-qualifying-checkpoint | 0 |
| fastspeech2_conformer_with_hifigan | FastSpeech2ConformerWithHifiGanConfig | eligible | 1 |
| flaubert | FlaubertConfig | eligible | 1 |
| flava | FlavaConfig | eligible | 1 |
| flava_image_model | FlavaImageConfig | no-qualifying-checkpoint | 0 |
| flava_multimodal_model | FlavaMultimodalConfig | no-qualifying-checkpoint | 0 |
| flava_text_model | FlavaTextConfig | no-qualifying-checkpoint | 0 |
| flex_olmo | FlexOlmoConfig | eligible | 18 |
| florence2 | Florence2Config | eligible | 1 |
| florence_vision | Florence2VisionConfig | no-qualifying-checkpoint | 0 |
| fnet | FNetConfig | eligible | 1 |
| focalnet | FocalNetConfig | eligible | 1 |
| fsmt | FSMTConfig | eligible | 5 |
| fun_asr_nano | FunAsrNanoConfig | eligible | 5 |
| fun_asr_nano_encoder | FunAsrNanoEncoderConfig | eligible | 1 |
| funnel | FunnelConfig | eligible | 1 |
| fuyu | FuyuConfig | eligible | 19 |
| gemma | GemmaConfig | eligible | 9 |
| gemma2 | Gemma2Config | eligible | 3 |
| gemma3 | Gemma3Config | eligible | 14 |
| gemma3_text | Gemma3TextConfig | eligible | 4 |
| gemma3n | Gemma3nConfig | eligible | 3 |
| gemma3n_audio | Gemma3nAudioConfig | eligible | 2 |
| gemma3n_text | Gemma3nTextConfig | eligible | 1 |
| gemma3n_vision | Gemma3nVisionConfig | no-qualifying-checkpoint | 0 |
| gemma4 | Gemma4Config | eligible | 48 |
| gemma4_assistant | Gemma4AssistantConfig | eligible | 1 |
| gemma4_audio | Gemma4AudioConfig | eligible | 1 |
| gemma4_text | Gemma4TextConfig | eligible | 1 |
| gemma4_unified | Gemma4UnifiedConfig | eligible | 12 |
| gemma4_unified_assistant | Gemma4UnifiedAssistantConfig | eligible | 1 |
| gemma4_unified_audio | Gemma4UnifiedAudioConfig | no-qualifying-checkpoint | 0 |
| gemma4_unified_text | Gemma4UnifiedTextConfig | eligible | 5 |
| gemma4_unified_vision | Gemma4UnifiedVisionConfig | no-qualifying-checkpoint | 0 |
| gemma4_vision | Gemma4VisionConfig | eligible | 3 |
| git | GitConfig | eligible | 1 |
| git_vision_model | GitVisionConfig | no-qualifying-checkpoint | 0 |
| glm | GlmConfig | eligible | 10 |
| glm4 | Glm4Config | eligible | 1 |
| glm46v | Glm46VConfig | eligible | 1 |
| glm4_moe | Glm4MoeConfig | eligible | 3 |
| glm4_moe_lite | Glm4MoeLiteConfig | eligible | 12 |
| glm4v | Glm4vConfig | eligible | 7 |
| glm4v_moe | Glm4vMoeConfig | eligible | 5 |
| glm4v_moe_text | Glm4vMoeTextConfig | eligible | 1 |
| glm4v_moe_vision | Glm4vMoeVisionConfig | eligible | 1 |
| glm4v_text | Glm4vTextConfig | eligible | 1 |
| glm4v_vision | Glm4vVisionConfig | eligible | 1 |
| glm5_next | Glm5NextConfig | eligible | 38 |
| glm5_next_text | Glm5NextTextConfig | eligible | 1 |
| glm5_next_vision | Glm5NextVisionConfig | eligible | 2 |
| glm_image | GlmImageConfig | eligible | 1 |
| glm_image_text | GlmImageTextConfig | eligible | 1 |
| glm_image_vision | GlmImageVisionConfig | eligible | 1 |
| glm_image_vqmodel | GlmImageVQVAEConfig | eligible | 1 |
| glm_moe_dsa | GlmMoeDsaConfig | eligible | 23 |
| glm_ocr | GlmOcrConfig | eligible | 6 |
| glm_ocr_text | GlmOcrTextConfig | eligible | 1 |
| glm_ocr_vision | GlmOcrVisionConfig | eligible | 1 |
| glmasr | GlmAsrConfig | eligible | 9 |
| glmasr_encoder | GlmAsrEncoderConfig | eligible | 1 |
| glmga | GlmgaConfig | no-qualifying-checkpoint | 0 |
| glpn | GLPNConfig | eligible | 1 |
| got_ocr2 | GotOcr2Config | eligible | 2 |
| gpt-sw3 | GPT2Config | no-qualifying-checkpoint | 3 |
| gpt2 | GPT2Config | eligible | 1 |
| gpt_bigcode | GPTBigCodeConfig | eligible | 1 |
| gpt_neo | GPTNeoConfig | eligible | 1 |
| gpt_neox | GPTNeoXConfig | eligible | 1 |
| gpt_neox_japanese | GPTNeoXJapaneseConfig | eligible | 2 |
| gpt_oss | GptOssConfig | eligible | 3 |
| gptj | GPTJConfig | eligible | 1 |
| granite | GraniteConfig | eligible | 19 |
| granite4_vision | Granite4VisionConfig | eligible | 3 |
| granite4_vision_text | Granite4VisionTextConfig | no-qualifying-checkpoint | 0 |
| granite_speech | GraniteSpeechConfig | eligible | 6 |
| granite_speech5_ctc | GraniteSpeech5CTCConfig | eligible | 1 |
| granite_speech5_encoder | GraniteSpeech5EncoderConfig | eligible | 1 |
| granite_speech_encoder | GraniteSpeechEncoderConfig | no-qualifying-checkpoint | 0 |
| granite_speech_plus | GraniteSpeechPlusConfig | eligible | 4 |
| granite_speech_plus_encoder | GraniteSpeechPlusEncoderConfig | no-qualifying-checkpoint | 0 |
| granite_swa | GraniteSWAConfig | eligible | 2 |
| granitemoe | GraniteMoeConfig | eligible | 3 |
| granitemoe_swa | GraniteMoeSWAConfig | eligible | 2 |
| granitemoehybrid | GraniteMoeHybridConfig | eligible | 1 |
| granitemoeshared | GraniteMoeSharedConfig | eligible | 2 |
| grounding-dino | GroundingDinoConfig | eligible | 1 |
| groupvit | GroupViTConfig | eligible | 1 |
| groupvit_text_model | GroupViTTextConfig | no-qualifying-checkpoint | 0 |
| groupvit_vision_model | GroupViTVisionConfig | no-qualifying-checkpoint | 0 |
| gte | GteConfig | eligible | 4 |
| helium | HeliumConfig | eligible | 3 |
| hgnet_v2 | HGNetV2Config | eligible | 1 |
| hiera | HieraConfig | eligible | 1 |
| higgs_audio_v2 | HiggsAudioV2Config | eligible | 5 |
| higgs_audio_v2_tokenizer | HiggsAudioV2TokenizerConfig | eligible | 1 |
| hrm_text | HrmTextConfig | eligible | 4 |
| hubert | HubertConfig | eligible | 2 |
| hunyuan_v1_dense | HunYuanDenseV1Config | eligible | 1 |
| hunyuan_v1_moe | HunYuanMoEV1Config | eligible | 2 |
| hunyuan_vl | HunYuanVLConfig | eligible | 6 |
| hunyuan_vl_text | HunYuanVLTextConfig | eligible | 1 |
| hunyuan_vl_vision | HunYuanVLVisionConfig | eligible | 1 |
| hy_v3 | HYV3Config | eligible | 7 |
| hy_v4 | HYV4Config | eligible | 13 |
| hyperclovax | HyperCLOVAXConfig | eligible | 35 |
| hyperclovax_vision_v2 | HyperCLOVAXVisionV2Config | eligible | 2 |
| ibert | IBertConfig | eligible | 1 |
| idefics | IdeficsConfig | eligible | 6 |
| idefics2 | Idefics2Config | eligible | 2 |
| idefics2_perceiver | Idefics2PerceiverConfig | no-qualifying-checkpoint | 0 |
| idefics2_vision | Idefics2VisionConfig | no-qualifying-checkpoint | 0 |
| idefics3 | Idefics3Config | eligible | 1 |
| idefics3_vision | Idefics3VisionConfig | eligible | 1 |
| idefics_perciever | IdeficsPerceiverConfig | no-qualifying-checkpoint | 0 |
| idefics_vision | IdeficsVisionConfig | no-qualifying-checkpoint | 0 |
| ijepa | IJepaConfig | eligible | 7 |
| imagegpt | ImageGPTConfig | eligible | 1 |
| informer | InformerConfig | eligible | 1 |
| inkling_audio | InklingAudioConfig | no-qualifying-checkpoint | 0 |
| inkling_mm_model | InklingConfig | eligible | 36 |
| inkling_text | InklingTextConfig | eligible | 1 |
| inkling_vision | InklingVisionConfig | no-qualifying-checkpoint | 0 |
| instructblip | InstructBlipConfig | eligible | 5 |
| instructblip_qformer | InstructBlipQFormerConfig | no-qualifying-checkpoint | 0 |
| instructblip_vision_model | InstructBlipVisionConfig | no-qualifying-checkpoint | 0 |
| instructblipvideo | InstructBlipVideoConfig | eligible | 1 |
| instructblipvideo_qformer | InstructBlipVideoQFormerConfig | no-qualifying-checkpoint | 0 |
| instructblipvideo_vision_model | InstructBlipVideoVisionConfig | no-qualifying-checkpoint | 0 |
| internvl | InternVLConfig | eligible | 14 |
| internvl_vision | InternVLVisionConfig | eligible | 1 |
| jais2 | Jais2Config | eligible | 3 |
| jamba | JambaConfig | eligible | 1 |
| janus | JanusConfig | eligible | 15 |
| janus_vision_model | JanusVisionConfig | no-qualifying-checkpoint | 0 |
| janus_vqgan | JanusVQVAEConfig | no-qualifying-checkpoint | 0 |
| jetmoe | JetMoeConfig | eligible | 20 |
| jina_embeddings_v3 | JinaEmbeddingsV3Config | eligible | 2 |
| kimi_k25 | Kimi_K25Config | eligible | 10 |
| kimi_k25_vision | Kimi_K25VisionConfig | eligible | 1 |
| kimi_linear | KimiLinearConfig | eligible | 1 |
| kosmos-2 | Kosmos2Config | eligible | 8 |
| kosmos-2.5 | Kosmos2_5Config | eligible | 5 |
| kosmos_2_5_text_model | Kosmos2_5TextConfig | eligible | 1 |
| kosmos_2_5_vision_model | Kosmos2_5VisionConfig | eligible | 1 |
| kosmos_2_text_model | Kosmos2TextConfig | no-qualifying-checkpoint | 0 |
| kosmos_2_vision_model | Kosmos2VisionConfig | no-qualifying-checkpoint | 0 |
| kyutai_speech_to_text | KyutaiSpeechToTextConfig | eligible | 3 |
| laguna | LagunaConfig | eligible | 21 |
| lasr_ctc | LasrCTCConfig | eligible | 2 |
| lasr_encoder | LasrEncoderConfig | eligible | 1 |
| layoutlm | LayoutLMConfig | eligible | 1 |
| layoutlmv2 | LayoutLMv2Config | eligible | 1 |
| layoutlmv3 | LayoutLMv3Config | eligible | 1 |
| layoutxlm | LayoutXLMConfig | no-qualifying-checkpoint | 0 |
| led | LEDConfig | eligible | 3 |
| levit | LevitConfig | eligible | 1 |
| lfm2 | Lfm2Config | eligible | 8 |
| lfm2_moe | Lfm2MoeConfig | eligible | 7 |
| lfm2_vl | Lfm2VlConfig | eligible | 2 |
| lightglue | LightGlueConfig | eligible | 1 |
| lighton_ocr | LightOnOcrConfig | eligible | 10 |
| lilt | LiltConfig | eligible | 1 |
| llama | LlamaConfig | eligible | 5 |
| llama4 | Llama4Config | eligible | 5 |
| llama4_text | Llama4TextConfig | eligible | 1 |
| llama4_vision_model | Llama4VisionConfig | no-qualifying-checkpoint | 0 |
| llava | LlavaConfig | eligible | 2 |
| llava_next | LlavaNextConfig | eligible | 3 |
| llava_next_video | LlavaNextVideoConfig | eligible | 2 |
| llava_onevision | LlavaOnevisionConfig | eligible | 33 |
| longcat_flash | LongcatFlashConfig | eligible | 1 |
| longformer | LongformerConfig | eligible | 1 |
| longt5 | LongT5Config | eligible | 1 |
| luke | LukeConfig | eligible | 1 |
| lw_detr | LwDetrConfig | eligible | 1 |
| lw_detr_vit | LwDetrViTConfig | eligible | 1 |
| lxmert | LxmertConfig | eligible | 1 |
| m2m_100 | M2M100Config | eligible | 19 |
| mamba | MambaConfig | eligible | 1 |
| mamba2 | Mamba2Config | eligible | 1 |
| marian | MarianConfig | eligible | 1 |
| markuplm | MarkupLMConfig | eligible | 1 |
| mask2former | Mask2FormerConfig | eligible | 1 |
| maskformer | MaskFormerConfig | eligible | 1 |
| maskformer-swin | MaskFormerSwinConfig | no-qualifying-checkpoint | 0 |
| mbart | MBartConfig | eligible | 7 |
| megatron-bert | MegatronBertConfig | eligible | 4 |
| mellum | MellumConfig | eligible | 52 |
| metaclip_2 | MetaClip2Config | eligible | 10 |
| metaclip_2_text_model | MetaClip2TextConfig | no-qualifying-checkpoint | 0 |
| metaclip_2_vision_model | MetaClip2VisionConfig | no-qualifying-checkpoint | 0 |
| mgp-str | MgpstrConfig | eligible | 1 |
| mimi | MimiConfig | eligible | 1 |
| mimo_v2_flash | MiMoV2FlashConfig | eligible | 16 |
| minicpm3 | MiniCPM3Config | eligible | 1 |
| minicpmv4_6 | MiniCPMV4_6Config | eligible | 19 |
| minicpmv4_6_vision | MiniCPMV4_6VisionConfig | no-qualifying-checkpoint | 0 |
| minicpmv4_7 | MiniCPMV4_7Config | eligible | 1 |
| minicpmv4_7_vision | MiniCPMV4_7VisionConfig | eligible | 1 |
| minimax | MiniMaxConfig | eligible | 86 |
| minimax_m2 | MiniMaxM2Config | eligible | 13 |
| minimax_m3_vl | MiniMaxM3VLConfig | eligible | 11 |
| minimax_m3_vl_text | MiniMaxM3VLTextConfig | eligible | 1 |
| minimax_m3_vl_vision | MiniMaxM3VLVisionConfig | no-qualifying-checkpoint | 1 |
| ministral | MinistralConfig | search-limit | 100 |
| ministral3 | Ministral3Config | eligible | 12 |
| mistral | MistralConfig | eligible | 15 |
| mistral3 | Mistral3Config | eligible | 13 |
| mistral4 | Mistral4Config | eligible | 1 |
| mixtral | MixtralConfig | eligible | 2 |
| mlcd | MLCDVisionConfig | no-qualifying-checkpoint | 4 |
| mlcd_vision_model | MLCDVisionConfig | eligible | 1 |
| mllama | MllamaConfig | eligible | 5 |
| mllama_text_model | MllamaTextConfig | eligible | 1 |
| mllama_vision_model | MllamaVisionConfig | eligible | 1 |
| mm-grounding-dino | MMGroundingDinoConfig | eligible | 1 |
| mobilebert | MobileBertConfig | eligible | 1 |
| mobilenet_v1 | MobileNetV1Config | eligible | 1 |
| mobilenet_v2 | MobileNetV2Config | eligible | 1 |
| mobilevit | MobileViTConfig | eligible | 1 |
| mobilevitv2 | MobileViTV2Config | eligible | 1 |
| modernbert | ModernBertConfig | eligible | 1 |
| modernbert-decoder | ModernBertDecoderConfig | eligible | 1 |
| modernvbert | ModernVBertConfig | eligible | 1 |
| moonshine | MoonshineConfig | eligible | 1 |
| moonshine_streaming | MoonshineStreamingConfig | eligible | 1 |
| moonshine_streaming_encoder | MoonshineStreamingEncoderConfig | no-qualifying-checkpoint | 0 |
| moshi | MoshiConfig | eligible | 34 |
| moshi_depth | MoshiDepthConfig | no-qualifying-checkpoint | 0 |
| mpnet | MPNetConfig | eligible | 1 |
| mpt | MptConfig | eligible | 2 |
| mra | MraConfig | eligible | 1 |
| mt5 | MT5Config | eligible | 1 |
| muse_glimmer | MuseGlimmerConfig | eligible | 3 |
| muse_glimmer_assistant | MuseGlimmerAssistantConfig | eligible | 4 |
| muse_glimmer_text | MuseGlimmerTextConfig | eligible | 2 |
| muse_glimmer_vision | MuseGlimmerVisionConfig | eligible | 2 |
| musicflamingo | MusicFlamingoConfig | eligible | 14 |
| musicgen | MusicgenConfig | eligible | 9 |
| musicgen_decoder | MusicgenDecoderConfig | eligible | 1 |
| musicgen_melody | MusicgenMelodyConfig | eligible | 7 |
| musicgen_melody_decoder | MusicgenMelodyDecoderConfig | eligible | 2 |
| mvp | MvpConfig | eligible | 24 |
| nanochat | NanoChatConfig | search-limit | 100 |
| nemotron | NemotronConfig | eligible | 7 |
| nemotron3_5_asr | Nemotron3_5AsrConfig | eligible | 14 |
| nemotron3_diarization | Nemotron3DiarizationConfig | eligible | 1 |
| nemotron3_diarization_audio | Nemotron3DiarizationAudioConfig | eligible | 1 |
| nemotron_asr_streaming | NemotronAsrStreamingConfig | eligible | 3 |
| nemotron_asr_streaming_encoder | NemotronAsrStreamingEncoderConfig | eligible | 1 |
| nemotron_h | NemotronHConfig | eligible | 14 |
| nemotron_h_omni | NemotronH_Omni_Reasoning_V3_Config | eligible | 1 |
| neomme | NeoMMEConfig | eligible | 1 |
| neucodec | NeuCodecConfig | eligible | 7 |
| nllb-moe | NllbMoeConfig | eligible | 2 |
| nomic_bert | NomicBertConfig | eligible | 1 |
| nougat | NougatConfig | no-qualifying-checkpoint | 8 |
| nystromformer | NystromformerConfig | eligible | 1 |
| olmo | OlmoConfig | eligible | 2 |
| olmo2 | Olmo2Config | eligible | 4 |
| olmo3 | Olmo3Config | eligible | 4 |
| olmo_hybrid | OlmoHybridConfig | eligible | 5 |
| olmoe | OlmoeConfig | eligible | 16 |
| omdet-turbo | OmDetTurboConfig | eligible | 1 |
| oneformer | OneFormerConfig | eligible | 1 |
| openai-gpt | OpenAIGPTConfig | eligible | 1 |
| openai_privacy_filter | OpenAIPrivacyFilterConfig | eligible | 6 |
| opt | OPTConfig | eligible | 1 |
| ovis2 | Ovis2Config | eligible | 3 |
| owlv2 | Owlv2Config | eligible | 1 |
| owlv2_text_model | Owlv2TextConfig | no-qualifying-checkpoint | 0 |
| owlv2_vision_model | Owlv2VisionConfig | no-qualifying-checkpoint | 0 |
| owlvit | OwlViTConfig | eligible | 1 |
| owlvit_text_model | OwlViTTextConfig | no-qualifying-checkpoint | 0 |
| owlvit_vision_model | OwlViTVisionConfig | no-qualifying-checkpoint | 0 |
| paddleocr_vl | PaddleOCRVLConfig | eligible | 8 |
| paddleocr_vl_text | PaddleOCRTextConfig | no-qualifying-checkpoint | 0 |
| paddleocr_vl_vision | PaddleOCRVisionConfig | no-qualifying-checkpoint | 0 |
| paligemma | PaliGemmaConfig | eligible | 6 |
| parakeet_ctc | ParakeetCTCConfig | eligible | 3 |
| parakeet_encoder | ParakeetEncoderConfig | eligible | 3 |
| parakeet_rnnt | ParakeetRNNTConfig | eligible | 5 |
| parakeet_tdt | ParakeetTDTConfig | eligible | 3 |
| patchtsmixer | PatchTSMixerConfig | eligible | 1 |
| patchtst | PatchTSTConfig | eligible | 1 |
| pe_audio | PeAudioConfig | eligible | 4 |
| pe_audio_encoder | PeAudioEncoderConfig | eligible | 1 |
| pe_audio_video | PeAudioVideoConfig | no-qualifying-checkpoint | 9 |
| pe_audio_video_encoder | PeAudioVideoEncoderConfig | eligible | 1 |
| pe_video | PeVideoConfig | eligible | 1 |
| pe_video_encoder | PeVideoEncoderConfig | eligible | 1 |
| pegasus | PegasusConfig | eligible | 52 |
| pegasus_x | PegasusXConfig | eligible | 7 |
| perceiver | PerceiverConfig | eligible | 1 |
| perception_lm | PerceptionLMConfig | eligible | 8 |
| persimmon | PersimmonConfig | eligible | 2 |
| phi | PhiConfig | eligible | 7 |
| phi3 | Phi3Config | eligible | 6 |
| phi4_multimodal | Phi4MultimodalConfig | eligible | 1 |
| phi4_multimodal_audio | Phi4MultimodalAudioConfig | no-qualifying-checkpoint | 0 |
| phi4_multimodal_vision | Phi4MultimodalVisionConfig | no-qualifying-checkpoint | 0 |
| phimoe | PhimoeConfig | eligible | 2 |
| pi0 | PI0Config | search-limit | 100 |
| pix2struct | Pix2StructConfig | eligible | 5 |
| pix2struct_text_model | Pix2StructTextConfig | no-qualifying-checkpoint | 0 |
| pix2struct_vision_model | Pix2StructVisionConfig | no-qualifying-checkpoint | 0 |
| pixio | PixioConfig | eligible | 4 |
| pixtral | PixtralVisionConfig | eligible | 37 |
| plbart | PLBartConfig | eligible | 1 |
| poolformer | PoolFormerConfig | eligible | 1 |
| pop2piano | Pop2PianoConfig | eligible | 1 |
| pp_chart2table | PPChart2TableConfig | no-qualifying-checkpoint | 1 |
| pp_doclayout_v2 | PPDocLayoutV2Config | eligible | 1 |
| pp_doclayout_v3 | PPDocLayoutV3Config | eligible | 1 |
| pp_formulanet | PPFormulaNetConfig | eligible | 1 |
| pp_lcnet | PPLCNetConfig | eligible | 1 |
| pp_lcnet_v3 | PPLCNetV3Config | eligible | 1 |
| pp_lcnet_v4 | PPLCNetV4Config | eligible | 1 |
| pp_ocrv5_mobile_det | PPOCRV5MobileDetConfig | eligible | 1 |
| pp_ocrv5_mobile_rec | PPOCRV5MobileRecConfig | eligible | 1 |
| pp_ocrv5_server_det | PPOCRV5ServerDetConfig | eligible | 1 |
| pp_ocrv5_server_rec | PPOCRV5ServerRecConfig | eligible | 1 |
| pp_ocrv6_medium_det | PPOCRV6MediumDetConfig | eligible | 1 |
| pp_ocrv6_small_det | PPOCRV6SmallDetConfig | eligible | 1 |
| pp_ocrv6_small_rec | PPOCRV6SmallRecConfig | eligible | 1 |
| pp_ocrv6_tiny_rec | PPOCRV6TinyRecConfig | eligible | 1 |
| prompt_depth_anything | PromptDepthAnythingConfig | eligible | 1 |
| prophetnet | ProphetNetConfig | eligible | 5 |
| pvt | PvtConfig | eligible | 1 |
| pvt_v2 | PvtV2Config | eligible | 1 |
| qianfan_ocr | QianfanOCRConfig | eligible | 4 |
| qianfan_ocr_vision | QianfanOCRVisionConfig | eligible | 1 |
| qwen2 | Qwen2Config | eligible | 2 |
| qwen2_5_omni | Qwen2_5OmniConfig | eligible | 7 |
| qwen2_5_omni_audio_encoder | Qwen2_5OmniAudioEncoderConfig | no-qualifying-checkpoint | 1 |
| qwen2_5_omni_bigvgan | Qwen2_5OmniBigVGANConfig | eligible | 1 |
| qwen2_5_omni_dit | Qwen2_5OmniDiTConfig | no-qualifying-checkpoint | 0 |
| qwen2_5_omni_talker | Qwen2_5OmniTalkerConfig | no-qualifying-checkpoint | 0 |
| qwen2_5_omni_text | Qwen2_5OmniTextConfig | no-qualifying-checkpoint | 2 |
| qwen2_5_omni_thinker | Qwen2_5OmniThinkerConfig | eligible | 45 |
| qwen2_5_omni_token2wav | Qwen2_5OmniToken2WavConfig | no-qualifying-checkpoint | 0 |
| qwen2_5_omni_vision_encoder | Qwen2_5OmniVisionEncoderConfig | no-qualifying-checkpoint | 0 |
| qwen2_5_vl | Qwen2_5_VLConfig | eligible | 9 |
| qwen2_5_vl_text | Qwen2_5_VLTextConfig | eligible | 4 |
| qwen2_5_vl_vision | Qwen2_5_VLVisionConfig | eligible | 1 |
| qwen2_audio | Qwen2AudioConfig | eligible | 3 |
| qwen2_audio_encoder | Qwen2AudioEncoderConfig | eligible | 6 |
| qwen2_moe | Qwen2MoeConfig | eligible | 2 |
| qwen2_vl | Qwen2VLConfig | eligible | 6 |
| qwen2_vl_text | Qwen2VLTextConfig | eligible | 1 |
| qwen2_vl_vision | Qwen2VLVisionConfig | no-qualifying-checkpoint | 0 |
| qwen3 | Qwen3Config | eligible | 17 |
| qwen3_5 | Qwen3_5Config | eligible | 80 |
| qwen3_5_moe | Qwen3_5MoeConfig | eligible | 31 |
| qwen3_5_moe_text | Qwen3_5MoeTextConfig | eligible | 10 |
| qwen3_5_moe_vision | Qwen3_5MoeVisionConfig | eligible | 1 |
| qwen3_5_text | Qwen3_5TextConfig | eligible | 53 |
| qwen3_5_vision | Qwen3_5VisionConfig | eligible | 1 |
| qwen3_asr | Qwen3ASRConfig | eligible | 15 |
| qwen3_asr_encoder | Qwen3ASREncoderConfig | eligible | 1 |
| qwen3_moe | Qwen3MoeConfig | eligible | 12 |
| qwen3_next | Qwen3NextConfig | eligible | 12 |
| qwen3_omni_moe | Qwen3OmniMoeConfig | eligible | 3 |
| qwen3_omni_moe_audio_encoder | Qwen3OmniMoeAudioEncoderConfig | no-qualifying-checkpoint | 5 |
| qwen3_omni_moe_talker_code_predictor | Qwen3OmniMoeTalkerCodePredictorConfig | no-qualifying-checkpoint | 0 |
| qwen3_omni_moe_talker_text | Qwen3OmniMoeTalkerTextConfig | no-qualifying-checkpoint | 0 |
| qwen3_omni_moe_text | Qwen3OmniMoeTextConfig | no-qualifying-checkpoint | 0 |
| qwen3_omni_moe_thinker | Qwen3OmniMoeThinkerConfig | eligible | 1 |
| qwen3_omni_moe_vision_encoder | Qwen3OmniMoeVisionEncoderConfig | no-qualifying-checkpoint | 0 |
| qwen3_vl | Qwen3VLConfig | eligible | 37 |
| qwen3_vl_moe | Qwen3VLMoeConfig | eligible | 15 |
| qwen3_vl_moe_text | Qwen3VLMoeTextConfig | eligible | 1 |
| qwen3_vl_moe_vision | Qwen3VLMoeVisionConfig | eligible | 1 |
| qwen3_vl_text | Qwen3VLTextConfig | eligible | 4 |
| qwen3_vl_vision | Qwen3VLVisionConfig | eligible | 2 |
| qwen4_exp | Qwen4ExpConfig | eligible | 98 |
| qwen4_exp_text | Qwen4ExpTextConfig | eligible | 16 |
| qwen4_exp_vision | Qwen4ExpVisionConfig | no-qualifying-checkpoint | 0 |
| radio | RadioConfig | eligible | 15 |
| rag | RagConfig | search-limit | 100 |
| recurrent_gemma | RecurrentGemmaConfig | eligible | 5 |
| reformer | ReformerConfig | eligible | 1 |
| regnet | RegNetConfig | eligible | 1 |
| rembert | RemBertConfig | eligible | 73 |
| resnet | ResNetConfig | eligible | 1 |
| rf_detr | RfDetrConfig | eligible | 1 |
| rf_detr_dinov2 | RfDetrDinov2Config | eligible | 1 |
| roberta | RobertaConfig | eligible | 1 |
| roberta-prelayernorm | RobertaPreLayerNormConfig | eligible | 1 |
| roc_bert | RoCBertConfig | eligible | 1 |
| roformer | RoFormerConfig | eligible | 1 |
| rt_detr | RTDetrConfig | eligible | 1 |
| rt_detr_resnet | RTDetrResNetConfig | eligible | 1 |
| rt_detr_v2 | RTDetrV2Config | eligible | 1 |
| rwkv | RwkvConfig | eligible | 10 |
| sam | SamConfig | eligible | 2 |
| sam2 | Sam2Config | eligible | 1 |
| sam2_hiera_det_model | Sam2HieraDetConfig | eligible | 1 |
| sam2_video | Sam2VideoConfig | eligible | 1 |
| sam2_vision_model | Sam2VisionConfig | eligible | 1 |
| sam3 | Sam3Config | eligible | 6 |
| sam3_detr_decoder | Sam3DETRDecoderConfig | no-qualifying-checkpoint | 0 |
| sam3_detr_encoder | Sam3DETREncoderConfig | no-qualifying-checkpoint | 0 |
| sam3_geometry_encoder | Sam3GeometryEncoderConfig | no-qualifying-checkpoint | 0 |
| sam3_lite_text | Sam3LiteTextConfig | eligible | 5 |
| sam3_lite_text_detr_decoder | Sam3LiteTextDETRDecoderConfig | no-qualifying-checkpoint | 0 |
| sam3_lite_text_detr_encoder | Sam3LiteTextDETREncoderConfig | no-qualifying-checkpoint | 0 |
| sam3_lite_text_geometry_encoder | Sam3LiteTextGeometryEncoderConfig | no-qualifying-checkpoint | 0 |
| sam3_lite_text_mask_decoder | Sam3LiteTextMaskDecoderConfig | no-qualifying-checkpoint | 0 |
| sam3_lite_text_text_model | Sam3LiteTextTextConfig | eligible | 1 |
| sam3_mask_decoder | Sam3MaskDecoderConfig | no-qualifying-checkpoint | 0 |
| sam3_tracker | Sam3TrackerConfig | eligible | 1 |
| sam3_tracker_video | Sam3TrackerVideoConfig | no-qualifying-checkpoint | 0 |
| sam3_video | Sam3VideoConfig | eligible | 16 |
| sam3_vision_model | Sam3VisionConfig | eligible | 1 |
| sam3_vit_model | Sam3ViTConfig | eligible | 1 |
| sam_hq | SamHQConfig | eligible | 1 |
| sam_hq_vision_model | SamHQVisionConfig | eligible | 1 |
| sam_vision_model | SamVisionConfig | eligible | 1 |
| sapiens2 | Sapiens2Config | eligible | 16 |
| sapiens2_head | Sapiens2HeadConfig | no-qualifying-checkpoint | 0 |
| seamless_m4t | SeamlessM4TConfig | eligible | 4 |
| seamless_m4t_v2 | SeamlessM4Tv2Config | eligible | 32 |
| seed_oss | SeedOssConfig | eligible | 6 |
| segformer | SegformerConfig | eligible | 1 |
| seggpt | SegGptConfig | eligible | 4 |
| sew | SEWConfig | eligible | 1 |
| sew-d | SEWDConfig | eligible | 1 |
| shieldgemma2 | ShieldGemma2Config | no-qualifying-checkpoint | 4 |
| siglip | SiglipConfig | eligible | 5 |
| siglip2 | Siglip2Config | search-limit | 100 |
| siglip2_text_model | Siglip2TextConfig | no-qualifying-checkpoint | 1 |
| siglip2_vision_model | Siglip2VisionConfig | eligible | 1 |
| siglip_text_model | SiglipTextConfig | eligible | 1 |
| siglip_vision_model | SiglipVisionConfig | eligible | 1 |
| slanet | SLANetConfig | eligible | 1 |
| slanext | SLANeXtConfig | eligible | 1 |
| smollm3 | SmolLM3Config | eligible | 3 |
| smolvlm | SmolVLMConfig | eligible | 4 |
| smolvlm_vision | SmolVLMVisionConfig | eligible | 1 |
| solar_open | SolarOpenConfig | eligible | 3 |
| speech-encoder-decoder | SpeechEncoderDecoderConfig | eligible | 1 |
| speech_to_text | Speech2TextConfig | eligible | 1 |
| speecht5 | SpeechT5Config | eligible | 1 |
| speecht5_hifigan | SpeechT5HifiGanConfig | no-qualifying-checkpoint | 0 |
| splinter | SplinterConfig | eligible | 1 |
| squeezebert | SqueezeBertConfig | eligible | 1 |
| stablelm | StableLmConfig | eligible | 1 |
| starcoder2 | Starcoder2Config | eligible | 1 |
| step3p5 | Step3p7TextConfig | no-qualifying-checkpoint | 37 |
| step3p5_vision | Step3p7VisionConfig | no-qualifying-checkpoint | 0 |
| step3p7 | Step3p7Config | eligible | 51 |
| superglue | SuperGlueConfig | eligible | 1 |
| superpoint | SuperPointConfig | eligible | 1 |
| swiftformer | SwiftFormerConfig | eligible | 1 |
| swin | SwinConfig | eligible | 1 |
| swin2sr | Swin2SRConfig | eligible | 1 |
| swinv2 | Swinv2Config | eligible | 1 |
| switch_transformers | SwitchTransformersConfig | eligible | 8 |
| t5 | T5Config | eligible | 1 |
| t5_gemma_module | T5GemmaModuleConfig | no-qualifying-checkpoint | 2 |
| t5gemma | T5GemmaConfig | eligible | 10 |
| t5gemma2 | T5Gemma2Config | eligible | 59 |
| t5gemma2_decoder | T5Gemma2DecoderConfig | no-qualifying-checkpoint | 0 |
| t5gemma2_encoder | T5Gemma2EncoderConfig | eligible | 1 |
| t5gemma2_text | T5Gemma2TextConfig | eligible | 1 |
| table-transformer | TableTransformerConfig | eligible | 1 |
| tapas | TapasConfig | eligible | 2 |
| textnet | TextNetConfig | eligible | 1 |
| time_series_transformer | TimeSeriesTransformerConfig | eligible | 1 |
| timesfm | TimesFmConfig | eligible | 1 |
| timesfm2_5 | TimesFm2_5Config | eligible | 1 |
| timesformer | TimesformerConfig | eligible | 1 |
| timm_backbone | TimmBackboneConfig | eligible | 1 |
| timm_wrapper | TimmWrapperConfig | eligible | 1 |
| tipsv2 | Tipsv2Config | eligible | 2 |
| tipsv2_dpt | Tipsv2DptConfig | eligible | 1 |
| tipsv2_text_model | Tipsv2TextConfig | eligible | 1 |
| tipsv2_vision_model | Tipsv2VisionConfig | eligible | 1 |
| trocr | TrOCRConfig | eligible | 98 |
| tvp | TvpConfig | eligible | 1 |
| udop | UdopConfig | eligible | 13 |
| umt5 | UMT5Config | eligible | 1 |
| unispeech | UniSpeechConfig | eligible | 2 |
| unispeech-sat | UniSpeechSatConfig | eligible | 2 |
| univnet | UnivNetConfig | eligible | 1 |
| upernet | UperNetConfig | eligible | 1 |
| uvdoc | UVDocConfig | eligible | 1 |
| uvdoc_backbone | UVDocBackboneConfig | eligible | 1 |
| vaultgemma | VaultGemmaConfig | eligible | 2 |
| vibevoice | VibeVoiceConfig | search-limit | 100 |
| vibevoice_acoustic_tokenizer | VibeVoiceAcousticTokenizerConfig | eligible | 6 |
| vibevoice_acoustic_tokenizer_decoder | VibeVoiceAcousticTokenizerDecoderConfig | eligible | 1 |
| vibevoice_acoustic_tokenizer_encoder | VibeVoiceAcousticTokenizerEncoderConfig | eligible | 1 |
| vibevoice_asr | VibeVoiceAsrConfig | eligible | 17 |
| video_llama_3 | VideoLlama3Config | eligible | 3 |
| video_llama_3_vision | VideoLlama3VisionConfig | eligible | 1 |
| video_llava | VideoLlavaConfig | eligible | 11 |
| videomae | VideoMAEConfig | eligible | 1 |
| videomt | VideomtConfig | eligible | 1 |
| videoprism | VideoPrismConfig | eligible | 2 |
| videoprism_text_model | VideoPrismTextConfig | no-qualifying-checkpoint | 0 |
| videoprism_vision_model | VideoPrismVisionConfig | eligible | 1 |
| vilt | ViltConfig | eligible | 1 |
| vipllava | VipLlavaConfig | eligible | 3 |
| vision-encoder-decoder | VisionEncoderDecoderConfig | eligible | 7 |
| vision-text-dual-encoder | VisionTextDualEncoderConfig | eligible | 1 |
| visual_bert | VisualBertConfig | eligible | 1 |
| vit | ViTConfig | eligible | 1 |
| vit_mae | ViTMAEConfig | eligible | 1 |
| vit_msn | ViTMSNConfig | eligible | 1 |
| vitdet | VitDetConfig | eligible | 1 |
| vitmatte | VitMatteConfig | eligible | 1 |
| vitpose | VitPoseConfig | eligible | 1 |
| vitpose_backbone | VitPoseBackboneConfig | eligible | 1 |
| vits | VitsConfig | eligible | 1 |
| vivit | VivitConfig | eligible | 1 |
| vjepa2 | VJEPA2Config | eligible | 12 |
| voxtral | VoxtralConfig | eligible | 18 |
| voxtral_encoder | VoxtralEncoderConfig | eligible | 1 |
| voxtral_realtime | VoxtralRealtimeConfig | eligible | 3 |
| voxtral_realtime_encoder | VoxtralRealtimeEncoderConfig | eligible | 1 |
| voxtral_realtime_text | VoxtralRealtimeTextConfig | eligible | 1 |
| wav2vec2 | Wav2Vec2Config | eligible | 3 |
| wav2vec2-bert | Wav2Vec2BertConfig | eligible | 4 |
| wav2vec2-conformer | Wav2Vec2ConformerConfig | eligible | 2 |
| wavlm | WavLMConfig | eligible | 10 |
| whisper | WhisperConfig | eligible | 3 |
| xclip | XCLIPConfig | eligible | 1 |
| xclip_text_model | XCLIPTextConfig | no-qualifying-checkpoint | 0 |
| xclip_vision_model | XCLIPVisionConfig | no-qualifying-checkpoint | 0 |
| xcodec | XcodecConfig | eligible | 1 |
| xcodec2 | Xcodec2Config | eligible | 8 |
| xglm | XGLMConfig | eligible | 2 |
| xlm | XLMConfig | eligible | 1 |
| xlm-roberta | XLMRobertaConfig | eligible | 9 |
| xlm-roberta-xl | XLMRobertaXLConfig | eligible | 2 |
| xlnet | XLNetConfig | eligible | 1 |
| xlstm | xLSTMConfig | eligible | 4 |
| xmod | XmodConfig | eligible | 2 |
| yolos | YolosConfig | eligible | 1 |
| yoso | YosoConfig | eligible | 1 |
| youtu | YoutuConfig | eligible | 7 |
| zamba | ZambaConfig | eligible | 3 |
| zamba2 | Zamba2Config | eligible | 11 |
| zaya | ZayaConfig | eligible | 7 |
| zoedepth | ZoeDepthConfig | eligible | 5 |
