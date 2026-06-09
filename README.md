# pubmed-lib

PubMed search, fetch, and parse for Python apps and AI agents.

## MCP quickstart

```bash
uv add "pubmed-lib[mcp]"
export ENTREZ_EMAIL=you@example.com
pubmed-mcp
```

Add to Cursor `mcp.json` (local repo — adjust path):

```json
{
  "mcpServers": {
    "pubmed": {
      "command": "uv",
      "args": ["--directory", "/Users/matu/Xcode/pubmed_lib", "run", "pubmed-mcp"],
      "env": {
        "ENTREZ_EMAIL": "you@example.com"
      }
    }
  }
}
```

After PyPI publish, you can use `"command": "uvx", "args": ["pubmed-mcp"]` instead.

Remote SSE:

```bash
MCP_API_KEY=<32+ chars> ENTREZ_EMAIL=you@example.com \
  pubmed-mcp --transport sse --port 8000
```

See [docs/mcp.md](docs/mcp.md) for tool reference and security notes.

## Python library

```bash
uv add pubmed-lib
```

```python
from pubmed_lib import PubMedClient

client = PubMedClient(email="you@example.com")
response = client.search_articles("diabetes", max_results=5)
for article in response.articles:
    print(article.summary)
```

See [docs/library.md](docs/library.md) and [docs/models.md](docs/models.md).

## Development

```bash
uv sync --all-extras --dev
uv run pytest
```

See [docs/contributing.md](docs/contributing.md) and [MIGRATION.md](MIGRATION.md).

## License

Apache-2.0
