SHELL := /bin/bash

VENV := .venv
UV := uv
PYTHON := $(VENV)/bin/python
PYTEST := $(VENV)/bin/pytest
BLACK := $(VENV)/bin/black
ISORT := $(VENV)/bin/isort
RUFF := $(VENV)/bin/ruff
MYPY := $(VENV)/bin/mypy

.PHONY: bootstrap doctor check lint typecheck format format-check unit build clean-local

bootstrap:
	$(UV) venv $(VENV)
	$(UV) pip install --python $(PYTHON) -e ".[dev]"
	$(UV) pip install --python $(PYTHON) build

doctor:
	scripts/doctor.sh

format:
	$(BLACK) src tests
	$(ISORT) src tests

format-check:
	$(BLACK) --check src tests
	$(ISORT) --check-only src tests

lint:
	$(RUFF) check src tests

typecheck:
	$(MYPY) src

unit:
	$(PYTEST) tests/unit

build:
	@if ! $(PYTHON) -c "import build" >/dev/null 2>&1; then \
		echo "ERROR: Python package 'build' is not installed in $(VENV)."; \
		echo "Run 'make bootstrap' (online) or '$(PYTHON) -m pip install build'."; \
		exit 1; \
	fi
	$(PYTHON) -m build

check: doctor format-check lint unit

clean-local:
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov dist build .coverage .coverage.* _tmp
