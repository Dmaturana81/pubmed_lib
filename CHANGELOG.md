# Changelog

## 1.0.0

- FastMCP server with five literature-review tools (stdio + SSE)
- SSE protected by `MCP_API_KEY`
- New `src/` layout with `PubMedClient`, `Article`, `Author` models
- uv-based packaging and CI

## 1.0.0-alpha

- New `src/` layout managed by uv
- `PubMedClient` replaces `Search`
- `Article` / `Author` replace `Result` / `Autor`
- Deterministic parser without LLM dependency
- Rate limiting and NCBI-safe defaults

## 0.0.3

- Legacy nbdev alpha release
