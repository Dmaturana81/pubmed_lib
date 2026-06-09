# Contributing

## Setup

```bash
uv sync --all-extras --dev
```

## Checks

```bash
uv run ruff check src tests
uv run mypy src/pubmed_lib
uv run pytest --cov=pubmed_lib --cov-fail-under=80
```

## Source layout

- `src/pubmed_lib/` — core library (canonical)
- `src/pubmed_mcp/` — MCP server
- `nbs/` — legacy notebooks (examples only, do not export new code)
- `tests/` — unit, integration, MCP contract tests

## Obsidian wiki sync

On release/milestone, manually copy updated `docs/*.md` into the Obsidian vault `PubMedLib/` folder. Git docs are canonical.

## Environment

Never commit `.env`. Required variables:

- `ENTREZ_EMAIL`
- `ENTREZ_API_KEY` (optional)
- `MCP_API_KEY` (SSE only)
