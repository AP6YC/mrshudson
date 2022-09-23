"""
    test_mrshudson.py

Tests the mrshudson package.
"""

# --------------------------------------------------------------------------- #
# STANDARD IMPORTS
# --------------------------------------------------------------------------- #

import os
from pathlib import Path
import logging as lg
from typing import (
    List,
    Dict,
    Tuple,
)

# --------------------------------------------------------------------------- #
# CUSTOM IMPORTS
# --------------------------------------------------------------------------- #

import pytest
import numpy as np
import pandas as pd

# --------------------------------------------------------------------------- #
# LOCAL IMPORTS
# --------------------------------------------------------------------------- #

import src.mrshudson as mrshudson

print(f"\nTesting path is: {os.getcwd()}")

# --------------------------------------------------------------------------- #
# UTILITY FUNCTIONS
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# FIXTURES
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# TESTS
# --------------------------------------------------------------------------- #

class TestMrsHudson:
    """
    Pytest class for mrshudson unit tests.
    """

    def test_mrshudson(self):
        """
        Boilerplate test.
        """

        assert True