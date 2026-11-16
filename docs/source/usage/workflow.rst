Produce or Load Results
=======================

:func:`mrshudson.saving.produce_or_load` reuses a saved result when its filename
exists. Otherwise it calls ``func(config)``, saves the result atomically, and
returns ``(data, path)``. The default directory is ``mrs.dirs.datadir_sims()``.

.. doctest::

   >>> import tempfile
   >>> import mrshudson as mrs
   >>> cache = tempfile.TemporaryDirectory()
   >>> def simulate(config):
   ...     return {"score": config["seed"] * 2}
   >>> result, path = mrs.saving.produce_or_load(
   ...     simulate, {"seed": 7}, cache.name)
   >>> result
   {'score': 14}
   >>> path.name
   'seed=7.json'
   >>> def must_not_run(config):
   ...     raise RuntimeError("cache should be reused")
   >>> mrs.saving.produce_or_load(must_not_run, {"seed": 7}, cache.name)[0]
   {'score': 14}
   >>> cache.cleanup()

Cache Identity
--------------

Generated names use :func:`~mrshudson.naming.savename` with full float precision
(``sigdigits=None``). Pass ``naming_options={"prefix": "experiment"}`` to customize
them, or ``filename="experiment-v2.json"`` to supply a complete basename.
``suffix="pkl"`` selects pickle; load only trusted pickle caches.

The filename is the entire cache key. Code changes, ignored parameters, and
values omitted by ``savename`` do not invalidate it. Include a version and all
relevant scalar parameters in the name, or supply a distinct filename for complex
configurations. Float rounding and sanitization can produce collisions. An empty
generated name is rejected. Keep the full configuration in your result for audit.

Refresh and Metadata
--------------------

Use ``force=True`` to recompute and replace the existing cache after a successful
save. Producer and serialization failures leave the previous cache intact.
Load errors, including corrupt files, propagate instead of triggering computation.

``tagged=True`` adds the metadata produced by :func:`~mrshudson.saving.tag`.
``git_path`` selects the source repository, defaulting to the configured project
root. Mapping results gain a ``_mrshudson`` entry; other results are wrapped under
``data``. A hit returns the saved metadata unchanged.

Both misses and hits return deserialized data. JSON may therefore convert tuples
to lists or dates to strings even on the first call. The returned path is absolute.

Concurrent Producers
--------------------

By default, a sibling directory named ``<filename>.lock`` serializes cooperating
calls for the same result, including the existence check, production, and save.
``lock_timeout`` controls the wait (60 seconds by default); expiration raises
``TimeoutError``. Choose a longer timeout for lengthy computations. Forced calls
each recompute, even if another caller has just finished.

Locks are released on ordinary exceptions. A killed process can leave a stale
lock; remove it only after verifying the producer is no longer running. The
filesystem must support exclusive directory creation, atomic replacement, and
hard links. This is not a distributed lease service.

With ``lock=False``, simultaneous misses may compute more than once. Atomic
publication still prevents an unforced call from replacing another writer's
result; it loads the winning result instead. Forced calls may replace each other.
