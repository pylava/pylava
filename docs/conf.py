# -*- coding: utf-8 -*-
import os
import sys
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath('.')))

from pylava import __version__ as release

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx']
source_suffix = '.rst'
master_doc = 'index'
project = 'Pylava'
copyright = '%s, Pylava Developers' % datetime.datetime.now().year
version = '.'.join(release.split('.')[:2])
exclude_patterns = ['_build']
html_use_modindex = False
html_show_sphinx = False
htmlhelp_basename = 'Pylavadoc'
latex_documents = [
    ('index', 'Pylava.tex', 'Pylava Documentation', 'Pylava Developers', 'manual'),
]
latex_use_modindex = False
latex_use_parts = True
man_pages = [
    ('index', 'Pylava', 'Pylava Documentation', ['Pylava Developers'], 1)
]
pygments_style = 'tango'
html_theme = 'default'
html_theme_options = {}

# lint_ignore=W0622
