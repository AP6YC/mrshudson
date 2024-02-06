"""
    project.py

# Description
This file contains the definitions for `mrshudson` project structures and states.
"""

# --------------------------------------------------------------------------- #
# STDLIB IMPORTS
# --------------------------------------------------------------------------- #

import os
import warnings
from pathlib import Path

# --------------------------------------------------------------------------- #
# EXTERNAL DEPENDENCY IMPORTS
# --------------------------------------------------------------------------- #

from typing_extensions import (
    TypeAlias,
    Dict,
)

# --------------------------------------------------------------------------- #
# LOCAL IMPORTS
# --------------------------------------------------------------------------- #

from ._utils import (
    _docstring_parameter,
    _ARG_PROJECT_STATE,
)

TypeLayout: TypeAlias = Dict[str, str]
"""TypeAlias: A type alias for the layout of a project.
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
"""TypeLayout: The default :mod:`mrshudson` project layout.
"""     # pylint: disable=W0105


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


DEFAULT_PROJECT_STATE: ProjectState = ProjectState()
"""ProjectState: The default project state that is used when mrshudson directory functions.
"""


@_docstring_parameter(_ARG_PROJECT_STATE)
def set_projectdir(
    project_name: str,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
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
