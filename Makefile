.PHONY: install lint format test test-py test-bash

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

install:
	python3 -m venv --system-site-packages $(VENV)
	$(PIP) install -e ".[dev]" -q

lint:
	$(VENV)/bin/ruff check src/ tests/

format:
	$(VENV)/bin/ruff format src/ tests/

test: test-py test-bash

test-py:
	$(PYTHON) -m pytest tests/ --ignore=tests/bash -v

test-bash:
	libs/bats/bin/bats tests/bash/install.bats
