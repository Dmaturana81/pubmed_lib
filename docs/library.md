# PubMed Library

Python client for searching, fetching, and parsing PubMed articles.

## Install

```bash
uv add pubmed-lib
```

## Quickstart

```python
from pubmed_lib import PubMedClient

client = PubMedClient(email="you@example.com")
response = client.search_articles("diabetes", max_results=5)
for article in response.articles:
    print(article.summary)
```

## Environment

- `ENTREZ_EMAIL` (required)
- `ENTREZ_API_KEY` (optional, higher NCBI rate limits)

## API

- `PubMedClient.search()` — PMIDs only
- `PubMedClient.fetch()` — parse articles from PMIDs
- `PubMedClient.search_articles()` — search + fetch
- `PubMedClient.get_article()` — single PMID

See [[docs/models.md]] for response schemas.
