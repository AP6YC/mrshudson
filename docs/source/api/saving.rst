Saving and Metadata
===================

.. automodule:: mrshudson.saving

.. currentmodule:: mrshudson.saving

.. autofunction:: save

.. autofunction:: load

.. autofunction:: safe_path

.. autofunction:: safe_save

.. autofunction:: tag

.. autofunction:: tag_save

.. autofunction:: gitroot

.. autofunction:: gitdescribe

.. autofunction:: isdirty

.. autofunction:: gitpatch

Configuration
-------------

.. autodata:: DEFAULT_METADATA_KEY
   :no-value:

Compatibility Aliases
---------------------

``wsave`` aliases :func:`save`, ``safesave`` aliases :func:`safe_save`, and
``tagsave`` aliases :func:`tag_save`.

Only load pickle files from trusted sources: unpickling can execute code.

