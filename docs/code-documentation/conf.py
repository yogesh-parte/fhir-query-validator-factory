"""Sphinx configuration for fhir-query-validator-factory."""

from __future__ import annotations

import os
import sys
from datetime import datetime

# -- Path setup --------------------------------------------------------------
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

# -- Project information -----------------------------------------------------
project = "fhir-query-validator-factory"
author = "Yogesh"
copyright = f"{datetime.now().year}, {author}"
release = "0.1.0"
version = "0.1"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "README.md"]

source_suffix = [".rst", ".md"]

master_doc = "index"
language = "en"

# -- Autodoc -----------------------------------------------------------------
autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "show-inheritance": True,
    "member-order": "bysource",
}
autodoc_typehints = "description"
autodoc_mock_imports = ["google.adk", "google.adk.agents", "google.adk.workflow"]
autosummary_generate = True
napoleon_google_docstring = True
napoleon_numpy_docstring = False

# -- Intersphinx -----------------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
}

# -- HTML theme --------------------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_title = "FHIR Query Validator Factory"
html_theme_options = {
    "navigation_depth": 4,
    "collapse_navigation": False,
}

# -- MyST (optional markdown includes) ---------------------------------------
myst_enable_extensions = ["colon_fence", "deflist"]
myst_heading_anchors = 3