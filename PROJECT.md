# pubmed_lib

## Overview

PubMed search/fetch/parse library with optional FastMCP server for AI agents.

## Architecture

- `src/pubmed_lib/` — core client, parser, models
- `src/pubmed_mcp/` — FastMCP server (M2)
- `tests/` — unit, integration, MCP contract tests
- `fixtures/` — PubMed XML samples

## Development

```bash
uv sync --dev
uv run pytest
uv run ruff check src tests
uv run mypy src/pubmed_lib
```

## Environment

- `ENTREZ_EMAIL` (required)
- `ENTREZ_API_KEY` (optional)
- `MCP_API_KEY` (required for SSE transport)

## Current State

M1 (`1.0.0-alpha`): core library refactor in progress.

Spec: `docs/EXECUTION_MANIFEST.md`
