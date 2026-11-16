File Naming
===========

Name an Experiment
------------------

:func:`~mrshudson.naming.savename` produces a string from parameter values.
Keys are sorted by default, so dictionary insertion order does not affect the
name. Prefixes and filename extensions are optional:

.. doctest::

   >>> import mrshudson as mrs
   >>> config = {"mode": "double", "a": 0.153456453, "b": 5}
   >>> mrs.naming.savename(config)
   'a=0.153_b=5_mode=double'
   >>> mrs.naming.savename(config, prefix="sim", suffix="json")
   'sim_a=0.153_b=5_mode=double.json'

Combine that string with a directory helper to get a complete path:

.. code-block:: python

   filename = mrs.naming.savename(config, prefix="sim", suffix="json")
   path = mrs.dirs.datadir_sims(filename)
   mrs.saving.save(path, {"config": config, "mean": 1.25})

Naming itself performs no filesystem writes. Store the full configuration with
results: rounded values and omitted fields mean names are not unique identifiers.

Containers and Selection
------------------------

Inputs may be mappings, dataclass instances, namedtuples, or objects with public
attributes. Default included values are integers, floats, booleans, strings,
dates, datetimes, and times. Lists, arrays, ``None``, and nested mappings are
omitted unless supported through the relevant options.

.. doctest::

   >>> from dataclasses import dataclass
   >>> @dataclass
   ... class Config:
   ...     seed: int
   ...     mode: str
   >>> mrs.naming.savename(Config(seed=7, mode="fast"))
   'mode=fast_seed=7'
   >>> mrs.naming.savename(config, accesses=["mode", "b"], sort=False)
   'mode=double_b=5'
   >>> mrs.naming.savename(config, ignores=["a"])
   'b=5_mode=double'

``accesses`` selects fields; ``ignores`` takes precedence. Missing selected keys
are skipped. ``allowedtypes`` replaces the set of included types.

Formatting
----------

Floats use three significant digits by default. ``digits`` selects decimal-place
rounding and takes precedence over ``sigdigits``. Use ``sigdigits=None`` for the
normal Python string representation. Booleans become ``true`` or ``false``;
date and time values use ISO format.

.. doctest::

   >>> mrs.naming.savename(config, digits=4)
   'a=0.1535_b=5_mode=double'
   >>> mrs.naming.savename({"x": 1, "y": 2}, connector="-", equals=":")
   'x:1-y:2'
   >>> mrs.naming.savename({"x": 1.25}, val_to_string=lambda v: f"{v:.2f}")
   'x=1.25'

``val_to_string`` formats each included value. ``expand=["key"]`` names a nested
container under that key, but does not preserve a parseable nested structure:

.. doctest::

   >>> mrs.naming.savename({"model": {"width": 8}}, expand=["model"])
   'model=width=8'

By default, sanitization replaces forward and backward slashes with hyphens and
removes null bytes from keys, values, and prefixes. It is not full filename
validation, does not escape separators, and does not sanitize the suffix.
Choose a simple extension and filesystem-compatible parameter strings.

Read Parameters from a Name
---------------------------

:func:`~mrshudson.naming.parse_savename` returns ``(prefix, parameters, suffix)``
and ignores the directory portion of its input. Values are interpreted as
booleans, then integers or floats, and otherwise strings:

.. doctest::

   >>> mrs.naming.parse_savename("sim_a=0.153_b=5_mode=double.json")
   ('sim', {'a': 0.153, 'b': 5, 'mode': 'double'}, 'json')

Pass matching ``connector`` and ``equals`` options when using custom separators.
``parsetypes`` customizes numeric conversion; boolean conversion always runs
first. This parser is a convenience for simple names, not a lossless inverse:

* Numeric-looking strings lose their original string type.
* Separators within keys or values and expanded containers are ambiguous.
* Without an explicit extension, a trailing decimal such as ``x=0.25`` is
  currently interpreted as ``x=0`` with suffix ``25``.
* Rounding, sanitization, and omitted fields cannot be reversed.

Use a simple explicit extension for names you intend to parse, and retain the
original configuration in the saved result. See :doc:`../api/naming` for all
parameters and defaults.
