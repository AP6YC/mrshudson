"""
mrshudson - a Python scientific project assistant package.
"""

# -----------------------------------------------------------------------------
# STDLIB IMPORTS
# -----------------------------------------------------------------------------

import os
from pathlib import Path
import logging as lg
import warnings

# -----------------------------------------------------------------------------
# EXTERNAL DEPENDENCY IMPORTS
# -----------------------------------------------------------------------------

from typing_extensions import (
    List,
    Callable,
    TypeAlias,
    Dict,
)

# -----------------------------------------------------------------------------
# LOCAL IMPORTS
# -----------------------------------------------------------------------------

# from . import constants

# -----------------------------------------------------------------------------
# PACKAGE ATTRIBUTES
# -----------------------------------------------------------------------------

__version__ = "0.1.0-alpha.1"

# -----------------------------------------------------------------------------
# TYPE ALIASES
# -----------------------------------------------------------------------------

TypeLayout: TypeAlias = Dict[str, str]
"""TypeAlias: A type alias for the layout of a project.
"""     # pylint: disable=W0105

TypeDirFuncs: TypeAlias = List[Callable]
"""TypeAlias: A type alias for the list of directory functions.
"""

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
"""TypeLayout: The default :mod:`mrshudson` project layout.
"""     # pylint: disable=W0105

# -----------------------------------------------------------------------------
# CLASSES
# -----------------------------------------------------------------------------


class ProjectState():

    def __init__(self):
        """Initializes the project state with the :func:`~default_projectdir` function and an unset.
        """

        self.projectdir: Path = self._default_projectdir()
        """The project directory.
        """

        self.projectdir_was_set: bool = False
        """A flag for if the projectdir was manually set.

        If low, the default the :func:`~default_projectdir` function is used to get the current :attr:`~ProjectState.projectdir`.
        """

        self.layout: TypeLayout = DEFAULT_LAYOUT
        """The layout of the project directory structure.

        This is used both for instantiating a project and for pointing to the correct locations when using the directory functions.
        """

        return

    def _default_projectdir(self):
        """Generates the default projectdir directory as the current working directory at runtime.
        """

        return Path(os.getcwd())

    def _set_projectdir(self, new_projectdir: Path):
        """Sets the projectdir from the provided path.

        This function also informs the :attr:`~project_was_set` attribute that the :attr:`~ProjectState.projectdir`. was set.

        Args:
            new_projectdir (Path): the new `pathlib.Path` that points to new :attr:`~ProjectState.projectdir` to use.
        """

        # Set the project directory to the provided path
        self.projectdir = new_projectdir

        # Tell the module that the directory was manually set
        self.projectdir_was_set = True

        return

    def _get_projectdir(self):
        """Returns the current top-level project directory.

        If the value is manually set, it returns :attr:`~ProjectState.projectdir`.
        Otherwise, the :func:`~default_projectdir` is generated at runtime depending on the current context.
        """

        if self.projectdir_was_set:
            return self.projectdir
        else:
            return self._default_projectdir()


# -----------------------------------------------------------------------------
# GLOBAL CONSTANTS
# -----------------------------------------------------------------------------


globalprojectstate: ProjectState = ProjectState()
"""ProjectState: The default project state that is used when mrshudson directory functions.
"""


# DEFAULT_LAYOUT_FILE: str = "layout.yml"
# """The location of the default layout file
# """     # pylint: disable=W0105


# LAYOUT = constants.DEFAULT_LAYOUT
# LAYOUT = DEFAULT_LAYOUT

_ARG_ARGS = """
    *args: the subdirectories/files to join to the path.
"""

_ARG_PROJECT_STATE = """
    project_state (ProjectState, optional): The stateful representation of the project structure to use. Defaults to globalprojectstate
"""

_ARG_ARGS_PROJECT_STATE = f"""
Args:
    {_ARG_ARGS}
    {_ARG_PROJECT_STATE}
"""


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


# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------

def _docstring_parameter(*sub):
    def dec(obj):
        obj.__doc__ = obj.__doc__.format(*sub)
        return obj
    return dec


