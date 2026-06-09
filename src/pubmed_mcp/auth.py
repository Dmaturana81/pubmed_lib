"""MCP SSE authentication helpers."""

from __future__ import annotations

import os
import sys

MIN_API_KEY_LENGTH = 32


def get_mcp_api_key() -> str:
    """Return the configured MCP API key or raise."""
    api_key = os.environ.get("MCP_API_KEY", "")
    if len(api_key) < MIN_API_KEY_LENGTH:
        raise ValueError(
            "MCP_API_KEY must be set and at least "
            f"{MIN_API_KEY_LENGTH} characters for SSE transport."
        )
    return api_key


def validate_sse_startup() -> None:
    """Ensure SSE mode has a valid API key before serving."""
    try:
        get_mcp_api_key()
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1) from exc


def is_authorized_request(headers: dict[str, str], *, required: bool) -> bool:
    """Check Authorization or X-API-Key headers when auth is required."""
    if not required:
        return True
    expected = get_mcp_api_key()
    auth_header = headers.get("authorization", "")
    if auth_header.lower().startswith("bearer "):
        token = auth_header[7:].strip()
        return token == expected
    api_key = headers.get("x-api-key", "")
    return api_key == expected
