"""
    constants.py

This file contains constant values for the Python components of the DeepClustering project.
"""

from pathlib import Path

from typing import (
    Dict,
    TypeAlias,
)

# --------------------------------------------------------------------------- #
# DEFAULTS
# --------------------------------------------------------------------------- #


DEFAULT_LAYOUT_FILE = 'layout.yml'
"""The location of the default layout file
"""     # pylint: disable=W0105


TypeLayout: TypeAlias = Dict[str, str]
"""A type alias for the layout of a project.
"""     # pylint: disable=W0105


DEFAULT_LAYOUT: TypeLayout = {
    "plots_dir": "plots",
    "papers_dir": "papers",
    "scripts_dir": "scripts",
    "src_dir": "src",
    "opts_dir": "opts",
    "data_dir": "data",
    "models_dir": "models",
    "notebooks_dir": "notebooks",
    "data_dir_raw": "data/exp_raw",
    "data_dir_pro": "data/exp_pro",
    "data_dir_sims": "data/sims",
}
"""The default :mod:`~mrshudson` project layout.
"""     # pylint: disable=W0105


# TypeLayout: TypeAlias = Dict[str, Path]
# """A type alias for the layout of a project.
# """     # pylint: disable=W0105


# DEFAULT_LAYOUT: TypeLayout = {
#     "plots_dir": Path("plots",
#     "papers_dir": Path("papers"),
#     "scripts_dir": Path("scripts"),
#     "src_dir": Path("src"),
#     "opts_dir": Path("opts"),
#     "data_dir": Path("data"),
#     "models_dir": Path("models"),
#     "notebooks_dir": Path("notebooks"),
#     "data_dir_raw": Path("data", "exp_raw"),
#     "data_dir_pro": Path("data", "exp_pro"),
#     "data_dir_sims": Path("data", "sims"),
# }
# """The default mrshudson project layout.
# """     # pylint: disable=W0105

# DEFAULT_TEMPLATE = [
#   "_research",
#   "src",
#   "scripts",
#   "plots",
#   "notebooks",
#   "papers",
#   "data" => ["sims", "exp_raw", "exp_pro"],
# ]
