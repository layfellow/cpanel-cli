BIN = ./venv/bin

LOCALIZER = sphinx-intl
DOCBUILDER = sphinx-build
TYPECHECKER = pyright
UNITTESTER = tox
PUBLISHER = twine

install: venv
	$(BIN)/pip3 install .

localize: venv install
	$(BIN)/$(DOCBUILDER) -b gettext doc doc/build/gettext
	$(BIN)/$(LOCALIZER) -c doc/conf.py update -p doc/build/gettext -l es

doc: venv
	$(BIN)/$(DOCBUILDER) -b html doc doc/build/html/en
	$(BIN)/$(DOCBUILDER) -b html -D language=es doc doc/build/html/es

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
	rm -rf venv build doc/build $$( find doc/locale/ -name *.mo ) *.egg-info .tox dist

.PHONY: install localize doc typecheck test package publish clean
