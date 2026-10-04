.DEFAULT_GOAL := smoke
UV ?= uv
WORKERS ?= 1
TIMEOUT ?= 900
SUBSET ?=
RUN = $(UV) run --frozen
OPTIONS = --workers $(WORKERS) --timeout $(TIMEOUT) $(if $(SUBSET),--subset $(SUBSET),)

.PHONY: setup smoke test report report.ci models.select models models.verify check-models check-tree-clean research.reference clean
setup:
	$(UV) sync --frozen
smoke: setup
	$(RUN) hf-pt2 smoke $(OPTIONS)
test: setup
	$(RUN) pytest -q
report: setup
	$(RUN) hf-pt2 report $(OPTIONS)
report.ci: report
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
