"""
mrshudson - a Python scientific project assistant package.
"""

# -----------------------------------------------------------------------------
# PUBLIC API
# -----------------------------------------------------------------------------

from . import (
    dirs,
    project,
)

# -----------------------------------------------------------------------------
# PACKAGE ATTRIBUTES
# -----------------------------------------------------------------------------

# Package version
__version__ = "0.1.0-alpha.1"

# Exported names when using *
__all__ = [
    "dirs",
    "project",
]
