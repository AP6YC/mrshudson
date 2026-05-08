"""
mrshudson - a Python scientific project assistant package.
"""

# -----------------------------------------------------------------------------
# PUBLIC API
# -----------------------------------------------------------------------------

from . import (
    dirs,
    naming,
    project,
    saving,
)

# -----------------------------------------------------------------------------
# PACKAGE ATTRIBUTES
# -----------------------------------------------------------------------------

# Package version
__version__ = "0.0.1"

# Exported names when using *
__all__ = [
    "dirs",
    "naming",
    "project",
    "saving",
]
