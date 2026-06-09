"""MCP auth tests."""

import pytest

from pubmed_mcp.auth import get_mcp_api_key, is_authorized_request, validate_sse_startup


def test_get_mcp_api_key_requires_minimum_length(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MCP_API_KEY", "short")
    with pytest.raises(ValueError, match="32"):
        get_mcp_api_key()


def test_is_authorized_request_accepts_bearer(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MCP_API_KEY", "x" * 32)
    headers = {"authorization": f"Bearer {'x' * 32}"}
    assert is_authorized_request(headers, required=True) is True


def test_is_authorized_request_rejects_missing_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MCP_API_KEY", "x" * 32)
    assert is_authorized_request({}, required=True) is False


def test_validate_sse_startup_exits_without_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MCP_API_KEY", raising=False)
    with pytest.raises(SystemExit):
        validate_sse_startup()
