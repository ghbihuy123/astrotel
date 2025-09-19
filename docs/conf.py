# conf.py

# -- Path setup --------------------------------------------------------------

import os
import sys
sys.path.insert(0, os.path.abspath('..'))  # add your project root to sys.path if needed


# -- Project information -----------------------------------------------------

project = 'Astrotel'
copyright = '2025, Luu Quang Huy'
author = 'Luu Quang Huy'

# The full version, including alpha/beta/rc tags
release = '0.1.0'


# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',    # for automatic documentation from docstrings
    'sphinx.ext.napoleon',   # for Google style docstrings
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

master_doc = "index"
# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'  # you can also use 'sphinx_rtd_theme' if installed
html_static_path = ['_static']
