.DEFAULT_GOAL := smoke
UV ?= uv
WORKERS ?= 1
TIMEOUT ?= 900
SUBSET ?=
RUN = $(UV) run --frozen
REPORT_PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
OPTIONS = --workers $(WORKERS) --timeout $(TIMEOUT) $(if $(SUBSET),--subset $(SUBSET),)

.PHONY: setup smoke test report report.ci report.symbolic models.select models models.verify check-models check-tree-clean research.reference clean
setup:
	$(UV) sync --frozen
smoke: setup
	$(RUN) hf-pt2 smoke $(OPTIONS)
test: setup
	$(RUN) pytest -q
report: setup
	$(RUN) hf-pt2 report $(OPTIONS)
	$(MAKE) report.symbolic
report.ci: report
report.symbolic:
	$(REPORT_PYTHON) scripts/report_symbolic_shapes.py
models.select: setup
	$(RUN) hf-pt2 select
models: setup
	$(RUN) hf-pt2 models $(OPTIONS)
models.verify: setup
	$(RUN) hf-pt2 verify
check-models:
	bash scripts/check-drift.sh
check-tree-clean: check-models
	git diff --exit-code
	test -z "$$(git ls-files --others --exclude-standard)"
research.reference: setup
	$(RUN) hf-pt2 research --population reference --output .build/reference $(OPTIONS)
clean:
	rm -rf .build .pytest_cache

.PHONY: models.fetch models.weights.verify models.generation models.generation.all models.heads research.extended models.precision.fp16 models.precision.bf16
GENERATION_OUTPUT ?= .build/generation
models.fetch: setup
	$(RUN) hf-pt2 fetch --subset $(SUBSET)
models.weights.verify: setup
	$(RUN) hf-pt2 bind --subset $(SUBSET) --graph $(GRAPH)
models.generation: setup
	$(RUN) hf-pt2 generation --output $(GENERATION_OUTPUT) $(OPTIONS)
models.generation.all: setup
	@set -e; for model in smollm2-135m t5-small whisper-tiny smolvlm-256m; do \
		$(RUN) hf-pt2 generation --subset $$model --output $(GENERATION_OUTPUT) --timeout $(TIMEOUT); \
	done
models.heads: setup
	$(RUN) hf-pt2 research --subset bert-tiny-sequence-classification,bert-tiny-qa,bert-tiny-token-classification,bert-tiny-masked-lm --output .build/heads --workers $(WORKERS) --timeout $(TIMEOUT)
research.extended: setup
	$(RUN) hf-pt2 research --subset yolos-tiny,segformer-b0,depth-anything-small,wav2vec2-base,smolvlm-256m --output .build/extended --workers $(WORKERS) --timeout $(TIMEOUT)
models.precision.fp16 models.precision.bf16: setup
	$(RUN) hf-pt2 research --dtype $(lastword $(subst ., ,$@)) --policy dynamo --subset bert-tiny,mobilevit-xxs,smollm2-135m --output .build/precision/$(lastword $(subst ., ,$@))-cast $(OPTIONS)
	$(RUN) hf-pt2 research --dtype $(lastword $(subst ., ,$@)) --policy autocast --subset bert-tiny,mobilevit-xxs,smollm2-135m --output .build/precision/$(lastword $(subst ., ,$@))-autocast $(OPTIONS)
