"""Project root discovery and project state management."""

# --------------------------------------------------------------------------- #
# STDLIB IMPORTS
# --------------------------------------------------------------------------- #

import logging as lg
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import TypeAlias

# --------------------------------------------------------------------------- #
# LOCAL IMPORTS
# --------------------------------------------------------------------------- #

from ._utils import (
    _docstring_parameter,
    _ARG_PROJECT_STATE,
)

TypeLayout: TypeAlias = Mapping[str, str]
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

PROJECT_MARKERS: tuple[str, ...] = ("pyproject.toml", ".git")
"""Default files or directories used to discover a Python project root."""


class ProjectState:
    """The stateful information for a `mrshudson` project.
    """

    def __init__(
        self,
        projectdir: str | Path | None = None,
        layout: TypeLayout | None = None,
    ):
        """Initializes the project state with the :func:`~default_projectdir` function.
        """

        self.projectdir: Path = (
            Path(projectdir).expanduser().resolve()
            if projectdir is not None
            else self._default_projectdir()
        )
        """The project directory.
        """

        self.projectdir_was_set: bool = projectdir is not None
        """A flag for if the projectdir was manually set.

        If low, the default the :func:`~default_projectdir` function is used to get the current :attr:`~ProjectState.projectdir`.
        """

        self.layout: dict[str, str] = dict(
            DEFAULT_LAYOUT if layout is None else layout
        )
        """The layout of the project directory structure.

        This is used both for instantiating a project and for pointing to the correct locations when using the directory functions.
        """

        return

    def _default_projectdir(self):
        """Generates the default projectdir directory as the current working directory at runtime.
        """

        return Path.cwd()

    def _set_projectdir(self, new_projectdir: str | Path):
        """Sets the projectdir from the provided path.

        This function also informs the :attr:`~project_was_set` attribute that the :attr:`~ProjectState.projectdir`. was set.

        Args:
            new_projectdir (Path): the new `pathlib.Path` that points to new :attr:`~ProjectState.projectdir` to use.
        """

        # Set the project directory to the provided path.
        self.projectdir = Path(new_projectdir).expanduser().resolve()

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


def _path_candidates(start: str | Path | None = None) -> Iterable[Path]:
    """Yield ``start`` and its parents from nearest to farthest."""

    path = Path.cwd() if start is None else Path(start).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    path = path.resolve()
    if path.is_file():
        path = path.parent

    yield path
    yield from path.parents


def _is_marker_match(path: Path, markers: Iterable[str]) -> bool:
    """Return whether ``path`` contains any project marker."""

    return any((path / marker).exists() for marker in markers)


def find_project(
    start: str | Path | None = None,
    markers: Iterable[str] = PROJECT_MARKERS,
    *,
    missing_ok: bool = False,
) -> Path | None:
    """Find the nearest project root containing one of ``markers``.

    Args:
        start: Directory or file to begin searching from. Defaults to the
            current working directory.
        markers: Files or directories that identify a project root.
        missing_ok: Return ``None`` instead of raising if no root is found.
    """

    marker_tuple = tuple(markers)
    for candidate in _path_candidates(start):
        if _is_marker_match(candidate, marker_tuple):
            return candidate

    if missing_ok:
        return None

    marker_display = ", ".join(marker_tuple)
    start_display = Path.cwd() if start is None else Path(start)
    raise FileNotFoundError(
        f"No project root containing one of {marker_display} found from {start_display}."
    )


def _find_named_parent(project_name: str, start: str | Path | None = None) -> Path:
    """Find the nearest parent directory named ``project_name``."""

    for candidate in _path_candidates(start):
        if candidate.name == project_name:
            return candidate

    start_display = Path.cwd() if start is None else Path(start)
    raise FileNotFoundError(
        f"No parent directory named {project_name!r} found from {start_display}."
    )


@_docstring_parameter(_ARG_PROJECT_STATE)
def set_projectdir(
    project: str | Path | None = None,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
    *,
    start: str | Path | None = None,
    markers: Iterable[str] = PROJECT_MARKERS,
) -> Path:
    """Sets the top projectdir location for all future calls in this session.

    ``project`` may be an explicit path, a parent directory name, or ``None``.
    When ``project`` is ``None``, the nearest parent containing one of
    ``markers`` is used.

    This function assumes the current working directory of the callee (e.g.,
    script, notebook, etc.) is at or below the project directory unless an
    explicit path is provided.

    Args:
        project: Path to the project root, parent directory name to search for,
            or ``None`` for marker-based discovery.
        {0}
        start: Directory or file to begin upward discovery from.
        markers: Files or directories that identify a Python project root.
    """

    if project is None:
        new_projectdir = find_project(start=start, markers=markers)
    else:
        project_path = Path(project).expanduser()
        project_str = str(project)
        looks_like_path = (
            isinstance(project, Path)
            or project_str in {".", ".."}
            or any(separator in project_str for separator in ("/", "\\"))
            or project_path.exists()
        )

        if looks_like_path:
            if not project_path.is_absolute():
                base = Path.cwd() if start is None else Path(start).expanduser()
                project_path = base / project_path
            project_path = project_path.resolve()
            if project_path.is_file():
                project_path = project_path.parent
            if not project_path.exists():
                raise FileNotFoundError(
                    f"Project path does not exist: {project_path}"
                )
            new_projectdir = project_path
        else:
            new_projectdir = _find_named_parent(project_str, start=start)

    project_state._set_projectdir(new_projectdir)
    return project_state._get_projectdir()


@_docstring_parameter(_ARG_PROJECT_STATE)
def projectname(
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
) -> str:
    """Return the name of the currently configured project.

    Args:
        {0}
    """

    return project_state._get_projectdir().name


@_docstring_parameter(_ARG_PROJECT_STATE)
def initialize_project(
    path: str | Path | None = None,
    *,
    layout: TypeLayout | None = None,
    project_state: ProjectState = DEFAULT_PROJECT_STATE,
    exist_ok: bool = True,
) -> Path:
    """Initializes a new mrshudson project from a layout dictionary.

    Args:
        path: Optional project root to initialize and set on ``project_state``.
        layout: Optional project layout. Defaults to ``project_state.layout``.
        {0}
        exist_ok: Passed to :meth:`pathlib.Path.mkdir` for each directory.
    """

    if path is not None:
        project_state._set_projectdir(path)

    project_root = project_state._get_projectdir()
    active_layout = project_state.layout if layout is None else layout
    for key, local_path in dict(active_layout).items():
        target = project_root.joinpath(local_path)
        lg.info("Making directory: %s at %s", key, target)
        target.mkdir(parents=True, exist_ok=exist_ok)

    return project_root
