"""
    test_mrshudson.py

Tests the mrshudson package.
"""

# --------------------------------------------------------------------------- #
# STANDARD IMPORTS
# --------------------------------------------------------------------------- #

import os
# from pathlib import Path
import logging as lg
# from typing import (
#     List,
#     Dict,
#     Tuple,
# )

# import tempfile

# --------------------------------------------------------------------------- #
# CUSTOM IMPORTS
# --------------------------------------------------------------------------- #

# import pytest
# import numpy as np
# import pandas as pd

# --------------------------------------------------------------------------- #
# LOCAL IMPORTS
# --------------------------------------------------------------------------- #

import src.mrshudson as mrshudson

# print(f"\nTesting path is: {os.getcwd()}")
# lg.info(f"\nTesting path is: {os.getcwd()}")

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

    def test_test_dir(self):
        lg.info(f"\nTesting path is: {os.getcwd()}")
        assert True

    def test_mrshudson(self):
        """
        Boilerplate test.
        """

        lg.info("First test!")

        assert True

    def test_initialize(self, tmp_path):
        """
        Tests the initialization of the default layout.
        """

        # Change to the temporary directory from the default pytest fixture
        os.chdir(tmp_path)
        lg.info(f"Current directory: {os.getcwd()}")

        # Set the new projectdir
        mrshudson.set_projectdir(tmp_path.stem)
        lg.info(f"New projectdir: {mrshudson.projectdir()}")

        mrshudson.initialize_project()
        # Initialize a project

        assert True
