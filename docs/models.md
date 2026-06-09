# Models

## Article

| Field | Type | Description |
|-------|------|-------------|
| `pmid` | str | PubMed ID |
| `pmc` | str \| null | PMC ID |
| `doi` | str \| null | DOI |
| `title` | str | Article title |
| `abstract` | str | Abstract text |
| `authors` | list[Author] | Author list |
| `journal` | str | Journal title |
| `published` | date \| null | Publication date |
| `keywords` | list[str] | Author keywords |
| `mesh_major` | list[str] | Major MeSH terms |
| `mesh_minor` | list[str] | Minor MeSH terms |
| `summary` | str | One-line summary for agents |

## Author

| Field | Type |
|-------|------|
| `name` | str |
| `forename` | str \| null |
| `lastname` | str \| null |
| `initials` | str \| null |
| `affiliation` | str \| null |
| `email` | str \| null |
| `orcid` | str \| null |

## SearchResponse

| Field | Type |
|-------|------|
| `query` | str |
| `query_used` | str |
| `total_available` | int |
| `returned` | int |
| `truncated` | bool |
| `pmids` | list[str] |
| `articles` | list[Article] |
