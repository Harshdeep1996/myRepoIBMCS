# -*- mode:makefile; coding:utf-8 -*-

.PHONY: all unit-tests lint flake8 accreditation clean doc

all: lint unit-tests
	@echo "Nothing done for all"

lint: flake8

flake8:
	$@ compliance

accreditation:
	PYTHONPATH=$(shell pwd) ACCREDITATION=$(ACCREDITATION) \
		python compliance --with-ControlValidation

unit-tests:
	PYTHONPATH=$(shell pwd) nosetests -v test

unit-tests-with-coverage:
	PYTHONPATH="." nosetests --cover-branches --with-coverage \
		--cover-package=compliance.utils -v test

test-reports:
	$(RM) -r reports/html
	mkdir -p reports/html
	PYTHONPATH="." nosetests --cover-erase --cover-html \
		--cover-html-dir=reports/html --cover-branches \
		--with-coverage --cover-package=compliance.utils test

doc:
	sphinx-apidoc -o doc . --separate --force setup.py
	make -C doc html

clean:
	$(RM) $(shell find . -name "*~") $(shell find . -name "*.pyc")
	$(RM) results.json
	make -C doc clean

clean-all: clean
	$(RM) -r reports .coverage
