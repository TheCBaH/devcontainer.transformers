# Most downloaded Transformers checkpoints

Transformers 5.18.0; scanned 2026-10-11T03:08:14.167956+00:00.

Global Hub downloads order, retaining multiple checkpoints per architecture. Public ungated repositories tagged with the Transformers library are considered; the pinned config model_type must be supported. Native graph export is not certified. Published test checkpoints and quantized weights are included. Downloads are the Hub rolling-window snapshot, not lifetime downloads. Configs and shard indices are downloaded; weights are not.

Eligible means published full safetensors strictly below 1,000,000,000 bytes in total across the repository. The overall ranking also shows rejected sizes/formats.

Examined 404 repositories; scan status: complete. Metadata errors may leave gaps.

| Rank | Checkpoint | Architecture | Task | Downloads | Safetensors bytes | Eligibility |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 1 | [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/tree/1110a243fdf4706b3f48f1d95db1a4f5529b4d41) | bert | sentence-similarity | 225,633,601 | 90,868,376 | eligible |
| 2 | [cross-encoder/ms-marco-MiniLM-L6-v2](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L6-v2/tree/233902d25c440f23af6f7d6e94d2946bac0bee0a) | bert | text-ranking | 80,398,259 | 90,870,598 | eligible |
| 3 | [BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5/tree/5c38ec7c405ec4b44b94cc5a9bb96e735b38267a) | bert | feature-extraction | 60,561,582 | 133,466,304 | eligible |
| 4 | [sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2/tree/e8f8c211226b894fcb81acc59f3b34ba3efd5f42) | bert | sentence-similarity | 48,797,791 | 470,641,600 | eligible |
| 5 | [google/electra-base-discriminator](https://huggingface.co/google/electra-base-discriminator/tree/1ae76a97c7e84a4e640876a07453fccd636f0667) | electra | unspecified | 45,353,786 | unknown | no-safetensors |
| 6 | [google-bert/bert-base-uncased](https://huggingface.co/google-bert/bert-base-uncased/tree/86b5e0934494bd15c9632b12f734a8a67f723594) | bert | fill-mask | 36,586,526 | 440,449,768 | eligible |
| 7 | [Qwen/Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B/tree/c1899de289a04d12100db370d81485cdf75e47ca) | qwen3 | text-generation | 30,768,858 | 1,503,300,328 | too-large |
| 8 | [google-t5/t5-small](https://huggingface.co/google-t5/t5-small/tree/df1b051c49625cf57a3d0d8d3863ed4d13564fe4) | t5 | translation | 24,098,674 | 242,043,056 | eligible |
| 9 | [openai/clip-vit-base-patch32](https://huggingface.co/openai/clip-vit-base-patch32/tree/3d74acf9a28c67741b2f4f2ea7635f0aaf6f0268) | clip | zero-shot-image-classification | 19,497,931 | unknown | no-safetensors |
| 10 | [sentence-transformers/all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2/tree/e8c3b32edf5434bc2275fc9bab85f82640a19130) | mpnet | sentence-similarity | 18,381,804 | 437,971,872 | eligible |
| 11 | [BAAI/bge-reranker-v2-m3](https://huggingface.co/BAAI/bge-reranker-v2-m3/tree/953dc6f6f85a1b2dbfca4c34a2796e7dde08d41e) | xlm-roberta | text-classification | 16,384,212 | 2,271,071,852 | too-large |
| 12 | [jonatasgrosman/wav2vec2-large-xlsr-53-japanese](https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-japanese/tree/cf031e020336460d15a417eba710bbc5bb43be9a) | wav2vec2 | automatic-speech-recognition | 15,922,793 | unknown | no-safetensors |
| 13 | [openai-community/gpt2](https://huggingface.co/openai-community/gpt2/tree/607a30d783dfa663caf39e06633721c8d4cfcd7e) | gpt2 | text-generation | 15,521,105 | 548,105,171 | eligible |
| 14 | [nomic-ai/nomic-embed-text-v1.5](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5/tree/e9b6763023c676ca8431644204f50c2b100d9aab) | nomic_bert | sentence-similarity | 12,877,830 | 546,938,168 | eligible |
| 15 | [FacebookAI/xlm-roberta-base](https://huggingface.co/FacebookAI/xlm-roberta-base/tree/e73636d4f797dec63c3081bb6ed5c7b0bb3f2089) | xlm-roberta | fill-mask | 12,872,726 | 1,115,567,652 | too-large |
| 16 | [google/vit-base-patch16-224](https://huggingface.co/google/vit-base-patch16-224/tree/3f49326eb077187dfe1c2a2bb15fbd74e6ab91e3) | vit | image-classification | 12,341,382 | 346,293,852 | eligible |
| 17 | [google/gemma-4-26B-A4B-it](https://huggingface.co/google/gemma-4-26B-A4B-it/tree/4d7ae4984b7db7de8f8457170b3f1a419ee76d52) | gemma4 | image-text-to-text | 11,854,067 | 51,612,009,916 | too-large |
| 18 | [Qwen/Qwen3-4B](https://huggingface.co/Qwen/Qwen3-4B/tree/1cfa9a7208912126459214e8b04321603b3df60c) | qwen3 | text-generation | 10,600,642 | 8,044,982,000 | too-large |
| 19 | [BAAI/bge-large-en-v1.5](https://huggingface.co/BAAI/bge-large-en-v1.5/tree/d4aa6901d3a41ba39fb536a557fa166f842b0e09) | bert | feature-extraction | 10,037,064 | 1,340,616,616 | too-large |
| 20 | [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B/tree/b968826d9c46dd6066d109eabc6255188de91218) | qwen3 | text-generation | 9,821,408 | 16,381,516,776 | too-large |
| 21 | [sentence-transformers/paraphrase-multilingual-mpnet-base-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2/tree/4328cf26390c98c5e3c738b4460a05b95f4911f5) | xlm-roberta | sentence-similarity | 9,693,187 | 1,112,201,288 | too-large |
| 22 | [google/gemma-4-31B-it](https://huggingface.co/google/gemma-4-31B-it/tree/842da3794eaa0b77d5f08bae87a17459d91ff475) | gemma4 | image-text-to-text | 9,619,659 | 62,546,338,248 | too-large |
| 23 | [BAAI/bge-base-en-v1.5](https://huggingface.co/BAAI/bge-base-en-v1.5/tree/a5beb1e3e68b9ab74eb54cfd186867f64f240e1a) | bert | feature-extraction | 9,401,970 | 437,955,512 | eligible |
| 24 | [Qwen/Qwen3-VL-8B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct/tree/0c351dd01ed87e9c1b53cbc748cba10e6187ff3b) | qwen3_vl | image-text-to-text | 8,975,548 | 17,534,339,512 | too-large |
| 25 | [Qwen/Qwen3-Embedding-0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B/tree/97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3) | qwen3 | feature-extraction | 8,750,378 | 1,191,586,416 | too-large |
| 26 | [Qwen/Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B/tree/c202236235762e1c871ad0ccb60c8ee5ba337b9a) | qwen3_5 | image-text-to-text | 8,319,798 | 19,306,310,880 | too-large |
| 27 | [laion/clap-htsat-fused](https://huggingface.co/laion/clap-htsat-fused/tree/365dea6ef167def6676140ed93bbc43f84dabb28) | clap | audio-classification | 8,185,193 | 614,496,152 | eligible |
| 28 | [FacebookAI/roberta-base](https://huggingface.co/FacebookAI/roberta-base/tree/e2da8e2f811d1448a5b465c236feacd80ffbac7b) | roberta | fill-mask | 8,172,185 | 498,818,054 | eligible |
| 29 | [facebook/contriever](https://huggingface.co/facebook/contriever/tree/2bd46a25019aeea091fd42d1f0fd4801675cf699) | bert | unspecified | 8,100,336 | unknown | no-safetensors |
| 30 | [Qwen/Qwen2.5-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct/tree/a09a35458c702b33eeacc393d103063234e8bc28) | qwen2 | text-generation | 8,077,595 | 15,231,271,888 | too-large |
| 31 | [Qwen/Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B/tree/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a) | qwen3_5 | image-text-to-text | 7,913,682 | 9,319,828,096 | too-large |
| 32 | [openai/clip-vit-large-patch14](https://huggingface.co/openai/clip-vit-large-patch14/tree/32bd64288804d66eefd0ccbe215aa642df71cc41) | clip | zero-shot-image-classification | 7,845,989 | 1,710,540,580 | too-large |
| 33 | [distilbert/distilbert-base-uncased](https://huggingface.co/distilbert/distilbert-base-uncased/tree/12040accade4e8a0f71eabdb258fecc2e7e948be) | distilbert | fill-mask | 7,837,070 | 267,954,768 | eligible |
| 34 | [Qwen/Qwen2.5-0.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct/tree/7ae557604adf67be50417f59c2c2f167def9a775) | qwen2 | text-generation | 7,302,712 | 988,097,824 | eligible |
| 35 | [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B/tree/1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0) | qwen3_5 | image-text-to-text | 6,768,654 | 55,563,006,776 | too-large |
| 36 | [FacebookAI/roberta-large](https://huggingface.co/FacebookAI/roberta-large/tree/722cf37b1afa9454edce342e7895e588b6ff1d59) | roberta | fill-mask | 6,523,322 | 1,421,700,479 | too-large |
| 37 | [zai-org/GLM-5.3-Flash](https://huggingface.co/zai-org/GLM-5.3-Flash/tree/eb9eb208eb0d988989d07a6a12d0fdeb5f52574a) | glm5_next | image-text-to-text | 6,479,110 | 328,337,455,672 | too-large |
| 38 | [Qwen/Qwen2.5-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct/tree/989aa7980e4cf806f80c7fef2b1adb7bc71aa306) | qwen2 | text-generation | 6,473,697 | 3,087,467,144 | too-large |
| 39 | [openai/whisper-large-v3-turbo](https://huggingface.co/openai/whisper-large-v3-turbo/tree/41f01f3fe87f28c78e2fbf8b568835947dd65ed9) | whisper | automatic-speech-recognition | 6,316,207 | 1,617,824,864 | too-large |
| 40 | [trl-internal-testing/tiny-Qwen2ForCausalLM-2.5](https://huggingface.co/trl-internal-testing/tiny-Qwen2ForCausalLM-2.5/tree/ce8d0bf270b28c8fab026ced69fe8aa14b0f0eda) | qwen2 | text-generation | 6,239,622 | 4,872,824 | eligible |
| 41 | [facebook/opt-125m](https://huggingface.co/facebook/opt-125m/tree/27dcfa74d334bc871f3234de431e71c6eeba5dd6) | opt | text-generation | 6,031,770 | unknown | no-safetensors |
| 42 | [openai/gpt-oss-20b](https://huggingface.co/openai/gpt-oss-20b/tree/6cee5e81ee83917806bbde320786a8fb61efebee) | gpt_oss | text-generation | 5,950,578 | 27,522,617,888 | too-large |
| 43 | [RadixArk/Kimi-K3-DSpark](https://huggingface.co/RadixArk/Kimi-K3-DSpark/tree/3c5bac301d9cf392706189d82ed947feca6c2f0f) | qwen3 | text-generation | 5,941,327 | 4,498,585,858 | too-large |
| 44 | [microsoft/mdeberta-v3-base](https://huggingface.co/microsoft/mdeberta-v3-base/tree/a0484667b22365f84929a935b5e50a51f71f159d) | deberta-v2 | fill-mask | 5,777,633 | unknown | no-safetensors |
| 45 | [cross-encoder/ms-marco-MiniLM-L4-v2](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L4-v2/tree/777b2f369bc1c2f850df8bd367ed1654bda4497b) | bert | text-ranking | 5,768,275 | 76,671,186 | eligible |
| 46 | [Qwen/Qwen3-14B](https://huggingface.co/Qwen/Qwen3-14B/tree/40c069824f4251a91eefaf281ebe4c544efd3e18) | qwen3 | text-generation | 5,422,096 | 29,536,665,640 | too-large |
| 47 | [Qwen/Qwen2.5-VL-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct/tree/cc594898137f460bfe9f0759e9844b3ce807cfb5) | qwen2_5_vl | image-text-to-text | 5,310,600 | 16,584,414,560 | too-large |
| 48 | [jonatasgrosman/wav2vec2-large-xlsr-53-portuguese](https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-portuguese/tree/634ac655299bcdc46c83bc01da9bab52d2987e4f) | wav2vec2 | automatic-speech-recognition | 5,274,731 | unknown | no-safetensors |
| 49 | [ibm-granite/granite-embedding-small-english-r2](https://huggingface.co/ibm-granite/granite-embedding-small-english-r2/tree/2ab6fa8ea2d674564defd37171ae19079b864b33) | modernbert | feature-extraction | 5,141,679 | 95,332,048 | eligible |
| 50 | [dphn/dolphin-2.9.1-yi-1.5-34b](https://huggingface.co/dphn/dolphin-2.9.1-yi-1.5-34b/tree/0141cba238d0faad09bc240ea7af14c9ea5aec44) | llama | text-generation | 4,671,902 | 68,777,898,032 | too-large |
| 51 | [deepseek-ai/DeepSeek-V3.2](https://huggingface.co/deepseek-ai/DeepSeek-V3.2/tree/a7e62ac04ecb2c0a54d736dc46601c5606cf10a6) | deepseek_v32 | text-generation | 4,576,177 | 689,483,049,129 | too-large |
| 52 | [deepseek-ai/DeepSeek-V4-Flash-0731](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731/tree/7872f01b1d1fe23eabc4c98b48bffcef5a386062) | deepseek_v4 | text-generation | 4,494,443 | 166,886,535,336 | too-large |
| 53 | [Qwen/Qwen3.8-27B-FP8](https://huggingface.co/Qwen/Qwen3.8-27B-FP8/tree/017b9c7af6b5689d5dd426a76e0bc077eb5ca20a) | qwen3_5 | image-text-to-text | 4,465,358 | 30,866,866,928 | too-large |
| 54 | [ProsusAI/finbert](https://huggingface.co/ProsusAI/finbert/tree/4556d13015211d73dccd3fdd39d39232506f3e43) | bert | text-classification | 4,451,746 | unknown | no-safetensors |
| 55 | [google/gemma-4-E4B-it](https://huggingface.co/google/gemma-4-E4B-it/tree/ee0ef6023621cff504d758262d4e04895a5af4a2) | gemma4 | any-to-any | 4,305,979 | 15,992,595,884 | too-large |
| 56 | [Qwen/Qwen2.5-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/tree/aa8e72537993ba99e69dfaafa59ed015b17504d1) | qwen2 | text-generation | 4,251,259 | 6,171,926,992 | too-large |
| 57 | [BAAI/bge-small-zh-v1.5](https://huggingface.co/BAAI/bge-small-zh-v1.5/tree/7999e1d3359715c523056ef9478215996d62a620) | bert | feature-extraction | 4,238,612 | 95,827,648 | eligible |
| 58 | [Qwen/Qwen3.6-35B-A3B-FP8](https://huggingface.co/Qwen/Qwen3.6-35B-A3B-FP8/tree/95a723d08a9490559dae23d0cff1d9466213d989) | qwen3_5_moe | image-text-to-text | 4,170,844 | 37,463,662,160 | too-large |
| 59 | [lmstudio-community/Qwen3.8-27B-MLX-4bit](https://huggingface.co/lmstudio-community/Qwen3.8-27B-MLX-4bit/tree/6067b15cf581666a4aecf6af3afaba4bb5efc20c) | qwen3_5 | image-text-to-text | 4,112,241 | 16,054,541,599 | too-large |
| 60 | [facebook/esm2_t33_650M_UR50D](https://huggingface.co/facebook/esm2_t33_650M_UR50D/tree/08e4846e537177426273712802403f7ba8261b6c) | esm | fill-mask | 4,094,578 | 2,609,506,392 | too-large |
| 61 | [answerdotai/ModernBERT-base](https://huggingface.co/answerdotai/ModernBERT-base/tree/8949b909ec900327062f0ebf497f51aef5e6f0c8) | modernbert | fill-mask | 4,025,520 | 598,635,032 | eligible |
| 62 | [jonatasgrosman/wav2vec2-large-xlsr-53-russian](https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-russian/tree/2329100508896c6d9b157019803ab5601e6f3406) | wav2vec2 | automatic-speech-recognition | 3,997,190 | unknown | no-safetensors |
| 63 | [lmstudio-community/Qwen3.8-27B-MLX-8bit](https://huggingface.co/lmstudio-community/Qwen3.8-27B-MLX-8bit/tree/241ebb5f1d60b122fd653da658836a55feb9e2b0) | qwen3_5 | image-text-to-text | 3,941,460 | 29,501,218,261 | too-large |
| 64 | [lmstudio-community/Qwen3.8-27B-MLX-6bit](https://huggingface.co/lmstudio-community/Qwen3.8-27B-MLX-6bit/tree/05f38c1f39e2f39619653616fe8e96a5d676358e) | qwen3_5 | image-text-to-text | 3,924,317 | 22,777,879,765 | too-large |
| 65 | [lmstudio-community/Qwen3.8-27B-MLX-5bit](https://huggingface.co/lmstudio-community/Qwen3.8-27B-MLX-5bit/tree/b9ad7b92aa2fd07b041f4b8b3aa459941f8abbf7) | qwen3_5 | image-text-to-text | 3,907,837 | 19,416,210,779 | too-large |
| 66 | [openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b/tree/b5c939de8f754692c1647ca79fbf85e8c1e70f8a) | gpt_oss | text-generation | 3,845,925 | 130,497,762,984 | too-large |
| 67 | [google/siglip2-base-patch16-256](https://huggingface.co/google/siglip2-base-patch16-256/tree/3f9f96cb90da5dbc758b01813f2f6f1aee24c1ab) | siglip | zero-shot-image-classification | 3,845,233 | 1,500,985,224 | too-large |
| 68 | [openai/whisper-large-v3](https://huggingface.co/openai/whisper-large-v3/tree/06f233fe06e710322aca913c1bc4249a0d71fce1) | whisper | automatic-speech-recognition | 3,791,795 | 9,261,243,048 | too-large |
| 69 | [SamLowe/roberta-base-go_emotions](https://huggingface.co/SamLowe/roberta-base-go_emotions/tree/d75048347613a25d77de8cf6412eaae9fa7b26be) | roberta | text-classification | 3,600,369 | 498,697,004 | eligible |
| 70 | [Qwen/Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507/tree/cdbee75f17c01a7cc42f958dc650907174af0554) | qwen3 | text-generation | 3,563,213 | 8,044,982,000 | too-large |
| 71 | [Qwen/Qwen3.6-35B-A3B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B/tree/995ad96eacd98c81ed38be0c5b274b04031597b0) | qwen3_5_moe | image-text-to-text | 3,545,718 | 71,903,776,776 | too-large |
| 72 | [google-bert/bert-base-cased](https://huggingface.co/google-bert/bert-base-cased/tree/cd5ef92a9fb2f889e972770a36d4ed042daf221e) | bert | fill-mask | 3,531,700 | 435,755,784 | eligible |
| 73 | [Qwen/Qwen3-1.7B](https://huggingface.co/Qwen/Qwen3-1.7B/tree/70d244cc86ccca08cf5af4e1e306ecf908b1ad5e) | qwen3 | text-generation | 3,480,034 | 4,063,515,592 | too-large |
| 74 | [Qwen/Qwen3-32B](https://huggingface.co/Qwen/Qwen3-32B/tree/9216db5781bf21249d130ec9da846c4624c16137) | qwen3 | text-generation | 3,466,526 | 65,524,328,560 | too-large |
| 75 | [EleutherAI/pythia-160m](https://huggingface.co/EleutherAI/pythia-160m/tree/50f5173d932e8e61f858120bcb800b97af589f46) | gpt_neox | text-generation | 3,461,088 | 374,998,696 | eligible |
| 76 | [Qwen/Qwen3.5-2B](https://huggingface.co/Qwen/Qwen3.5-2B/tree/15852e8c16360a2fea060d615a32b45270f8a8fc) | qwen3_5 | image-text-to-text | 3,355,912 | 4,548,221,488 | too-large |
| 77 | [w11wo/indonesian-roberta-base-posp-tagger](https://huggingface.co/w11wo/indonesian-roberta-base-posp-tagger/tree/5067796360930a7b9c5e1d76e1ab2b8c6b4cd103) | roberta | token-classification | 3,300,231 | 496,324,072 | eligible |
| 78 | [openai/whisper-small](https://huggingface.co/openai/whisper-small/tree/973afd24965f72e36ca33b3055d56a652f456b4d) | whisper | automatic-speech-recognition | 3,238,936 | 966,995,080 | eligible |
| 79 | [sentence-transformers/all-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2/tree/a50ef00143b4d5391434df20ae11632588ac25be) | bert | sentence-similarity | 3,162,825 | 133,466,304 | eligible |
| 80 | [Qwen/Qwen3-VL-4B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct/tree/ebb281ec70b05090aa6165b016eac8ec08e71b17) | qwen3_vl | image-text-to-text | 3,113,173 | 8,875,719,344 | too-large |
| 81 | [microsoft/Florence-2-base](https://huggingface.co/microsoft/Florence-2-base/tree/5ca5edf5bd017b9919c05d08aebef5e4c7ac3bac) | florence2 | image-text-to-text | 3,030,125 | 463,221,266 | eligible |
| 82 | [google/gemma-4-E2B-it](https://huggingface.co/google/gemma-4-E2B-it/tree/3e22461f65e89153144f8adb70e3b8c2cc9845a7) | gemma4 | any-to-any | 3,020,170 | 10,246,621,918 | too-large |
| 83 | [Qwen/Qwen3-14B-AWQ](https://huggingface.co/Qwen/Qwen3-14B-AWQ/tree/31c69efc29464b6bb0aee1398b5a7b50a99340c3) | qwen3 | text-generation | 2,984,692 | 9,976,690,240 | too-large |
| 84 | [E-MIMIC/inclusively-reformulation-it5](https://huggingface.co/E-MIMIC/inclusively-reformulation-it5/tree/7638c77268d2a9f9057ab81007e0e114a2b552e1) | t5 | unspecified | 2,973,823 | 3,132,464,096 | too-large |
| 85 | [facebook/dinov2-base](https://huggingface.co/facebook/dinov2-base/tree/f9e44c814b77203eaa57a6bdbbd535f21ede1415) | dinov2 | image-feature-extraction | 2,947,912 | 346,345,912 | eligible |
| 86 | [microsoft/deberta-v3-base](https://huggingface.co/microsoft/deberta-v3-base/tree/8ccc9b6f36199bec6961081d44eb72fb3f7353f3) | deberta-v2 | fill-mask | 2,784,836 | unknown | no-safetensors |
| 87 | [facebook/dinov2-small](https://huggingface.co/facebook/dinov2-small/tree/ed25f3a31f01632728cabb09d1542f84ab7b0056) | dinov2 | image-feature-extraction | 2,747,055 | 88,249,960 | eligible |
| 88 | [distilbert/distilbert-base-uncased-finetuned-sst-2-english](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english/tree/714eb0fa89d2f80546fda750413ed43d93601a13) | distilbert | text-classification | 2,732,025 | 267,832,558 | eligible |
| 89 | [sentence-transformers/all-distilroberta-v1](https://huggingface.co/sentence-transformers/all-distilroberta-v1/tree/842eaed40bee4d61673a81c92d5689a8fed7a09f) | roberta | sentence-similarity | 2,730,583 | 328,489,328 | eligible |
| 90 | [nomic-ai/nomic-embed-text-v1](https://huggingface.co/nomic-ai/nomic-embed-text-v1/tree/3ac47f125a41961d13b397d0332866be2f9152e1) | nomic_bert | sentence-similarity | 2,671,015 | 546,938,168 | eligible |
| 91 | [cardiffnlp/twitter-roberta-base-sentiment-latest](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest/tree/3216a57f2a0d9c45a2e6c20157c20c49fb4bf9c7) | roberta | text-classification | 2,625,543 | unknown | no-safetensors |
| 92 | [FacebookAI/xlm-roberta-large](https://huggingface.co/FacebookAI/xlm-roberta-large/tree/c23d21b0620b635a76227c604d44e43a9f0ee389) | xlm-roberta | fill-mask | 2,622,410 | 2,244,817,354 | too-large |
| 93 | [Qwen/Qwen3-VL-2B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-2B-Instruct/tree/89644892e4d85e24eaac8bacfd4f463576704203) | qwen3_vl | image-text-to-text | 2,607,120 | 4,255,140,312 | too-large |
| 94 | [facebook/bart-large-mnli](https://huggingface.co/facebook/bart-large-mnli/tree/d7645e127eaf1aefc7862fd59a17a5aa8558b8ce) | bart | zero-shot-classification | 2,598,918 | 1,629,437,147 | too-large |
| 95 | [MahmoudAshraf/mms-300m-1130-forced-aligner](https://huggingface.co/MahmoudAshraf/mms-300m-1130-forced-aligner/tree/49402e9577b1158620820667c218cd494cc44486) | wav2vec2 | automatic-speech-recognition | 2,582,330 | 1,261,930,388 | too-large |
| 96 | [Qwen/Qwen3.5-0.8B](https://huggingface.co/Qwen/Qwen3.5-0.8B/tree/2fc06364715b967f1860aea9cf38778875588b17) | qwen3_5 | image-text-to-text | 2,561,283 | 1,746,942,600 | too-large |
| 97 | [jonatasgrosman/wav2vec2-large-xlsr-53-polish](https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-polish/tree/6b1cea36bd8bc5f65ec8081667cd9c0207d51970) | wav2vec2 | automatic-speech-recognition | 2,546,065 | unknown | no-safetensors |
| 98 | [Qwen/Qwen2.5-7B-Instruct-AWQ](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-AWQ/tree/b25037543e9394b818fdfca67ab2a00ecc7dd641) | qwen2 | text-generation | 2,497,317 | 5,570,829,760 | too-large |
| 99 | [google-bert/bert-base-multilingual-uncased](https://huggingface.co/google-bert/bert-base-multilingual-uncased/tree/7cbf9a625e29989f6b9c6c2fa68234c304f7e38f) | bert | fill-mask | 2,426,601 | 672,247,920 | eligible |
| 100 | [prithivMLmods/Gender-Classifier-Mini](https://huggingface.co/prithivMLmods/Gender-Classifier-Mini/tree/4855356b698e88ba57996836bb35091f81932667) | siglip | image-classification | 2,419,562 | 1,114,703,976 | too-large |
