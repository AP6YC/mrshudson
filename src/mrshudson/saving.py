"""Saving, loading, and reproducibility helpers."""

from __future__ import annotations

import dataclasses
import json
import os
import pickle
import subprocess
import tempfile
from collections.abc import Mapping, MutableMapping
from datetime import date, datetime, time, timezone
from pathlib import Path
from typing import Any

JSON_SUFFIXES = {".json"}
"""Filename suffixes handled by the JSON serializer."""

PICKLE_SUFFIXES = {".pkl", ".pickle"}
"""Filename suffixes handled by the pickle serializer."""

SUPPORTED_SERIALIZERS = ("json", "pickle")
"""Serializer names supported by :func:`save` and :func:`load`."""

DEFAULT_METADATA_KEY = "_mrshudson"
"""Default key used by :func:`tag` for reproducibility metadata."""


def _json_default(value: Any) -> Any:
    """Convert common scientific config objects to JSON-compatible values."""

    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return dataclasses.asdict(value)

    if isinstance(value, (date, datetime, time)):
        return value.isoformat()

    if isinstance(value, Path):
        return str(value)

    if isinstance(value, set):
        return list(value)

    if hasattr(value, "_asdict"):
        return value._asdict()

    if hasattr(value, "__dict__"):
        return {
            key: item
            for key, item in vars(value).items()
            if not key.startswith("_")
        }

    raise TypeError(
        f"Object of type {type(value).__name__} is not JSON serializable."
    )


def _normalise_serializer(
    path: str | Path,
    serializer: str | None = None,
) -> str:
    """Return the serializer name inferred from ``path`` or ``serializer``."""

    if serializer is not None:
        serializer_name = serializer.lower().lstrip(".")
        if serializer_name in {"pkl", "pickle"}:
            return "pickle"
        if serializer_name == "json":
            return "json"
        raise ValueError(
            f"Unsupported serializer {serializer!r}; expected one of "
            f"{', '.join(SUPPORTED_SERIALIZERS)}."
        )

    suffix = Path(path).suffix.lower()
    if suffix in JSON_SUFFIXES:
        return "json"
    if suffix in PICKLE_SUFFIXES:
        return "pickle"

    raise ValueError(
        f"Could not infer serializer from suffix {suffix!r}; pass serializer "
        f"with one of {', '.join(SUPPORTED_SERIALIZERS)}."
    )


def _prepare_target(path: str | Path, create_dirs: bool) -> Path:
    """Resolve a save target and optionally create its parent directory."""

    target = Path(path).expanduser()
    if create_dirs:
        target.parent.mkdir(parents=True, exist_ok=True)
    return target


def _atomic_target(path: Path) -> tuple[int, Path]:
    """Create a temporary file in the target directory for atomic replacement."""

    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    return descriptor, Path(temporary_name)


def _write_data(
    path: Path,
    data: Any,
    serializer: str,
    *,
    indent: int | None,
    sort_keys: bool,
    pickle_protocol: int,
) -> None:
    """Write ``data`` to ``path`` using ``serializer``."""

    if serializer == "json":
        with path.open("w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                default=_json_default,
                indent=indent,
                sort_keys=sort_keys,
            )
            file.write("\n")
        return

    if serializer == "pickle":
        with path.open("wb") as file:
            pickle.dump(data, file, protocol=pickle_protocol)
        return

    raise ValueError(f"Unsupported serializer: {serializer!r}.")


