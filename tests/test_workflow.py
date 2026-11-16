"""Behavioral tests for persistent computation results."""

import multiprocessing
import time
from concurrent.futures import ProcessPoolExecutor

import pytest

from mrshudson import saving


def test_hit_skips_producer_and_normalizes_json(tmp_path):
    calls = []
    config = {"rate": 0.1234567}

    def produce(value):
        assert value is config
        calls.append(value)
        return {"values": (1, 2)}

    first = saving.produce_or_load(produce, config, tmp_path)
    second = saving.produce_or_load(produce, config, tmp_path)
    assert first == second == ({"values": [1, 2]}, tmp_path / "rate=0.1234567.json")
    assert len(calls) == 1


def test_force_and_failures_preserve_previous_cache(tmp_path):
    options = {"filename": "result.json"}
    saving.produce_or_load(lambda _: 1, {}, tmp_path, **options)

    def broken(_):
        raise RuntimeError("producer failed")

    with pytest.raises(RuntimeError):
        saving.produce_or_load(broken, {}, tmp_path, force=True, **options)
    with pytest.raises(TypeError):
        saving.produce_or_load(lambda _: complex(1, 2), {}, tmp_path, force=True, **options)
    assert saving.load(tmp_path / "result.json") == 1
    assert sorted(p.name for p in tmp_path.iterdir()) == ["result.json"]
    assert saving.produce_or_load(lambda _: 2, {}, tmp_path, force=True, **options)[0] == 2


def test_corrupt_cache_is_not_silently_recomputed(tmp_path):
    (tmp_path / "result.json").write_text("invalid JSON")
    with pytest.raises(ValueError):
        saving.produce_or_load(lambda _: pytest.fail("called"), {}, tmp_path,
                               filename="result.json")


def test_pickle_and_tagged_results(tmp_path):
    result, path = saving.produce_or_load(lambda _: (1, 2), {"seed": 1}, tmp_path,
                                         suffix="pkl", tagged=True, git_path=tmp_path)
    assert result["data"] == (1, 2)
    assert "timestamp_utc" in result["_mrshudson"]
    assert saving.produce_or_load(lambda _: None, {"seed": 1}, tmp_path,
                                  suffix="pkl")[0] == result
    assert path.suffix == ".pkl"


def test_lock_timeout(tmp_path):
    (tmp_path / "result.json.lock").mkdir()
    with pytest.raises(TimeoutError):
        saving.produce_or_load(lambda _: pytest.fail("called"), {}, tmp_path,
                               filename="result.json", lock_timeout=0)
    assert (tmp_path / "result.json.lock").exists()


@pytest.mark.parametrize("options", [
    {"filename": "../escape.json"}, {"suffix": "unknown"},
    {"lock_timeout": -1}, {"lock_timeout": float("inf")},
    {"filename": "x.json", "naming_options": {}},
])
def test_invalid_options_fail_before_production(tmp_path, options):
    with pytest.raises(ValueError):
        saving.produce_or_load(lambda _: pytest.fail("called"), {"x": 1}, tmp_path,
                               **options)


def _worker(directory):
    def produce(config):
        with (directory / "calls.txt").open("a") as stream:
            stream.write("called\n")
        time.sleep(0.1)
        return config

    return saving.produce_or_load(produce, {"seed": 2}, directory)


def test_processes_share_one_computation(tmp_path):
    with ProcessPoolExecutor(max_workers=3, mp_context=multiprocessing.get_context("spawn")) as pool:
        results = list(pool.map(_worker, [tmp_path] * 3))
    assert results[0] == results[1] == results[2]
    assert (tmp_path / "calls.txt").read_text() == "called\n"


def test_atomic_no_overwrite_handles_competing_publication(tmp_path, monkeypatch):
    original = saving._write_data
    target = tmp_path / "result.json"

    def competing_write(*args, **kwargs):
        original(*args, **kwargs)
        target.write_text("42")

    monkeypatch.setattr(saving, "_write_data", competing_write)
    with pytest.raises(FileExistsError):
        saving.save(target, 10, overwrite=False)
    assert saving.load(target) == 42
