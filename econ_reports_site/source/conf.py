# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import plotly.io as pio
import sphinx_material

pio.renderers.default = "browser"

# release = "0.1.0"

project = "econ_reports"
copyright = "2022, Greg Moore"
author = "Greg Moore"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "nbsphinx",
]

nbsphinx_execute = "never"

templates_path = ["_templates"]

# Material theme options
extensions.append("sphinx_material")
html_theme_path = sphinx_material.html_theme_path()
html_context = sphinx_material.get_html_context()
html_theme = "sphinx_material"
html_show_sourcelink = False
html_sidebars = {"**": ["logo-text.html", "globaltoc.html", "searchbox.html"]}
html_theme_options = {
    # "base_url": "",
    "repo_url": "https://github.com/gw-moore/econ_reports/",
    "repo_name": project,
    "repo_type": "github",
    "nav_title": f"{project}",
    # "nav_links": [
    #     {
    #         "href": "index",
    #         "title": project,
    #         "internal": True,
    #     }
    # ],
    "color_primary": "blue",
    "color_accent": "blue",
    "globaltoc_depth": 2,
    "globaltoc_collapse": True,
    "master_doc": False,
    "heroes": {
        "index": "Econ Reports",
    },
    # setting the logo icon so as to not have broken element on the page
    # considering adding a custom svg to the project and assigning it to 'html_logo'
    "logo_icon": "&#xE1AF",
}

html_static_path = ["_static"]
templates_path = ["_templates"]
exclude_patterns = ["build", "Thumbs.db", ".DS_Store"]
