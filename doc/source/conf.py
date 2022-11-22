# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../../sandbox'))

from typing import List, Dict, Tuple, Optional
import sphinx_rtd_theme  # pylint: disable=unused-import  # noqa:F401

# -- Project information -----------------------------------------------------

# the master toctree document
master_doc = "index"

project = 'django-book-manager'
copyright = '2022, Caltech IMSS ADS'  # pylint: disable=redefined-builtin
author = 'Caltech IMSS ADS'

# The full version, including alpha/beta/rc tags
release = '0.3.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx_rtd_theme',
    "sphinxcontrib_django2",
]

source_suffix = ".rst"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns: List[str] = ['_build']

add_function_parentheses = False
add_module_names = True

# Make Sphinx not expand all our Type Aliases

autodoc_member_order = 'groupwise'
autodoc_type_aliases = {
}

# the locations and names of other projects that should be linked to this one
intersphinx_mapping: Dict[str, Tuple[str, Optional[str]]] = {
    'python': ('https://docs.python.org/3', None),
    'django': ('http://docs.djangoproject.com/en/dev/', 'http://docs.djangoproject.com/en/dev/_objects/'),
}

# Configure the path to the Django settings module
django_settings = "demo.settings"
# Include the database table names of Django models
django_show_db_tables = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
#html_static_path = ['_static']

html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = True
