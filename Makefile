# AI_Keystone — the single command entry point.
#
# Windows note: `make` is not native. Run these via Git Bash, or install make
# (`choco install make`). PowerShell equivalents live in scripts/dev/ as they are added.
# Per the operating manual, the developer runs every command manually — this file
# documents the canonical commands, it is not executed by the assistant.

.DEFAULT_GOAL := help
.PHONY: help setup fmt lint type test check hooks

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

setup:  ## Create/refresh the conda env and install dev+test deps
	conda env update -p ./myvenv -f environment.yml || true
	pip install -e ".[dev,test]"
	pre-commit install

fmt:  ## Auto-format
	ruff format .

lint:  ## Lint (and the dependency rule, once src/ exists)
	ruff check .
	@command -v lint-imports >/dev/null 2>&1 && lint-imports || echo "import-linter: skipped (no src yet)"

type:  ## Type-check
	mypy src

test:  ## Run the test suite
	pytest

check: lint type test  ## Everything CI runs, locally

hooks:  ## Run pre-commit on all files
	pre-commit run --all-files
