# MAKE files requires tab as indent, don't replace them with spaces

lint:
	pylint pyedbglib

develop:
	pip install -e .[dev]

develop-end:
	pip uninstall pyedbglib

build:
	python setup.py bdist_wheel