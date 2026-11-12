"""Directory utilities for the `mrshudson` package."""

# --------------------------------------------------------------------------- #
# STDLIB IMPORTS
# --------------------------------------------------------------------------- #

from pathlib import Path
from typing import Callable, TypeAlias

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
    TypeLayout,
    initialize_project as _initialize_project,
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

    return projectdir(
        project_state.layout["plots_dir"],
        *args,
        project_state=project_state,
    )


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def papersdir(
    *args,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
) -> Path:
    """Returns the DrWatson-like papers directory.
    {0}
    """

    return projectdir(
        project_state.layout["papers_dir"],
        *args,
        project_state=project_state,
    )


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def srcdir(
    *args,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
) -> Path:
    """Returns the DrWatson-like source directory.
    {0}
    """

    return projectdir(
        project_state.layout["src_dir"],
        *args,
        project_state=project_state,
    )


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def scriptsdir(
    *args,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
) -> Path:
    """Returns the DrWatson-like scripts directory.
    {0}
    """

    return projectdir(
        project_state.layout["scripts_dir"],
        *args,
        project_state=project_state,
    )


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def optsdir(
    *args,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
) -> Path:
    """Returns the DrWatson-like options directory.
    {0}
    """

    return projectdir(
        project_state.layout["opts_dir"],
        *args,
        project_state=project_state,
    )


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def modelsdir(
    *args,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
) -> Path:
    """Returns the DrWatson-like models directory.
    {0}
    """

    return projectdir(
        project_state.layout["models_dir"],
        *args,
        project_state=project_state,
    )


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def notebooksdir(
    *args,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
) -> Path:
    """Returns the DrWatson-like notebooks directory.
    {0}
    """

    return projectdir(
        project_state.layout["notebooks_dir"],
        *args,
        project_state=project_state,
    )


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def datadir(
    *args,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
) -> Path:
    """Returns the DrWatson-like data directory.
    {0}
    """

    return projectdir(
        project_state.layout["data_dir"],
        *args,
        project_state=project_state,
    )


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def datadir_raw(
    *args,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
) -> Path:
    """Returns the DrWatson-like raw data directory.
    {0}
    """

    return projectdir(
        project_state.layout["data_dir_raw"],
        *args,
        project_state=project_state,
    )


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def datadir_pro(
    *args,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
) -> Path:
    """Returns the DrWatson-like processed data directory.
    {0}
    """

    return projectdir(
        project_state.layout["data_dir_pro"],
        *args,
        project_state=project_state,
    )


@_docstring_parameter(_ARG_ARGS_PROJECT_STATE)
def datadir_sims(
    *args,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
) -> Path:
    """Returns the DrWatson-like simulations data directory.
    {0}
    """

    return projectdir(
        project_state.layout["data_dir_sims"],
        *args,
        project_state=project_state,
    )


# --------------------------------------------------------------------------- #
# DIRFUNCS
# --------------------------------------------------------------------------- #

TypeDirFuncs: TypeAlias = list[Callable]
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
    notebooksdir,
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
    path: str | Path | None = None,
    *,
    layout: TypeLayout | None = None,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
    exist_ok: bool = True,
) -> Path:
    """Initializes a new mrshudon project from the provided project layout dictionary.

    Args:
        path: Optional project root to initialize and set on ``project_state``.
        layout: Optional project layout. Defaults to ``project_state.layout``.
        {0}
        exist_ok: Passed to :meth:`pathlib.Path.mkdir` for each directory.
    """

    return _initialize_project(
        path,
        layout=layout,
        project_state=project_state,
        exist_ok=exist_ok,
    )
