# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------

project = "arrangeit"
copyright = "1999-2019, Ivica Paleka"
author = "Ivica Paleka"

# The full version, including alpha/beta/rc tags
from arrangeit import __version__

release = __version__

# -- General configuration ---------------------------------------------------

master_doc = "index"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.autodoc"]

# mocks by Sphinx so autodoc of all modules is possible from GNU/Linux
autodoc_mock_imports = [
    "AppKit",
    "Quartz",
    "win32api",
    "win32gui",
    "win32ui",
    "PIL.ImageGrab",
    "comtypes",
    "pynput",
    "Xlib",
]

# custom mocks so autodoc of all modules is possible from GNU/Linux
from unittest.mock import Mock


class MockedObject(Mock):
    USHORT = 0
    DWORD = 0
    RECT = 0
    UINT = 0
    ATOM = 0
    WS_EX_NOACTIVATE = 0
    WS_EX_TOOLWINDOW = 0
    STATE_SYSTEM_INVISIBLE = 0
    WS_THICKFRAME = 0
    BaseTrust = 0
    PartialTrust = 0
    HIDDEN = 0
    MINIMIZED = 0
    X = 0
    Y = 0
    WIDTH = 0
    HEIGHT = 0


MOCK_MODULES = [
    "ctypes",
    "ctypes.wintypes",
    "win32con",
    "vdi.TrustLevel",
    "gi",
    "gi.repository",
    "gi.repository.Gdk",
    "gi.repository.Wnck",
]
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = MockedObject()

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#
html_logo = "_static/logo.png"
html_favicon = "_static/favicon.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# -- Options for LaTeX output ---------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    ("index", "arrangeit.tex", "arrangeit documentation", author, "howto")
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#
latex_logo = html_logo

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [("index", "arrangeit", "arrangeit documentation", [author], 1)]
