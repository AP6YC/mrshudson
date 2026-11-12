# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'mrshudson'
copyright = '2024, Sasha Petrenko'
author = 'Sasha Petrenko'
release = '0.1.0-alpha.1'
version = '0.1.0-alpha.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# extensions = []
extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    # 'sphinx_rtd_dark_mode',
    # 'sphinx_autopackagesummary',
]

# default_dark_mode = False

autosummary_generate_overwrite = True

autodoc_inherit_docstrings = True

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}

intersphinx_disabled_domains = ['std']


templates_path = ['_templates']
exclude_patterns = ['_autosummary']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
# html_theme = 'sphinx_rtd_theme'
html_theme = 'furo'

html_static_path = []

# -- Options for EPUB output
epub_show_urls = 'footnote'

# # Skip param objects because of their weird rendering in docs
# def maybe_skip_member(app, what, name, obj, skip, options):
#     # print app, what, name, obj, skip, options
#     # if name == ""
#     return True

# def setup(app):
#     app.connect('autodoc-skip-member', maybe_skip_member)
