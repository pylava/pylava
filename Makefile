MODULE=pylava
SPHINXBUILD=sphinx-build
ALLSPHINXOPTS= -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .
BUILDDIR=_build

LIBSDIR=$(CURDIR)/libs

.PHONY: help
# target: help - Display callable targets
help:
	@egrep "^# target:" [Mm]akefile

.PHONY: clean
# target: clean - Clean repo
clean:
	@rm -rf build dist docs/_build *.egg
	@rm -rf .tox pylava.egg-info .pytest_cache
	@find . -name "*.pyc" -delete
	@find . -name "*.orig" -delete
	@rm -rf $(CURDIR)/libs

# ==============
#  Bump version
# ==============

.PHONY: release
VERSION?=minor
# target: release - Bump version
release:
	@pip install bumpversion
	@bumpversion $(VERSION)
	@git checkout master
	@git push
	@git push --tags

.PHONY: minor
minor: release

.PHONY: patch
patch:
	make release VERSION=patch

# ===============
#  Build package
# ===============

.PHONY: register
# target: register - Register module on PyPi
register:
	python setup.py register

.PHONY: upload
# target: upload - Upload module on PyPi
upload: clean
	@pip install twine wheel
	@python setup.py sdist bdist_wheel
	@twine upload dist/* || true

.PHONY: test-upload
test-upload: clean
	@pip install twine wheel
	@python setup.py sdist bdist_wheel
	@twine upload --repository-url https://test.pypi.org/legacy/ dist/* || true

# =============
#  Development
# =============

.PHONY: t
t test:
	@py.test --pylava pylava
	@py.test -sx test_pylava.py

.PHONY: audit
audit:
	@python -m "pylava.main"

.PHONY: docs
docs:
	@cd docs && sphinx-build -b html . _build/html