@_docstring_parameter(_ARG_PROJECT_STATE)
def set_projectdir(
    project_name: str,
    project_state: ProjectState = globalprojectstate,
):
    """Sets the top projectdir location for all future calls in this session.

    This function takes the name of the project and searches upwards for the location of that directory to set it as the current projectdir that is returned when calling :func:`~projectdir`.

    This function assumes two things: firstly that the current working directory of the callee (e.g., script, notebook, etc.) is at or below the directory, and secondly that the provided directory name exists in the first place.

    Args:
        project_name (str): the name of the directory that is at or above of the current working directory to set as the value that is returned when calling :func:`~projectdir`.
        {0}
    """

    # Initiate the local directory for searching up
    local_dir = project_state._default_projectdir()
    local_projectname = project_name

    # If the name is in the path parts, set the projectdir to the
    if local_projectname in local_dir.parts:
        # Get the index of the dir
        index = local_dir.parts.index(local_projectname)
        # Recombine the path up to the index
        local_parts = local_dir.parts[0:index+1]
        # Set the project state's top dir to the recombined path
        # project_state.projectdir = Path(*local_parts)
        project_state._set_projectdir(Path(*local_parts))
    else:
        warnings.warn("The provided project name is not a parent of the current working directory.")

    return


# def _get_project_root(project_state: ProjectState = globalprojectstate) -> Path:
#     """Returns the top project directory from the project state.
#     """
#     return project_state._get_projectdir()


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def projectdir(
    *args,
    project_state: ProjectState = globalprojectstate,
) -> Path:
    """Returns the top project directory with optional added path parts.
    {0}
    """

    # return _get_project_root(project_state).joinpath(*args)
    return project_state._get_projectdir().joinpath(*args)


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def plotsdir(
    *args,
    project_state: ProjectState = globalprojectstate,
) -> Path:
    """Returns the DrWatson-like plots directory.
    {0}
    """

    return projectdir(project_state.layout["plots_dir"], *args)


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def papersdir(
    *args,
    project_state: ProjectState = globalprojectstate,
) -> Path:
    """Returns the DrWatson-like papers directory.
    {0}
    """

    return projectdir(project_state.layout["papers_dir"], *args)


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def srcdir(
    *args,
    project_state: ProjectState = globalprojectstate,
) -> Path:
    """Returns the DrWatson-like source directory.
    {0}
    """

    return projectdir(project_state.layout["src_dir"], *args)


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def scriptsdir(
    *args,
    project_state: ProjectState = globalprojectstate,
) -> Path:
    """Returns the DrWatson-like scripts directory.
    {0}
    """

    return projectdir(project_state.layout["scripts_dir"], *args)


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def optsdir(
    *args,
    project_state: ProjectState = globalprojectstate,
) -> Path:
    """Returns the DrWatson-like options directory.
    {0}
    """

    return projectdir(project_state.layout["opts_dir"], *args)


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def modelsdir(
    *args,
    project_state: ProjectState = globalprojectstate,
) -> Path:
    """Returns the DrWatson-like models directory.
    {0}
    """

    return projectdir(project_state.layout["models_dir"], *args)


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def notebooksdir(
    *args,
    project_state: ProjectState = globalprojectstate,
) -> Path:
    """Returns the DrWatson-like notebooks directory.
    {0}
    """

    return projectdir(project_state.layout["notebooks_dir"], *args)


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def datadir(
    *args,
    project_state: ProjectState = globalprojectstate,
) -> Path:
    """Returns the DrWatson-like data directory.
    {0}
    """

    return projectdir(project_state.layout["data_dir"], *args)


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def datadir_raw(
    *args,
    project_state: ProjectState = globalprojectstate,
) -> Path:
    """Returns the DrWatson-like raw data directory.
    {0}
    """

    return projectdir(project_state.layout["data_dir_raw"], *args)


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def datadir_pro(
    *args,
    project_state: ProjectState = globalprojectstate,
) -> Path:
    """Returns the DrWatson-like processed data directory.
    {0}
    """

    return projectdir(project_state.layout["data_dir_pro"], *args)


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def datadir_sims(
    *args,
    project_state: ProjectState = globalprojectstate,
) -> Path:
    """Returns the DrWatson-like simulations data directory.
    {0}
    """

    return projectdir(project_state.layout["data_dir_sims"], *args)


def initialize_project(
    # layout=DEFAULT_LAYOUT
    project_state: ProjectState = globalprojectstate,
):
    """Initializes a new mrshudon project from the provided project layout dictionary.
    """

    # For each
    for key, local_path in project_state.layout.items():
        lg.info(f"Making directory: {key} at {local_path}")
        # projectdir(local_path).mkdir(parents=True, exist_ok=True)
        projectdir(Path(local_path)).mkdir(parents=True, exist_ok=True)

    return


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


__all__ = [
    "ProjectState",
    "set_projectdir",
    "initialize_project",
    "projectdir",
    "plotsdir",
    "papersdir",
    "srcdir",
    "scriptsdir",
    "optsdir",
    "modelsdir",
    "datadir",
    "datadir_raw",
    "datadir_pro",
    "datadir_sims",
]
