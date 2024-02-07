"""All of the directory utilities for the `mrshudson` package.
"""

# --------------------------------------------------------------------------- #
# STDLIB IMPORTS
# --------------------------------------------------------------------------- #

from pathlib import Path
import logging as lg

# --------------------------------------------------------------------------- #
# EXTERNAL DEPENDENCY IMPORTS
# --------------------------------------------------------------------------- #

from typing_extensions import (
    TypeAlias,
    List,
    Callable,
)

# --------------------------------------------------------------------------- #
# LOCAL IMPORTS
# --------------------------------------------------------------------------- #

from ._utils import (
    _docstring_parameter,
    _ARG_ARGS_PROJECT_STATE,
    _ARG_PROJECT_STATE,
)

from .project import (
    ProjectState,
    DEFAULT_PROJECT_STATE,
)

# --------------------------------------------------------------------------- #
# FUNCTIONS
# --------------------------------------------------------------------------- #


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def projectdir(
    *args,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
) -> Path:
    """Returns the top project directory with optional added path parts.
    {0}
    """

    # return _get_project_root(project_state).joinpath(*args)
    return project_state._get_projectdir().joinpath(*args)


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def plotsdir(
    *args,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
) -> Path:
    """Returns the DrWatson-like plots directory.
    {0}
    """

    return projectdir(project_state.layout["plots_dir"], *args)


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def papersdir(
    *args,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
) -> Path:
    """Returns the DrWatson-like papers directory.
    {0}
    """

    return projectdir(project_state.layout["papers_dir"], *args)


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def srcdir(
    *args,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
) -> Path:
    """Returns the DrWatson-like source directory.
    {0}
    """

    return projectdir(project_state.layout["src_dir"], *args)


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def scriptsdir(
    *args,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
) -> Path:
    """Returns the DrWatson-like scripts directory.
    {0}
    """

    return projectdir(project_state.layout["scripts_dir"], *args)


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def optsdir(
    *args,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
) -> Path:
    """Returns the DrWatson-like options directory.
    {0}
    """

    return projectdir(project_state.layout["opts_dir"], *args)


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def modelsdir(
    *args,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
) -> Path:
    """Returns the DrWatson-like models directory.
    {0}
    """

    return projectdir(project_state.layout["models_dir"], *args)


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def notebooksdir(
    *args,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
) -> Path:
    """Returns the DrWatson-like notebooks directory.
    {0}
    """

    return projectdir(project_state.layout["notebooks_dir"], *args)


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def datadir(
    *args,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
) -> Path:
    """Returns the DrWatson-like data directory.
    {0}
    """

    return projectdir(project_state.layout["data_dir"], *args)


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def datadir_raw(
    *args,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
) -> Path:
    """Returns the DrWatson-like raw data directory.
    {0}
    """

    return projectdir(project_state.layout["data_dir_raw"], *args)


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def datadir_pro(
    *args,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
) -> Path:
    """Returns the DrWatson-like processed data directory.
    {0}
    """

    return projectdir(project_state.layout["data_dir_pro"], *args)


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def datadir_sims(
    *args,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
) -> Path:
    """Returns the DrWatson-like simulations data directory.
    {0}
    """

    return projectdir(project_state.layout["data_dir_sims"], *args)


# --------------------------------------------------------------------------- #
# DIRFUNCS
# --------------------------------------------------------------------------- #

TypeDirFuncs: TypeAlias = List[Callable]
"""TypeAlias: A type alias for the list of directory functions.
"""


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

# --------------------------------------------------------------------------- #
# OTHER UTILITIES
# --------------------------------------------------------------------------- #


@_docstring_parameter(_ARG_PROJECT_STATE)
def initialize_project(
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
):
    """Initializes a new mrshudon project from the provided project layout dictionary.

    Args:
    {0}
    """

    # Iterate over the layout of the provided project state
    for key, local_path in project_state.layout.items():
        # Optional logging
        lg.info(f"Making directory: {key} at {local_path}")
        # projectdir(local_path).mkdir(parents=True, exist_ok=True)
        projectdir(Path(local_path), project_state=project_state).mkdir(parents=True, exist_ok=True)

    return
