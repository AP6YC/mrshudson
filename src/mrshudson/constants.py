"""
    constants.py

This file contains constant values for the Python components of the DeepClustering project.
"""

from pathlib import Path

# --------------------------------------------------------------------------- #
# DEFAULTS
# --------------------------------------------------------------------------- #

DEFAULT_LAYOUT_FILE = 'layout.yml'

DEFAULT_FEATURE_FILE = 'features.yml'

DEFAULT_LAYOUT = {
    "plots_dir": Path("plots"),
    "papers_dir": Path("papers"),
    "scripts_dir": Path("scripts"),
    "src_dir": Path("src"),
    "opts_dir": Path("opts"),
    "data_dir": Path("data"),
    "data_dir_raw": Path("data").joinpath("exp_raw"),
    "data_dir_pro": Path("data").joinpath("exp_pro"),
    "data_dir_sims": Path("data").joinpath("sims"),
}

# DEFAULT_LAYOUT = {
#     "plots_dir": "plots",
#     "papers_dir": "papers",
#     "scripts_dir": "scripts",
#     "src_dir": "src",
#     "opts_dir": "opts",
#     "data_dir": "data",
#     "data_dir_raw": "data/exp_raw",
#     "data_dir_pro": "data/exp_pro",
#     "data_dir_sims": "data/sims",
# }

# DEFAULT_TEMPLATE = [
#   "_research",
#   "src",
#   "scripts",
#   "plots",
#   "notebooks",
#   "papers",
#   "data" => ["sims", "exp_raw", "exp_pro"],
# ]
