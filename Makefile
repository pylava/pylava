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
# target: release - Bump version
release:
	@pip install bumpversion
	@bumpversion $(VERSION)
	@git checkout master
	@git push
	@git push --tags

.PHONY: major
major:
	make release VERSION=major

.PHONY: minor
minor:
	make release VERSION=minor

.PHONY: patch
patch:
	make release VERSION=patch

# ===============
#  Build package
# ===============

.PHONY: upload
# target: upload - Upload module on PyPI
upload: clean
	@pip install twine wheel
	@python setup.py sdist bdist_wheel
	@twine upload dist/* || true

.PHONY: test-upload
# target: test-upload - Upload module on Test PyPI
test-upload: clean
	@pip install twine wheel
	@python setup.py sdist bdist_wheel
	@twine upload --repository-url https://test.pypi.org/legacy/ dist/* || true

# =============
#  Development
# =============

.PHONY: venv
venv:
	python3 -m venv ~/.venv/pylava
	echo . ~/.venv/pylava/bin/activate > venv
	. ./venv && pip install -r requirements.txt
	. ./venv && pip install -r requirements-test.txt
	@echo
	@echo "To activate virtual environment, enter this command:"
	@echo
	@echo "    . venv"
	@echo

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
