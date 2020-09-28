Developer Notes
===============

This document contains notes that may be useful to developers and
release operators of Pylava.


Release Checklist
-----------------

- Update CHANGES.rst and commit it.

- Activate virtual environment for project development, if any.

- Enter the following command to run tests: ::

    make venv
    . venv
    make test

- Create and upload a new release to PyPI.

  If it's a backwards-incompatible update, enter this command: ::

    make major

  If it's a backwards-compatible update with new functionality, enter
  this command: ::

    make minor

  If it's a backwards-compatible bug-fix, enter this command: ::

    make patch

- Test release upload on Test PyPI with this command: ::

    make test-upload

- Visit https://test.pypi.org/project/pylava/ to check the test release.

- Upload new release on PyPI with this command: ::

    make upload

- Visit https://pypi.org/project/pylava/ to check the new release.
