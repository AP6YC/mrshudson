"""Deterministic names for parameter containers."""

from __future__ import annotations

import dataclasses
from collections.abc import Iterable, Mapping
from datetime import date, datetime, time
from pathlib import Path
from typing import Any, Callable

DEFAULT_ALLOWED_TYPES = (int, float, bool, str, date, datetime, time)
"""Types included in names by default."""


def _as_mapping(config: Any) -> Mapping[str, Any]:
    """Return a string-keyed mapping view of a supported config container."""

    if isinstance(config, Mapping):
        return config

    if dataclasses.is_dataclass(config) and not isinstance(config, type):
        return dataclasses.asdict(config)

    if hasattr(config, "_asdict"):
        return config._asdict()

    if hasattr(config, "__dict__"):
        return {
            key: value
            for key, value in vars(config).items()
            if not key.startswith("_")
        }

    raise TypeError(
        "savename expects a mapping, dataclass instance, namedtuple, or object "
        f"with public attributes; got {type(config).__name__}."
    )


def _format_value(
    value: Any,
    *,
    digits: int | None,
    sigdigits: int | None,
    val_to_string: Callable[[Any], str] | None,
) -> str:
    """Format a supported value deterministically."""

    if val_to_string is not None:
        return str(val_to_string(value))

    if isinstance(value, bool):
        return str(value).lower()

    if isinstance(value, float):
        if digits is not None:
            return str(round(value, digits))
        if sigdigits is not None:
            return f"{value:.{sigdigits}g}"

    if isinstance(value, (date, datetime, time)):
        return value.isoformat()

    return str(value)


def _sanitize_component(value: str) -> str:
    """Remove path separators and null bytes from a name component."""

    return value.replace("\x00", "").replace("/", "-").replace("\\", "-")


def _parse_value(value: str, parsetypes: Iterable[type]) -> Any:
    """Parse a string value using bool, then ``parsetypes``, then string."""

    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False

    for parser in parsetypes:
        try:
            return parser(value)
        except (TypeError, ValueError):
            continue

    return value


def savename(
    config: Any,
    *,
    prefix: str = "",
    suffix: str = "",
    sort: bool = True,
    digits: int | None = None,
    sigdigits: int | None = 3,
    connector: str = "_",
    equals: str = "=",
    allowedtypes: tuple[type, ...] = DEFAULT_ALLOWED_TYPES,
    accesses: Iterable[str] | None = None,
    ignores: Iterable[str] | None = None,
    expand: Iterable[str] | None = None,
    val_to_string: Callable[[Any], str] | None = None,
    sanitize: bool = True,
) -> str:
    """Create a deterministic shorthand name from a parameter container.

    Args:
        config: Mapping, dataclass instance, namedtuple, or object with public
            attributes.
        prefix: Optional prefix added before the generated key-value parts.
        suffix: Optional filename suffix. The leading dot is optional.
        sort: Sort keys alphabetically before naming.
        digits: Decimal digits for rounding floats.
        sigdigits: Significant digits for formatting floats when ``digits`` is
            not set.
        connector: String used between entries.
        equals: String used between keys and values.
        allowedtypes: Value types included in names.
        accesses: Explicit keys to include. Defaults to all available keys.
        ignores: Keys to exclude even when present in ``accesses``.
        expand: Keys whose nested container values should be named recursively.
        val_to_string: Optional custom value formatter.
        sanitize: Replace path separators in generated components.
    """

    if not connector:
        raise ValueError("connector must not be empty.")
    if not equals:
        raise ValueError("equals must not be empty.")

    mapping = _as_mapping(config)
    ignore_set = {str(key) for key in (ignores or ())}
    expand_set = {str(key) for key in (expand or ())}
    keys = list(accesses) if accesses is not None else list(mapping.keys())
    if sort:
        keys = sorted(keys, key=str)

    parts: list[str] = []
    for key in keys:
        key_string = str(key)
        if key_string in ignore_set or key not in mapping:
            continue

        value = mapping[key]
        if key_string in expand_set:
            try:
                value_string = savename(
                    value,
                    sort=sort,
                    digits=digits,
                    sigdigits=sigdigits,
                    connector=connector,
                    equals=equals,
                    allowedtypes=allowedtypes,
                    val_to_string=val_to_string,
                    sanitize=sanitize,
                )
            except TypeError:
                continue
            if not value_string:
                continue
        elif not isinstance(value, allowedtypes):
            continue
        else:
            value_string = _format_value(
                value,
                digits=digits,
                sigdigits=sigdigits,
                val_to_string=val_to_string,
            )

        if sanitize:
            key_string = _sanitize_component(key_string)
            value_string = _sanitize_component(value_string)

        parts.append(f"{key_string}{equals}{value_string}")

    if prefix:
        parts.insert(0, _sanitize_component(prefix) if sanitize else prefix)

    name = connector.join(parts)
    if suffix:
        suffix = suffix[1:] if suffix.startswith(".") else suffix
        name = f"{name}.{suffix}" if name else f".{suffix}"

    return name


def parse_savename(
    filename: str | Path,
    *,
    connector: str = "_",
    equals: str = "=",
    parsetypes: Iterable[type] = (int, float),
) -> tuple[str, dict[str, Any], str]:
    """Parse a name produced by :func:`savename`.

    Returns:
        A ``(prefix, parameters, suffix)`` tuple. Values are parsed as bool,
        then by ``parsetypes``, and finally left as strings.
    """

    if not connector:
        raise ValueError("connector must not be empty.")
    if not equals:
        raise ValueError("equals must not be empty.")

    name = Path(filename).name
    body, separator, suffix_candidate = name.rpartition(".")
    if (
        separator
        and connector not in suffix_candidate
        and equals not in suffix_candidate
    ):
        suffix = suffix_candidate
    else:
        body = name
        suffix = ""

    prefix_parts: list[str] = []
    parameters: dict[str, Any] = {}
    found_parameter = False

    for part in body.split(connector):
        if equals not in part:
            if not found_parameter:
                prefix_parts.append(part)
            continue

        found_parameter = True
        key, value = part.split(equals, 1)
        parameters[key] = _parse_value(value, parsetypes)

    return connector.join(prefix_parts), parameters, suffix


__all__ = [
    "DEFAULT_ALLOWED_TYPES",
    "parse_savename",
    "savename",
]