def save(
    path: str | Path,
    data: Any,
    *,
    serializer: str | None = None,
    overwrite: bool = True,
    atomic: bool = True,
    create_dirs: bool = True,
    indent: int | None = 2,
    sort_keys: bool = True,
    pickle_protocol: int = pickle.HIGHEST_PROTOCOL,
) -> Path:
    """Save ``data`` to ``path`` and return the path written.

    The serializer is inferred from the filename suffix unless ``serializer`` is
    provided. JSON and pickle are supported without extra dependencies.
    """

    target = _prepare_target(path, create_dirs=create_dirs)
    serializer_name = _normalise_serializer(target, serializer)
    if target.exists() and not overwrite:
        raise FileExistsError(f"Refusing to overwrite existing file: {target}")

    if not atomic:
        _write_data(
            target,
            data,
            serializer_name,
            indent=indent,
            sort_keys=sort_keys,
            pickle_protocol=pickle_protocol,
        )
        return target

    descriptor, temporary_path = _atomic_target(target)
    os.close(descriptor)
    try:
        _write_data(
            temporary_path,
            data,
            serializer_name,
            indent=indent,
            sort_keys=sort_keys,
            pickle_protocol=pickle_protocol,
        )
        if target.exists() and not overwrite:
            raise FileExistsError(f"Refusing to overwrite existing file: {target}")
        os.replace(temporary_path, target)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()

    return target


def load(
    path: str | Path,
    *,
    serializer: str | None = None,
) -> Any:
    """Load data from ``path``."""

    source = Path(path).expanduser()
    serializer_name = _normalise_serializer(source, serializer)

    if serializer_name == "json":
        with source.open("r", encoding="utf-8") as file:
            return json.load(file)

    if serializer_name == "pickle":
        with source.open("rb") as file:
            return pickle.load(file)

    raise ValueError(f"Unsupported serializer: {serializer_name!r}.")


def safe_path(
    path: str | Path,
    *,
    connector: str = "_",
    start: int = 1,
) -> Path:
    """Return a non-existing path by appending a counter when needed."""

    if start < 0:
        raise ValueError("start must be non-negative.")
    if not connector:
        raise ValueError("connector must not be empty.")

    target = Path(path).expanduser()
    if not target.exists():
        return target

    suffix = "".join(target.suffixes)
    stem = target.name[: -len(suffix)] if suffix else target.name

    counter = start
    while True:
        candidate = target.with_name(f"{stem}{connector}{counter}{suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def safe_save(
    path: str | Path,
    data: Any,
    *,
    connector: str = "_",
    start: int = 1,
    serializer: str | None = None,
    atomic: bool = True,
    create_dirs: bool = True,
    indent: int | None = 2,
    sort_keys: bool = True,
    pickle_protocol: int = pickle.HIGHEST_PROTOCOL,
) -> Path:
    """Save data without overwriting an existing file."""

    target = _prepare_target(path, create_dirs=create_dirs)
    target = safe_path(target, connector=connector, start=start)
    return save(
        target,
        data,
        serializer=serializer,
        overwrite=False,
        atomic=atomic,
        create_dirs=create_dirs,
        indent=indent,
        sort_keys=sort_keys,
        pickle_protocol=pickle_protocol,
    )


def _git_cwd(path: str | Path | None = None) -> Path:
    """Return a directory suitable for running Git commands."""

    cwd = Path.cwd() if path is None else Path(path).expanduser()
    if not cwd.is_absolute():
        cwd = Path.cwd() / cwd
    cwd = cwd.resolve()
    return cwd.parent if cwd.is_file() else cwd


def _run_git(args: list[str], path: str | Path | None = None) -> str | None:
    """Run a Git command and return stripped stdout, or ``None`` on failure."""

    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=_git_cwd(path),
            capture_output=True,
            check=False,
            text=True,
        )
    except (FileNotFoundError, OSError):
        return None

    if completed.returncode != 0:
        return None

    return completed.stdout.strip()


def gitroot(path: str | Path | None = None) -> Path | None:
    """Return the Git repository root containing ``path``, if any."""

    root = _run_git(["rev-parse", "--show-toplevel"], path)
    return Path(root).resolve() if root else None


def isdirty(
    path: str | Path | None = None,
    *,
    include_untracked: bool = True,
) -> bool:
    """Return whether the Git repository has uncommitted changes."""

    args = ["status", "--porcelain"]
    if not include_untracked:
        args.append("--untracked-files=no")
    return bool(_run_git(args, path))


def gitpatch(
    path: str | Path | None = None,
    *,
    staged: bool = False,
) -> str:
    """Return the current Git diff for ``path``'s repository."""

    args = ["diff", "--staged"] if staged else ["diff"]
    return _run_git(args, path) or ""


