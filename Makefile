BIN = ./venv/bin

LOCALIZER = sphinx-intl
DOCBUILDER = sphinx-build
TYPECHECKER = pyright
UNITTESTER = tox
PUBLISHER = twine
LOCALES = $(shell ls -1 doc/locale )
TAG = $(shell git describe --tags --always --abbrev=0)

install: venv dist
	$(BIN)/pip3 install dist/cpanel*.whl

typecheck: venv
	. $(BIN)/activate && $(TYPECHECKER) cpanel/*.py cpanel/caller/*.py test/*.py

test: venv dist
	@test -f test/cpanelrc.test || ( echo "Missing test configuration file test/cpanelrc.test" && exit 1 )
	$(BIN)/cpanel version
	$(BIN)/$(UNITTESTER)

package: venv
	rm -f dist/*
	. $(BIN)/activate && $(BIN)/python3 -m build --wheel --sdist

dist:
	$(MAKE) package

doc: venv doc/build/gettext doc/reference.rst
	$(BIN)/$(DOCBUILDER) -b html doc doc/build/html/en
	$(foreach iso,$(LOCALES),$(BIN)/$(DOCBUILDER) -b html -D language=$(iso) doc doc/build/html/$(iso);)

publish: venv
	$(BIN)/$(PUBLISHER) upload dist/*

venv:
	python3 -m venv venv
	$(BIN)/pip3 install .[dev]

doc/build/gettext: venv install
	$(BIN)/$(DOCBUILDER) -b gettext doc doc/build/gettext

doc/reference.rst: cpanel/REFERENCE cpanel/USAGE
	bash ./doc/reference.sh $< doc/reference

locale: doc/build/gettext
	$(BIN)/$(LOCALIZER) -c doc/conf.py update -p doc/build/gettext -l $(iso)

releases:
	gh release create $(TAG)

clean:
	rm -rf venv build doc/build $$( find doc/locale/ -name *.mo ) *.egg-info .tox dist */__pycache__ ./__pycache__

.PHONY: install doc typecheck test package publish locale releases clean
