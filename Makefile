BIN = ./venv/bin

DOCBUILDER = sphinx-build
TYPECHECKER = pyright
UNITTESTER = tox
PUBLISHER = twine

local: venv
	$(BIN)/pip3 install .

doc: venv
	$(BIN)/$(DOCBUILDER) -b html doc doc/build

typecheck: venv
	. $(BIN)/activate && $(TYPECHECKER) cpanel/*.py test/*.py

test: venv
	$(BIN)/cpanel version
	$(BIN)/$(UNITTESTER)

package: venv
	rm -f dist/*
	$(BIN)/python3 -m build

publish: venv
	$(BIN)/$(PUBLISHER) upload dist/*

venv:
	python3 -m venv venv
	$(BIN)/pip3 install -r requirements-dev.txt

clean:
	rm -rf venv build doc/build *.egg-info .tox dist

.PHONY: local doc typecheck test package publish clean
