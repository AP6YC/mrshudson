"""Tests for the mrshudson package."""

import shutil
import subprocess
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


def test_save_and_load_json_creates_parent_directory(tmp_path):
    path = tmp_path / "nested" / "result.json"
    data = {"a": 1, "b": [2, 3]}

    written = mrs.saving.save(path, data)

    assert written == path
    assert path.exists()
    assert mrs.saving.load(path) == data


def test_save_refuses_overwrite_when_requested(tmp_path):
    path = tmp_path / "result.json"
    mrs.saving.save(path, {"a": 1})

    with pytest.raises(FileExistsError):
        mrs.saving.save(path, {"a": 2}, overwrite=False)


def test_safe_save_increments_existing_filename(tmp_path):
    path = tmp_path / "result.json"
    mrs.saving.save(path, {"a": 1})

    written = mrs.saving.safe_save(path, {"a": 2})

    assert written == tmp_path / "result_1.json"
    assert mrs.saving.load(path) == {"a": 1}
    assert mrs.saving.load(written) == {"a": 2}


def test_save_and_load_pickle(tmp_path):
    path = tmp_path / "result.pkl"
    data = {"values": (1, 2, 3)}

    mrs.saving.save(path, data)

    assert mrs.saving.load(path) == data


def test_tag_save_adds_metadata(tmp_path):
    path = tmp_path / "result.json"

    written = mrs.saving.tag_save(path, {"value": 1})
    loaded = mrs.saving.load(written)

    assert loaded["value"] == 1
    assert "_mrshudson" in loaded
    assert loaded["_mrshudson"]["package"] == "mrshudson"
    assert loaded["_mrshudson"]["git"]["available"] is False
    assert "timestamp_utc" in loaded["_mrshudson"]


@pytest.mark.skipif(shutil.which("git") is None, reason="git is unavailable")
def test_git_metadata_detects_repository_and_dirty_state(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    (repo / "result.txt").write_text("untracked\n")

    description = mrs.saving.gitdescribe(repo)

    assert mrs.saving.gitroot(repo) == repo.resolve()
    assert mrs.saving.isdirty(repo)
    assert description["available"] is True
    assert description["root"] == str(repo.resolve())
