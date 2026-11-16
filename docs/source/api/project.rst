Project Setup
=============

.. automodule:: mrshudson.project

.. currentmodule:: mrshudson.project

.. autoclass:: ProjectState

   Supply ``projectdir`` to fix the root and ``layout`` to customize locations.
   Without a root, the state follows the working directory. Layouts are copied.
   See :doc:`../usage/directories` for examples.

.. autofunction:: find_project

.. autofunction:: set_projectdir

.. autofunction:: projectname

.. autofunction:: initialize_project

Configuration
-------------

.. autodata:: DEFAULT_LAYOUT
   :no-value:

.. autodata:: DEFAULT_PROJECT_STATE
   :no-value:

.. autodata:: PROJECT_MARKERS
   :no-value:

