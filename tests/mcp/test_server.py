"""MCP server tests."""

import asyncio
from unittest.mock import MagicMock

import pytest
from starlette.middleware import Middleware
from starlette.testclient import TestClient

from pubmed_mcp.server import ApiKeyMiddleware, build_parser, create_mcp
from pubmed_mcp.tools import PubMedTools


@pytest.fixture
def mcp_server(monkeypatch: pytest.MonkeyPatch) -> object:
    monkeypatch.setenv("ENTREZ_EMAIL", "test@example.com")
    mock_client = MagicMock()
    return create_mcp(PubMedTools(client=mock_client))


def test_create_mcp_registers_five_tools(mcp_server: object) -> None:
    tools = asyncio.run(mcp_server.get_tools())
    names = {tool.name for tool in tools.values()}
    assert names == {
        "pubmed_search",
        "pubmed_fetch",
        "pubmed_search_fetch",
        "pubmed_get_article",
        "pubmed_format_citation",
    }


def test_sse_app_rejects_unauthenticated_request(
    mcp_server: object, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("MCP_API_KEY", "x" * 32)
    app = mcp_server.http_app(transport="sse", middleware=[Middleware(ApiKeyMiddleware)])
    response = TestClient(app).get("/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


def test_cli_supports_stdio_and_sse() -> None:
    parser = build_parser()
    stdio_args = parser.parse_args([])
    sse_args = parser.parse_args(["--transport", "sse", "--port", "9000"])
    assert stdio_args.transport == "stdio"
    assert sse_args.transport == "sse"
    assert sse_args.port == 9000
