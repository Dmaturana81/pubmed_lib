# PubMed MCP Server

Configure Cursor, Claude Desktop, or other MCP clients to search and fetch PubMed literature.

## Requirements

- Python 3.11+
- `ENTREZ_EMAIL` (required by NCBI)
- `ENTREZ_API_KEY` (optional, higher rate limits)
- `MCP_API_KEY` (required for SSE transport, minimum 32 characters)

## Install

```bash
uv add "pubmed-lib[mcp]"
```

## stdio (local agents)

```json
{
  "mcpServers": {
    "pubmed": {
      "command": "uvx",
      "args": ["pubmed-mcp"],
      "env": {
        "ENTREZ_EMAIL": "you@example.com",
        "ENTREZ_API_KEY": "optional"
      }
    }
  }
}
```

## SSE (remote agents)

```bash
MCP_API_KEY=your-long-secret-key ENTREZ_EMAIL=you@example.com \
  pubmed-mcp --transport sse --port 8000
```

Send `Authorization: Bearer <MCP_API_KEY>` or `X-API-Key: <MCP_API_KEY>` on each request.

## Tools

| Tool | Description |
|------|-------------|
| `pubmed_search` | Search and return PMIDs + metadata |
| `pubmed_fetch` | Fetch parsed articles by PMID list |
| `pubmed_search_fetch` | Search and fetch in one call |
| `pubmed_get_article` | Fetch one article |
| `pubmed_format_citation` | Format APA/Vancouver/BibTeX citation |

## Limits

- Default `max_results`: 20
- Hard cap: 200
- Responses are JSON with optional per-article `summary` fields

See also: [library.md](library.md)
