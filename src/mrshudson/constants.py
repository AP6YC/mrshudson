"""
    constants.py

This file contains constant values for the Python components of the DeepClustering project.
"""

from pathlib import Path

from typing import Dict

# --------------------------------------------------------------------------- #
# DEFAULTS
# --------------------------------------------------------------------------- #

DEFAULT_LAYOUT_FILE = 'layout.yml'
"""The location of the default layout file
"""     # pylint: disable=W0105

TYPE_LAYOUT = Dict[str, Path]

DEFAULT_LAYOUT: TYPE_LAYOUT = {
    "plots_dir": Path("plots"),
    "papers_dir": Path("papers"),
    "scripts_dir": Path("scripts"),
    "src_dir": Path("src"),
    "opts_dir": Path("opts"),
    "data_dir": Path("data"),
    "models_dir": Path("models"),
    "notebooks_dir": Path("notebooks"),
    "data_dir_raw": Path("data", "exp_raw"),
    "data_dir_pro": Path("data", "exp_pro"),
    "data_dir_sims": Path("data", "sims"),
}
"""The default mrshudson project layout.
"""     # pylint: disable=W0105

# DEFAULT_TEMPLATE = [
#   "_research",
#   "src",
#   "scripts",
#   "plots",
#   "notebooks",
#   "papers",
#   "data" => ["sims", "exp_raw", "exp_pro"],
# ]
