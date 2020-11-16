# Copyright (C) 2019-2020 Richard Hughes <richard@hughsie.com>
# SPDX-License-Identifier: GPL-2.0+

VENV=./env
PYTHON=$(VENV)/bin/python
PYTEST=$(VENV)/bin/pytest
SPHINX_BUILD=$(VENV)/bin/sphinx-build
FLASK=$(VENV)/bin/flask
BLACK=$(VENV)/bin/black
FLAKE8=$(VENV)/bin/flake8
MYPY=$(VENV)/bin/mypy

setup:
	virtualenv ./env

clean:
	rm -rf ./build
	rm -rf ./htmlcov

docs:
	$(SPHINX_BUILD) docs build

blacken:
	find PyGnuTLS -name '*.py' -exec $(BLACK) {} \;

check: $(PYTEST)
	$(PYTEST)
	$(MYPY) PyGnuTLS
	$(FLAKE8)
