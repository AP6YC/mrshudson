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
import warnings

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
        self.projectdir: Path = self.default_projectdir()
        self.projectdir_was_set: bool = False
        return

    def default_projectdir(self):
        return Path(os.getcwd())

    def set_projectdir(self, new_projectdir: Path):
        self.projectdir = new_projectdir
        self.projectdir_was_set = True

    def get_projectdir(self):
        if self.projectdir_was_set:
            return self.projectdir
        else:
            return self.default_projectdir()

# -----------------------------------------------------------------------------
# GLOBAL CONSTANTS
# -----------------------------------------------------------------------------


globalprojectstate = ProjectState()

# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------


# @multimethod
def set_projectdir(
    project_name: str,
    project_state: ProjectState = globalprojectstate,
):
    # Initiate the local directory for searching up
    local_dir = project_state.default_projectdir()
    local_projectname = project_name

    # If the name is in the path parts, set the projectdir to the
    if local_projectname in local_dir.parts:
        # Get the index of the dir
        index = local_dir.parts.index(local_projectname)
        # Recombine the path up to the index
        local_parts = local_dir.parts[0:index+1]
        # Set the project state's top dir to the recombined path
        project_state.projectdir = Path(*local_parts)
    else:
        warnings.warn("The provided project name is not a parent of the current working directory.")

    return


def get_project_root(project_state: ProjectState = globalprojectstate) -> Path:
    """Returns the top project directory from the project state.
    """

    return project_state.get_projectdir()


def projectdir(*args) -> Path:
    """Returns the top project directory with optional added path parts.
    """

    return get_project_root().joinpath(*args)


LAYOUT = constants.DEFAULT_LAYOUT


def plotsdir(*args) -> Path:
    """Returns the DrWatson-like plots directory.
    """

    return projectdir(LAYOUT["plots_dir"], *args)


def papersdir(*args) -> Path:
    """Returns the DrWatson-like papers directory.
    """

    return projectdir(LAYOUT["papers_dir"], *args)


def srcdir(*args) -> Path:
    """Returns the DrWatson-like source directory.
    """

    return projectdir(LAYOUT["src_dir"], *args)


def scriptsdir(*args) -> Path:
    """Returns the DrWatson-like scripts directory.
    """

    return projectdir(LAYOUT["scripts_dir"], *args)


def optsdir(*args) -> Path:
    """Returns the DrWatson-like options directory.
    """

    return projectdir(LAYOUT["opts_dir"], *args)


def modelsdir(*args) -> Path:
    """Returns the DrWatson-like models directory.
    """

    return projectdir(LAYOUT["models_dir"], *args)


def notebooksdir(*args) -> Path:
    """Returns the DrWatson-like notebooks directory.
    """

    return projectdir(LAYOUT["notebooks_dir"], *args)


def datadir(*args) -> Path:
    """Returns the DrWatson-like data directory.
    """

    return projectdir(LAYOUT["data_dir"], *args)


def datadir_raw(*args) -> Path:
    """Returns the DrWatson-like raw data directory.
    """

    return projectdir(LAYOUT["data_dir_raw"], *args)


def datadir_pro(*args) -> Path:
    """Returns the DrWatson-like processed data directory.
    """

    return projectdir(LAYOUT["data_dir_pro"], *args)


def datadir_sims(*args) -> Path:
    """Returns the DrWatson-like simulations data directory.
    """

    return projectdir(LAYOUT["data_dir_sims"], *args)


def initialize_project(layout=constants.DEFAULT_LAYOUT):
    """Initializes a new mrshudon project from the provided project layout dictionary.
    """

    for key, local_path in layout.items():
        lg.info(f"Making directory: {key} at {local_path}")
        projectdir(local_path).mkdir(parents=True, exist_ok=True)

    return


DIRFUNCS = [
    projectdir,
    plotsdir,
    papersdir,
    srcdir,
    scriptsdir,
    optsdir,
    modelsdir,
    datadir,
    datadir_raw,
    datadir_pro,
    datadir_sims,
]
"""A list of the functions in the mrshudson module that point to project directories.
"""     # pylint: disable=W0105
