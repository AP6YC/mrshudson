Public API
==========

Use ``import mrshudson as mrs`` and access public functions through their
modules. Internal helpers and imported dependencies are omitted here.

.. automodule:: mrshudson

.. currentmodule:: None

.. toctree::
   :maxdepth: 1

   api/project
   api/dirs
   api/naming
   api/saving

Project Setup
-------------

.. autosummary::
   :nosignatures:

   mrshudson.project.ProjectState
   mrshudson.project.find_project
   mrshudson.project.set_projectdir
   mrshudson.project.projectname
   mrshudson.project.initialize_project

Directory Paths
---------------

.. autosummary::
   :nosignatures:

   mrshudson.dirs.projectdir
   mrshudson.dirs.plotsdir
   mrshudson.dirs.papersdir
   mrshudson.dirs.srcdir
   mrshudson.dirs.scriptsdir
   mrshudson.dirs.optsdir
   mrshudson.dirs.modelsdir
   mrshudson.dirs.notebooksdir
   mrshudson.dirs.datadir
   mrshudson.dirs.datadir_raw
   mrshudson.dirs.datadir_pro
   mrshudson.dirs.datadir_sims
   mrshudson.dirs.initialize_project

File Naming
-----------

.. autosummary::
   :nosignatures:

   mrshudson.naming.savename
   mrshudson.naming.parse_savename

Saving and Metadata
-------------------

.. autosummary::
   :nosignatures:

   mrshudson.saving.save
   mrshudson.saving.load
   mrshudson.saving.safe_path
   mrshudson.saving.safe_save
   mrshudson.saving.tag
   mrshudson.saving.tag_save
   mrshudson.saving.gitroot
   mrshudson.saving.gitdescribe
   mrshudson.saving.isdirty
   mrshudson.saving.gitpatch
