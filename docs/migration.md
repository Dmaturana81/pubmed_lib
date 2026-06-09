# Migration Guide

## 0.0.x → 1.0.0

| Old | New |
|-----|-----|
| `Search()` | `PubMedClient()` |
| `Search.search()` | `PubMedClient.search()` |
| `Search.results()` | `PubMedClient.search_articles()` |
| `Result` | `Article` |
| `Autor` | `Author` |
| `pubmed` | `pmid` |
| `mayorKeys` | `keywords` |
| `mayorMesh` | `mesh_major` |
| `minorMesh` | `mesh_minor` |

Environment variables:

- Use `ENTREZ_EMAIL` instead of `EMAIL`
- Use `ENTREZ_API_KEY` (optional) instead of ad hoc names

LLM affiliation parsing moved to optional `[llm]` extra (1.0.1).
