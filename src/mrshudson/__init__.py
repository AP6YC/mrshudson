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

from typing import (
    List,
    Callable,
    TypeAlias,
)

# -----------------------------------------------------------------------------
# EXTERNAL DEPENDENCIES
# -----------------------------------------------------------------------------

# import yaml
# from multimethod import multimethod

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
        """Initializes the project state with the :func:`~default_projectdir` function and an unset.
        """

        self.projectdir: Path = self.default_projectdir()
        """The project directory.
        """

        self.projectdir_was_set: bool = False
        """A flag for if the projectdir was manually set.

        If low, the default the :func:`~default_projectdir` function is used to get the current :attr:`~ProjectState.projectdir`.
        """
        return

    def default_projectdir(self):
        """Generates the default projectdir directory as the current working directory at runtime.
        """

        return Path(os.getcwd())

    def set_projectdir(self, new_projectdir: Path):
        """Sets the projectdir from the provided path.

        This function also informs the :attr:`~project_was_set` asdf.

        Args:
            new_projectdir (Path): the new `pathlib.Path` that points to the correct project directory.
        """

        self.projectdir = new_projectdir
        self.projectdir_was_set = True

        return

    def get_projectdir(self):
        """Returns the current top-level project directory.

        If the value is manually set, it returns :attr:`~ProjectState.projectdir`.
        Otherwise, the :func:`~default_projectdir` is generated at runtime depending on the current context.
        """

        if self.projectdir_was_set:
            return self.projectdir
        else:
            return self.default_projectdir()

# -----------------------------------------------------------------------------
# GLOBAL CONSTANTS
# -----------------------------------------------------------------------------


globalprojectstate = ProjectState()
"""The default project state that is used when mrshudson directory functions.
"""

# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------


def set_projectdir(
    project_name: str,
    project_state: ProjectState = globalprojectstate,
):
    """Sets the top projectdir location for all future calls in this session.

    This function takes the name of the project and searches upwards for the location of that directory to set it as the current projectdir that is returned when calling :func:`~projectdir`.

    This function assumes two things: firstly that the current working directory of the callee (e.g., script, notebook, etc.) is at or below the directory, and secondly that the provided directory name exists in the first place.

    Args:
        project_name (str): the name of the directory that is at or above of the current working directory to set as the value that is returned when calling :func:`~projectdir`.
    """
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


def docstring_parameter(*sub):
    def dec(obj):
        obj.__doc__ = obj.__doc__.format(*sub)
        return obj
    return dec


ARGS_ARG = """

Args:
    *args: the subdirectories/files to join to the path.
"""


@docstring_parameter(ARGS_ARG)
def projectdir(*args) -> Path:
    """Returns the top project directory with optional added path parts.
    {0}
    """

    return get_project_root().joinpath(*args)


LAYOUT = constants.DEFAULT_LAYOUT


@docstring_parameter(ARGS_ARG)
def plotsdir(*args) -> Path:
    """Returns the DrWatson-like plots directory.
    {0}
    """

    return projectdir(LAYOUT["plots_dir"], *args)


@docstring_parameter(ARGS_ARG)
def papersdir(*args) -> Path:
    """Returns the DrWatson-like papers directory.
    {0}
    """

    return projectdir(LAYOUT["papers_dir"], *args)


@docstring_parameter(ARGS_ARG)
def srcdir(*args) -> Path:
    """Returns the DrWatson-like source directory.
    {0}
    """

    return projectdir(LAYOUT["src_dir"], *args)


@docstring_parameter(ARGS_ARG)
def scriptsdir(*args) -> Path:
    """Returns the DrWatson-like scripts directory.
    {0}
    """

    return projectdir(LAYOUT["scripts_dir"], *args)


@docstring_parameter(ARGS_ARG)
def optsdir(*args) -> Path:
    """Returns the DrWatson-like options directory.
    {0}
    """

    return projectdir(LAYOUT["opts_dir"], *args)


@docstring_parameter(ARGS_ARG)
def modelsdir(*args) -> Path:
    """Returns the DrWatson-like models directory.
    {0}
    """

    return projectdir(LAYOUT["models_dir"], *args)


@docstring_parameter(ARGS_ARG)
def notebooksdir(*args) -> Path:
    """Returns the DrWatson-like notebooks directory.
    {0}
    """

    return projectdir(LAYOUT["notebooks_dir"], *args)


@docstring_parameter(ARGS_ARG)
def datadir(*args) -> Path:
    """Returns the DrWatson-like data directory.
    {0}
    """

    return projectdir(LAYOUT["data_dir"], *args)


@docstring_parameter(ARGS_ARG)
def datadir_raw(*args) -> Path:
    """Returns the DrWatson-like raw data directory.
    {0}
    """

    return projectdir(LAYOUT["data_dir_raw"], *args)


@docstring_parameter(ARGS_ARG)
def datadir_pro(*args) -> Path:
    """Returns the DrWatson-like processed data directory.
    {0}
    """

    return projectdir(LAYOUT["data_dir_pro"], *args)


@docstring_parameter(ARGS_ARG)
def datadir_sims(*args) -> Path:
    """Returns the DrWatson-like simulations data directory.
    {0}
    """

    return projectdir(LAYOUT["data_dir_sims"], *args)


def initialize_project(
    layout=constants.DEFAULT_LAYOUT
):
    """Initializes a new mrshudon project from the provided project layout dictionary.

    Args:
        layout=constants.DEFAULT_LAYOUT
    """

    # For each
    for key, local_path in layout.items():
        lg.info(f"Making directory: {key} at {local_path}")
        # projectdir(local_path).mkdir(parents=True, exist_ok=True)
        projectdir(Path(local_path)).mkdir(parents=True, exist_ok=True)

    return


TypeDirFuncs: TypeAlias = List[Callable]


DIRFUNCS: TypeDirFuncs = [
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
