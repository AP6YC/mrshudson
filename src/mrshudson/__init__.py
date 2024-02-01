"""
mrshudson - a Python scientific project assistant package.
"""

__version__ = "0.1.0-alpha.1"

# from .lib import *

"""
    lib.py

mrshudson's utility functions.
"""

# -----------------------------------------------------------------------------
# STDLIB IMPORTS
# -----------------------------------------------------------------------------

import os
from pathlib import Path
import logging as lg

# -----------------------------------------------------------------------------
# EXTERNAL DEPENDENCIES
# -----------------------------------------------------------------------------

import yaml
from multimethod import multimethod

# -----------------------------------------------------------------------------
# LOCAL IMPORTS
# -----------------------------------------------------------------------------

# import src.python.constants as cs
from . import constants

# -----------------------------------------------------------------------------
# CLASSES
# -----------------------------------------------------------------------------


class ProjectState():

    def __init__(self):
        self.projectdir: Path = Path(os.getcwd())
        return

# -----------------------------------------------------------------------------
# GLOBAL CONSTANTS
# -----------------------------------------------------------------------------


globalprojectstate = ProjectState()

# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------

# def test_print():
#     lg.warning("bbbbb")
#     return

# @multimethod
def set_projectdir(
    project_name: str,
    project_state: ProjectState = globalprojectstate,
):
    # Initiate the local directory for searching up
    local_dir = Path(os.getcwd())
    local_projectname = project_name

    # lg.warning(f"local dir: {local_dir}")
    # lg.warning(f"parts: {local_dir.parts}")
    # lg.warning(f"project name: {local_projectname}")

    # If the name is in the path parts, set the projectdir to the
    if local_projectname in local_dir.parts:
        # Get the index of the dir
        index = local_dir.parts.index(local_projectname)
        # Recombine the path up to the index
        local_parts = local_dir.parts[0:index+1]
        # Set the project state's top dir to the recombined path
        project_state.projectdir = Path(*local_parts)
    else:
        raise Warning("The provided project name is not a parent of the current working directory.")

    # lg.warning(f"new projectdir: {project_state.projectdir}")

    return


def get_methods(my_class):
    """
    Gets the non-wrangled methods and members of a class.
    """
    method_list = [method for method in dir(my_class) if method.startswith('__') is False]
    return method_list


def print_methods(my_class):
    """
    Prints the non-wrangled methods and members of a class.
    """
    print(get_methods(my_class))


def get_project_root(project_state: ProjectState = globalprojectstate) -> Path:
    """Returns the top project directory from the project state.
    """

    # return Path(__file__).resolve().parent.parent.parent
    # return Path(os.getcwd())
    return project_state.projectdir


def projectdir(*args) -> Path:
    """Returns the top project directory with optional added path parts.
    """

    return get_project_root().joinpath(*args)


def load_layout(layout_file):
    """Loads and returns the provided YAML project layout file.
    """

    try:
        with open(layout_file, 'r') as file:
            layout = yaml.safe_load(file)
    except Exception:
        lg.warning("Could not open layout file, loading default layout.")
        layout = constants.DEFAULT_LAYOUT

    return layout


# LAYOUT = load_layout(projectdir(constants.DEFAULT_LAYOUT_FILE))
LAYOUT = constants.DEFAULT_LAYOUT


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
    """Takes DrWatson-like directory functions and returns subdirectory functions with `dest_name`.
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


def initialize_project():
    """
    Initializes a new mrshudon project
    """

    for key, local_path in constants.DEFAULT_LAYOUT.items():
        lg.info(f"Making directory: {key}")
        projectdir().joinpath(local_path).mkdir(parents=True, exist_ok=True)
