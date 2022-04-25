BIN = ./venv/bin

LOCALIZER = sphinx-intl
DOCBUILDER = sphinx-build
TYPECHECKER = pyright
UNITTESTER = tox
PUBLISHER = twine
LOCALES = $(shell ls -1 doc/locale )

install: venv
	$(BIN)/pip3 install .

typecheck: venv
	. $(BIN)/activate && $(TYPECHECKER) cpanel/*.py test/*.py

test: venv
	@test -f test/cpanelrc.test || ( echo "Missing test configuration file test/cpanelrc.test" && exit 1 )
	$(BIN)/cpanel version
	$(BIN)/$(UNITTESTER)

package: venv
	rm -f dist/*
	$(BIN)/python3 -m build

doc: venv doc/build/gettext doc/reference.rst
	$(BIN)/$(DOCBUILDER) -b html doc doc/build/html/en
	$(foreach iso,$(LOCALES),$(BIN)/$(DOCBUILDER) -b html -D language=$(iso) doc doc/build/html/$(iso);)

publish: venv
	$(BIN)/$(PUBLISHER) upload dist/*

venv:
	python3 -m venv venv
	$(BIN)/pip3 install -r requirements-dev.txt

doc/build/gettext: venv install
	$(BIN)/$(DOCBUILDER) -b gettext doc doc/build/gettext

doc/reference.rst: cpanel/REFERENCE cpanel/USAGE
	bash ./doc/reference.sh $< doc/reference

locale: doc/build/gettext
	$(BIN)/$(LOCALIZER) -c doc/conf.py update -p doc/build/gettext -l $(iso)

clean:
	rm -rf venv build doc/build $$( find doc/locale/ -name *.mo ) *.egg-info .tox dist */__pycache__

.PHONY: install doc typecheck test package publish locale clean
