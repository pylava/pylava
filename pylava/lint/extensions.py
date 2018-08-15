"""Load extensions."""

LINTERS = {}

try:
    from pylava.lint.pylava_mccabe import Linter
    LINTERS['mccabe'] = Linter()
except ImportError:
    pass

try:
    from pylava.lint.pylava_pydocstyle import Linter
    LINTERS['pep257'] = Linter()  # for compatibility
    LINTERS['pydocstyle'] = Linter()
except ImportError:
    pass

try:
    from pylava.lint.pylava_pycodestyle import Linter
    LINTERS['pep8'] = Linter()  # for compability
    LINTERS['pycodestyle'] = Linter()
except ImportError:
    pass

try:
    from pylava.lint.pylava_pyflakes import Linter
    LINTERS['pyflakes'] = Linter()
except ImportError:
    pass

try:
    from pylava.lint.pylava_radon import Linter
    LINTERS['radon'] = Linter()
except ImportError:
    pass


from pkg_resources import iter_entry_points

for entry in iter_entry_points('pylava.linter'):
    if entry.name not in LINTERS:
        try:
            LINTERS[entry.name] = entry.load()()
        except ImportError:
            pass

#  pylava:ignore=E0611
