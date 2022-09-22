"""
    lib.py

mrshudson's utility functions.
"""

# --------------------------------------------------------------------------- #
# STANDARD IMPORTS
# --------------------------------------------------------------------------- #

from pathlib import Path
import logging

# --------------------------------------------------------------------------- #
# CUSTOM IMPORTS
# --------------------------------------------------------------------------- #

import yaml

# --------------------------------------------------------------------------- #
# LOCAL IMPORTS
# --------------------------------------------------------------------------- #

# import src.python.constants as cs
from . import constants

# --------------------------------------------------------------------------- #
# GLOBAL CONSTANTS
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# FUNCTIONS
# --------------------------------------------------------------------------- #

def get_project_root() -> Path:
    """Returns the top project directory.
    """

    return Path(__file__).resolve().parent.parent.parent

def projectdir(*args) -> Path:
    """Returns the DrWatson-like project directory.
    """

    return get_project_root().joinpath(*args)

def load_layout(layout_file):
    """Loads and returns the provided YAML project layout file.
    """

    try:
        with open(layout_file, 'r') as file:
            layout = yaml.safe_load(file)
    except:
        logging.warning("Could not open layout file, loading default layout.")
        layout = constants.DEFAULT_LAYOUT

    return layout

LAYOUT = load_layout(projectdir(constants.DEFAULT_LAYOUT_FILE))

def plotsdir(*args) -> Path:
    """Returns the DrWatson-like plots directory.
    """

    return projectdir().joinpath(LAYOUT["plots_dir"], *args)

def papersdir(*args) -> Path:
    """Returns the DrWatson-like papers directory.
    """

    return projectdir().joinpath(LAYOUT["papers_dir"], *args)

def srcdir(*args) -> Path:
    """Returns the DrWatson-like source directory.
    """

    return projectdir().joinpath(LAYOUT["src_dir"], *args)

def scriptsdir(*args) -> Path:
    """Returns the DrWatson-like scripts directory.
    """

    return projectdir().joinpath(LAYOUT["scripts_dir"], *args)

def optsdir(*args) -> Path:
    """Returns the DrWatson-like options directory.
    """

    return projectdir().joinpath(LAYOUT["opts_dir"], *args)

def modelsdir(*args) -> Path:
    """Returns the DrWatson-like models directory.
    """

    return projectdir().joinpath(LAYOUT["models_dir"], *args)

def datadir(*args) -> Path:
    """Returns the DrWatson-like data directory.
    """

    return projectdir().joinpath(LAYOUT["data_dir"], *args)

def datadir_raw(*args) -> Path:
    """Returns the DrWatson-like raw data directory.
    """

    return datadir(LAYOUT["data_dir_raw"], *args)

def datadir_pro(*args) -> Path:
    """Returns the DrWatson-like data directory.
    """

    return datadir(LAYOUT["data_dir_pro"], *args)

def datadir_sims(*args) -> Path:
    """Returns the DrWatson-like data directory.
    """

    return datadir(LAYOUT["data_dir_sims"], *args)

def dropboxdir(*args) -> Path:
    """Returns the DrWatson-like dropbox directory.
    """

    return projectdir().joinpath(LAYOUT["dropbox_dir"], *args)

def localize(dest_name, *args) -> tuple:
    """Takes DrWatson directory functions and returns subdirectory functions with `dest_name`.
    """

    return tuple((lambda *local_args, my_arg=arg: my_arg(dest_name, *local_args)) for arg in args)
    # funcs = []
    # for arg in args:
    #     funcs.append(lambda *local_args, my_arg=arg: my_arg(dest_name, *local_args))
    # return funcs

def localize_and_make(dest_name, *args) -> tuple:
    """Localize the directory functions to the `dest_name` and make the directories at the same time.
    """

    funcs = localize(dest_name, *args)
    for func in funcs:
        func().mkdir(parents=True, exist_ok=True)

    return funcs