def gitdescribe(path: str | Path | None = None) -> dict[str, Any]:
    """Return Git metadata for the repository containing ``path``."""

    root = gitroot(path)
    if root is None:
        return {
            "available": False,
            "root": None,
            "commit": None,
            "short_commit": None,
            "branch": None,
            "describe": None,
            "is_dirty": None,
            "remote_url": None,
        }

    return {
        "available": True,
        "root": str(root),
        "commit": _run_git(["rev-parse", "HEAD"], root),
        "short_commit": _run_git(["rev-parse", "--short", "HEAD"], root),
        "branch": _run_git(["branch", "--show-current"], root),
        "describe": _run_git(["describe", "--tags", "--always", "--dirty"], root),
        "is_dirty": isdirty(root),
        "remote_url": _run_git(["config", "--get", "remote.origin.url"], root),
    }


def tag(
    data: Any,
    *,
    key: str = DEFAULT_METADATA_KEY,
    path: str | Path | None = None,
    include_patch: bool = False,
    include_staged_patch: bool = False,
    copy_data: bool = True,
    extra: Mapping[str, Any] | None = None,
) -> Any:
    """Attach reproducibility metadata to ``data``.

    Mapping inputs are tagged under ``key``. Non-mapping inputs are wrapped in a
    dictionary under ``"data"``.
    """

    metadata: dict[str, Any] = {
        "package": "mrshudson",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git": gitdescribe(path),
    }
    if include_patch:
        metadata["git_patch"] = gitpatch(path)
    if include_staged_patch:
        metadata["git_staged_patch"] = gitpatch(path, staged=True)
    if extra:
        metadata.update(dict(extra))

    if isinstance(data, MutableMapping) and not copy_data:
        data[key] = metadata
        return data

    if isinstance(data, Mapping):
        tagged = dict(data)
        tagged[key] = metadata
        return tagged

    return {
        "data": data,
        key: metadata,
    }


def tag_save(
    path: str | Path,
    data: Any,
    *,
    key: str = DEFAULT_METADATA_KEY,
    git_path: str | Path | None = None,
    include_patch: bool = False,
    include_staged_patch: bool = False,
    safe: bool = False,
    extra: Mapping[str, Any] | None = None,
    serializer: str | None = None,
    overwrite: bool = True,
    atomic: bool = True,
    create_dirs: bool = True,
    indent: int | None = 2,
    sort_keys: bool = True,
    pickle_protocol: int = pickle.HIGHEST_PROTOCOL,
) -> Path:
    """Tag ``data`` with reproducibility metadata, save it, and return the path."""

    metadata_path = path if git_path is None else git_path
    tagged = tag(
        data,
        key=key,
        path=metadata_path,
        include_patch=include_patch,
        include_staged_patch=include_staged_patch,
        extra=extra,
    )

    if safe:
        return safe_save(
            path,
            tagged,
            serializer=serializer,
            atomic=atomic,
            create_dirs=create_dirs,
            indent=indent,
            sort_keys=sort_keys,
            pickle_protocol=pickle_protocol,
        )

    return save(
        path,
        tagged,
        serializer=serializer,
        overwrite=overwrite,
        atomic=atomic,
        create_dirs=create_dirs,
        indent=indent,
        sort_keys=sort_keys,
        pickle_protocol=pickle_protocol,
    )


wsave = save
"""DrWatson-style alias for :func:`save`."""

safesave = safe_save
"""DrWatson-style alias for :func:`safe_save`."""

tagsave = tag_save
"""DrWatson-style alias for :func:`tag_save`."""


__all__ = [
    "DEFAULT_METADATA_KEY",
    "JSON_SUFFIXES",
    "PICKLE_SUFFIXES",
    "SUPPORTED_SERIALIZERS",
    "gitdescribe",
    "gitpatch",
    "gitroot",
    "isdirty",
    "load",
    "safe_path",
    "safe_save",
    "safesave",
    "save",
    "tag",
    "tag_save",
    "tagsave",
    "wsave",
]
