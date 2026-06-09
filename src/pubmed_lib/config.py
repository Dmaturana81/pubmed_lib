"""Environment and configuration helpers."""

from __future__ import annotations

import os
from typing import Any


def get_from_env(key: str, env_key: str, default: str | None = None) -> str:
    """Return a value from an environment variable or raise."""
    if env_key in os.environ and os.environ[env_key]:
        return os.environ[env_key]
    if default is not None:
        return default
    raise ValueError(
        f"Did not find {key}, please add an environment variable "
        f"`{env_key}` which contains it, or pass `{key}` as a named parameter."
    )


def get_from_dict_or_env(
    data: dict[str, Any],
    key: str,
    env_key: str,
    default: str | None = None,
) -> str:
    """Return a value from a mapping or environment variable."""
    if key in data and data[key]:
        return str(data[key])
    return get_from_env(key, env_key, default=default)
