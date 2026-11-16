Directories and Projects
========================

Choose a Project Root
---------------------

Directory helpers return ``pathlib.Path`` objects. Configure the root once
before using them in scripts or notebooks:

.. code-block:: python

   from pathlib import Path
   import mrshudson as mrs

   # Discover the nearest ancestor containing pyproject.toml or .git.
   root = mrs.project.set_projectdir()

   # Alternatively, select an existing directory explicitly.
   root = mrs.project.set_projectdir(Path("~/research/my_project"))

For upward discovery from a particular directory or existing file, pass
``start=...``. A bare name such as ``"my_project"`` searches parent directories
when it does not identify an existing path. Discovery selects the nearest
matching ancestor and raises ``FileNotFoundError`` if nothing matches.

:func:`~mrshudson.project.find_project` discovers a root without changing the
active state. It accepts custom markers and ``missing_ok=True`` to return
``None`` when no match exists:

.. code-block:: python

   root = mrs.project.find_project(
       start=Path.cwd(), markers=("pyproject.toml",), missing_ok=True
   )

Setting the root does not change the working directory or activate a Python
environment. Until a root is explicitly set, directory helpers use the current
working directory at each call. An explicitly set root stays fixed when the
working directory changes. :func:`~mrshudson.project.projectname` returns its
directory name.

Build Paths
-----------

.. code-block:: python

   observations = mrs.dirs.datadir_raw("study_a", "observations.csv")
   figure = mrs.dirs.plotsdir("study_a", "summary.png")
   script = mrs.dirs.projectdir("scripts", "run.py")
   same_script = mrs.dirs.projectdir() / "scripts" / "run.py"

Pass relative components to keep paths under the chosen root. These helpers
join paths; they neither create files nor check that the paths exist. Absolute
components and ``..`` follow normal ``pathlib`` rules and can leave the root.

.. list-table:: Default locations relative to the project root
   :header-rows: 1
   :widths: 45 55

   * - Helper
     - Location
   * - :func:`~mrshudson.dirs.projectdir`
     - Project root
   * - :func:`~mrshudson.dirs.plotsdir`
     - ``plots``
   * - :func:`~mrshudson.dirs.papersdir`
     - ``papers``
   * - :func:`~mrshudson.dirs.srcdir`
     - ``src``
   * - :func:`~mrshudson.dirs.scriptsdir`
     - ``scripts``
   * - :func:`~mrshudson.dirs.optsdir`
     - ``opts``
   * - :func:`~mrshudson.dirs.modelsdir`
     - ``models``
   * - :func:`~mrshudson.dirs.notebooksdir`
     - ``notebooks``
   * - :func:`~mrshudson.dirs.datadir`
     - ``data``
   * - :func:`~mrshudson.dirs.datadir_raw`
     - ``data/exp_raw``
   * - :func:`~mrshudson.dirs.datadir_pro`
     - ``data/exp_pro``
   * - :func:`~mrshudson.dirs.datadir_sims`
     - ``data/sims``

Initialize and Customize
------------------------

:func:`~mrshudson.project.initialize_project` creates the layout directories
and returns the root. Existing directories are accepted by default. Providing
``path`` also sets that root on the selected project state. Initialization
creates directories only: it does not create a Git repository, a project marker,
or a virtual environment.

.. code-block:: python

   root = mrs.project.initialize_project(Path("~/research/new_project"))

For multiple projects or a custom layout, create a
:class:`~mrshudson.project.ProjectState` and pass it explicitly. Copy the default
layout before overriding entries so all named helpers remain available:

.. code-block:: python

   layout = dict(mrs.project.DEFAULT_LAYOUT)
   layout["plots_dir"] = "figures"
   state = mrs.project.ProjectState(Path("~/research/study"), layout=layout)
   mrs.project.initialize_project(project_state=state)
   figure = mrs.dirs.plotsdir("summary.png", project_state=state)

Every directory helper accepts ``project_state``. A state copies its supplied
layout; omitted keys in a custom layout cause the corresponding helper to raise
``KeyError``. Keep layout values relative to the root. The ``layout`` argument to
``initialize_project`` controls that creation call only; configure the state's
layout as above when future helpers should use the same locations.

See :doc:`../api/project` and :doc:`../api/dirs` for the public API.
