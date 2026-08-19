# AI_Keystone — the single command entry point.
#
# Cross-platform: recipes avoid shell-specific syntax (no grep/awk/command -v),
# so the same targets work on Windows (cmd via GNU make), Git Bash, and Linux/CI.
#
# --- First-time bootstrap (run once, manually) ------------------------------
#   conda create -p ./myvenv python=3.11 -y
#   conda env config vars set PYTHONNOUSERSITE=1 -p ./myvenv   # hermetic env
#   conda activate ./myvenv
#   conda install -c conda-forge make -y                       # Windows: no native make
#   make setup
# ---------------------------------------------------------------------------
#
# Per the operating manual, the developer runs every command manually — this file
# documents the canonical commands; the assistant never executes them.

.DEFAULT_GOAL := help
.PHONY: help setup verify fmt lint type test check hooks clean

help:  ## Show available targets
	@echo.
	@echo AI_Keystone - available commands
	@echo.
	@echo   make setup    Install dev+test tooling into the active env
	@echo   make verify   Verify the local environment (python, docker, postgres, pgvector)
	@echo   make fmt      Auto-format the codebase
	@echo   make lint     Lint (and the dependency rule, from Phase 1)
	@echo   make type     Type-check
	@echo   make test     Run the test suite
	@echo   make check    Everything CI runs, locally
	@echo   make hooks    Run pre-commit across all files
	@echo.

setup:  ## Install dev+test tooling into the ACTIVE env (activate ./myvenv first)
	pip install ruff mypy pre-commit import-linter pytest pytest-asyncio hypothesis "coverage[toml]"
	pre-commit install
	@echo From Phase 1 (once src/keystone exists) this becomes: pip install -e ".[dev,test]"

verify:  ## Verify the local environment is ready
	python scripts/dev/verify_env.py

fmt:  ## Auto-format
	ruff format .

lint:  ## Lint; the dependency rule is enforced from Phase 1 (leading - = non-fatal until then)
	ruff check .
	-lint-imports

type:  ## Type-check (no package until Phase 1)
	-mypy src

test:  ## Run the test suite (no tests until Phase 1)
	-pytest

check: lint type test  ## Everything CI runs, locally

hooks:  ## Run pre-commit on all files
	pre-commit run --all-files

clean:  ## Remove caches
	-rmdir /s /q .ruff_cache
	-rmdir /s /q .mypy_cache
	-rmdir /s /q .pytest_cache
