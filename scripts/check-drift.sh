#!/usr/bin/env bash
set -euo pipefail
git diff --stat -- models results models.md models-selected.yaml symbolic-shapes.md catalogue.json 'ops-*'
if ! git diff --quiet -- models results models.md models-selected.yaml symbolic-shapes.md catalogue.json 'ops-*'; then
    git diff -- models results models.md models-selected.yaml symbolic-shapes.md catalogue.json 'ops-*' | head -c 16000 || true
    exit 1
fi
unexpected=$(git ls-files --others --exclude-standard -- models results)
if [ -n "$unexpected" ]; then
    printf 'Unexpected generated files:\n%s\n' "$unexpected"
    exit 1
fi
