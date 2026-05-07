"""Tests for the mrshudson package."""

from dataclasses import dataclass

import pytest

import mrshudson as mrs
from mrshudson.project import DEFAULT_LAYOUT, ProjectState


def test_initialize_project_from_project_module(tmp_path):
    state = ProjectState()

    root = mrs.project.initialize_project(tmp_path, project_state=state)

    assert root == tmp_path.resolve()
    for local_path in state.layout.values():
        assert (root / local_path).exists()


def test_set_projectdir_discovers_marker_from_nested_path(tmp_path):
    root = tmp_path / "example_project"
    nested = root / "scripts" / "nested"
    nested.mkdir(parents=True)
    (root / "pyproject.toml").write_text("[project]\nname = 'example-project'\n")
    state = ProjectState()

    found = mrs.project.set_projectdir(project_state=state, start=nested)

    assert found == root.resolve()
    assert mrs.dirs.projectdir(project_state=state) == root.resolve()


def test_set_projectdir_finds_named_parent(tmp_path):
    root = tmp_path / "named_project"
    nested = root / "notebooks" / "scratch"
    nested.mkdir(parents=True)
    state = ProjectState()

    found = mrs.project.set_projectdir(
        "named_project",
        project_state=state,
        start=nested,
    )

    assert found == root.resolve()


def test_set_projectdir_raises_for_missing_project(tmp_path):
    state = ProjectState()

    with pytest.raises(FileNotFoundError):
        mrs.project.set_projectdir("missing", project_state=state, start=tmp_path)


def test_directory_helpers_honor_custom_project_state(tmp_path):
    layout = dict(DEFAULT_LAYOUT)
    layout["plots_dir"] = "figures"
    state = ProjectState(projectdir=tmp_path, layout=layout)

    assert (
        mrs.dirs.plotsdir("plot.png", project_state=state)
        == tmp_path.resolve() / "figures" / "plot.png"
    )


def test_initialize_project_includes_all_directory_functions(tmp_path):
    state = ProjectState(projectdir=tmp_path)

    mrs.dirs.initialize_project(project_state=state)

    for dirfunc in mrs.dirs.DIRFUNCS:
        assert dirfunc(project_state=state).exists()


@dataclass
class SimulationConfig:
    a: float
    b: int
    mode: str
    scratch: list[int]


def test_savename_uses_sorted_allowed_values_and_ignores_keys():
    config = SimulationConfig(
        a=0.153456453,
        b=5,
        mode="double",
        scratch=[1, 2, 3],
    )

    name = mrs.naming.savename(config, ignores=["scratch"])

    assert name == "a=0.153_b=5_mode=double"


def test_savename_supports_prefix_suffix_and_rounding():
    config = {"mode": "double", "a": 0.153456453, "b": 5}

    name = mrs.naming.savename(config, prefix="sim", suffix="json", digits=4)

    assert name == "sim_a=0.1535_b=5_mode=double.json"


def test_parse_savename_returns_prefix_parameters_and_suffix():
    prefix, params, suffix = mrs.naming.parse_savename(
        "sim_a=0.153_b=5_flag=true.json"
    )

    assert prefix == "sim"
    assert params == {"a": 0.153, "b": 5, "flag": True}
    assert suffix == "json"


def test_parse_savename_keeps_decimal_values_without_suffix():
    prefix, params, suffix = mrs.naming.parse_savename("a=0.153_b=5")

    assert prefix == ""
    assert params == {"a": 0.153, "b": 5}
    assert suffix == ""
