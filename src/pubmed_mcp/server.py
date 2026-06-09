"""FastMCP server for PubMed literature review."""

from __future__ import annotations

import argparse
import sys

from fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from pubmed_mcp.auth import is_authorized_request, validate_sse_startup
from pubmed_mcp.tools import PubMedTools

INSTRUCTIONS = (
    "PubMed literature review tools. Requires ENTREZ_EMAIL. "
    "Default max_results is 20; hard cap is 200. "
    "Respect NCBI rate limits."
)


def create_mcp(tools: PubMedTools | None = None) -> FastMCP:
    """Create the FastMCP application with registered tools."""
    tool_impl = tools or PubMedTools()
    mcp = FastMCP(
        "pubmed",
        instructions=INSTRUCTIONS,
        version="1.0.0",
    )

    mcp.tool(name="pubmed_search")(tool_impl.pubmed_search)
    mcp.tool(name="pubmed_fetch")(tool_impl.pubmed_fetch)
    mcp.tool(name="pubmed_search_fetch")(tool_impl.pubmed_search_fetch)
    mcp.tool(name="pubmed_get_article")(tool_impl.pubmed_get_article)
    mcp.tool(name="pubmed_format_citation")(tool_impl.pubmed_format_citation)
    return mcp


class ApiKeyMiddleware(BaseHTTPMiddleware):
    """Require MCP API key for HTTP/SSE requests."""

    async def dispatch(self, request: Request, call_next):  # type: ignore[no-untyped-def]
        header_map = {key.lower(): value for key, value in request.headers.items()}
        if not is_authorized_request(header_map, required=True):
            return JSONResponse({"detail": "Unauthorized"}, status_code=401)
        return await call_next(request)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PubMed MCP server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="MCP transport mode",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host for SSE transport")
    parser.add_argument("--port", type=int, default=8000, help="Port for SSE transport")
    return parser


def main(argv: list[str] | None = None) -> None:
    """Run the MCP server."""
    args = build_parser().parse_args(argv)
    mcp = create_mcp()

    if args.transport == "sse":
        validate_sse_startup()
        if args.host == "0.0.0.0":
            print("Warning: binding to 0.0.0.0 exposes SSE without TLS.", file=sys.stderr)
        app = mcp.http_app(transport="sse", middleware=[Middleware(ApiKeyMiddleware)])
        import uvicorn

        uvicorn.run(app, host=args.host, port=args.port)
        return

    mcp.run(transport="stdio", show_banner=True)


if __name__ == "__main__":
    main()
