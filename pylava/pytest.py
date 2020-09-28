""" py.test plugin for checking files with pylava. """
from __future__ import absolute_import

from os import path as op

import py # noqa
import pytest


HISTKEY = "pylava/mtimes"


def pytest_load_initial_conftests(early_config, parser, args):
    # Marks have to be registered before usage
    # to not fail with --strict command line argument
    early_config.addinivalue_line(
        'markers',
        'pycodestyle: Mark test as using pylava code audit tool.')


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group.addoption(
        '--pylava', action='store_true',
        help="perform some pylava code checks on .py files")


def pytest_sessionstart(session):
    config = session.config
    if config.option.pylava and getattr(config, 'cache', None):
        config._pylavamtimes = config.cache.get(HISTKEY, {})


def pytest_sessionfinish(session):
    config = session.config
    if hasattr(config, "_pylavamtimes"):
        config.cache.set(HISTKEY, config._pylavamtimes)


def pytest_collect_file(path, parent):
    config = parent.config
    if config.option.pylava and path.ext == '.py':
        if hasattr(PylavaItem, "from_parent"):
            return PylavaItem.from_parent(parent=parent, path=path, fspath=path)
        return PylavaItem(path, parent)


class PylavaError(Exception):
    """ indicates an error during pylava checks. """


class PylavaItem(pytest.Item, pytest.File):

    def __init__(self, path, parent, fspath=None):
        super(PylavaItem, self).__init__(path, parent)
        self.add_marker("pycodestyle")
        self.cache = None
        self._pylavamtimes = None

    def setup(self):
        if not getattr(self.config, 'cache', None):
            return False

        self.cache = True
        self._pylavamtimes = self.fspath.mtime()
        pylavamtimes = self.config._pylavamtimes
        old = pylavamtimes.get(str(self.fspath), 0)
        if old == self._pylavamtimes:
            pytest.skip("file(s) previously passed Pylava checks")

    def runtest(self):
        errors = check_file(self.fspath)
        if errors:
            pattern = "%(filename)s:%(lnum)s:%(col)s: %(text)s"
            out = "\n".join([pattern % e._info for e in errors])
            raise PylavaError(out)

        # update mtime only if test passed
        # otherwise failures would not be re-run next time
        if self.cache:
            self.config._pylavamtimes[str(self.fspath)] = self._pylavamtimes

    def repr_failure(self, excinfo):
        if excinfo.errisinstance(PylavaError):
            return excinfo.value.args[0]
        return super(PylavaItem, self).repr_failure(excinfo)


def check_file(path):
    from pylava.main import parse_options, process_paths
    from pylava.config import CURDIR

    options = parse_options()
    path = op.relpath(str(path), CURDIR)
    return process_paths(options, candidates=[path], error=False)

# pylava:ignore=D,E1002,W0212,F0001
