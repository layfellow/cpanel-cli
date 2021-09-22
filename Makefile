BIN = ./venv/bin

local: venv
	$(BIN)/pip3 install .

doc: venv
	$(BIN)/sphinx-build -b html doc doc/build

test: venv
	$(BIN)/cpanel version
	$(BIN)/tox

package: venv
	rm -f dist/*
	$(BIN)/python3 -m build

publish: venv
	$(BIN)/twine upload dist/*

venv:
	python3 -m venv venv
	$(BIN)/pip3 install -r requirements-dev.txt

clean:
	rm -rf venv build doc/build *.egg-info .tox dist

.PHONY: local doc test package publish publish.test clean
