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

# --------------------------------------------------------------------------- #
# LOCAL IMPORTS
# --------------------------------------------------------------------------- #

import src.mrshudson as mrshudson

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
    """Pytest class for mrshudson unit tests.
    """

    def test_test_dir(self):
        """Boilerplate test for showing where the unit tests occur.
        """
        lg.info(f"\nTesting path is: {os.getcwd()}")
        assert True

    def test_initialize(self, tmp_path):
        """Tests the initialization of the default layout.
        """

        # Change to the temporary directory from the default pytest fixture
        os.chdir(tmp_path)
        lg.info(f"Current directory: {os.getcwd()}")

        # Set the new projectdir
        mrshudson.set_projectdir(tmp_path.stem)
        lg.info(f"New projectdir: {mrshudson.projectdir()}")

        # Initialize a project
        mrshudson.initialize_project()

        # Test that the initialied directories exist
        for dirfunc in mrshudson.DIRFUNCS:
            assert dirfunc().exists()

        return
