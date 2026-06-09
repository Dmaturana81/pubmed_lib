"""MCP tool handlers for PubMed literature review."""

from __future__ import annotations

import json
from typing import Any

from pubmed_lib.citation import format_citation
from pubmed_lib.client import PubMedClient
from pubmed_lib.constants import SEARCH_TAGS, SearchField, SortOrder
from pubmed_lib.models.article import Article
from pubmed_lib.models.search import SearchResponse


def _resolve_search_field(field: str) -> SearchField:
    if field in SEARCH_TAGS:
        return SearchField(field)
    for search_field in SearchField:
        if search_field.tag == field or search_field.value.lower() == field.lower():
            return search_field
    raise ValueError(f"Unknown search field: {field}")


def _dump_json(payload: Any) -> str:
    if hasattr(payload, "model_dump"):
        data = payload.model_dump(mode="json")
    else:
        data = payload
    return json.dumps(data, indent=2, default=str)


class PubMedTools:
    """Tool implementations backed by PubMedClient."""

    def __init__(self, client: PubMedClient | None = None) -> None:
        self._client = client or PubMedClient()

    def pubmed_search(
        self,
        query: str,
        field: str = "Title/Abstract",
        max_results: int = 20,
        min_year: int | None = None,
        max_year: int | None = None,
        sort: str = "relevance",
    ) -> str:
        """Search PubMed and return PMIDs plus search metadata."""
        response = self._client.search(
            query,
            field=_resolve_search_field(field),
            max_results=max_results,
            min_year=min_year,
            max_year=max_year,
            sort=SortOrder(sort),
        )
        payload = response.model_dump(mode="json")
        payload["articles"] = []
        return _dump_json(payload)

    def pubmed_fetch(self, pmids: list[str], max_articles: int = 20) -> str:
        """Fetch parsed articles for a list of PMIDs."""
        articles = self._client.fetch(pmids, max_articles=max_articles)
        return _dump_json(
            {
                "returned": len(articles),
                "articles": [article.model_dump(mode="json") for article in articles],
            }
        )

    def pubmed_search_fetch(
        self,
        query: str,
        field: str = "Title/Abstract",
        max_results: int = 20,
        min_year: int | None = None,
        max_year: int | None = None,
        sort: str = "relevance",
    ) -> str:
        """Search PubMed and return parsed articles."""
        response = self._client.search_articles(
            query,
            field=_resolve_search_field(field),
            max_results=max_results,
            min_year=min_year,
            max_year=max_year,
            sort=SortOrder(sort),
        )
        return _dump_json(response)

    def pubmed_get_article(self, pmid: str) -> str:
        """Fetch a single parsed article by PMID."""
        article = self._client.get_article(pmid)
        return _dump_json(article)

    def pubmed_format_citation(self, pmid: str, style: str = "apa") -> str:
        """Return a formatted citation for an article PMID."""
        article = self._client.get_article(pmid)
        return _dump_json(
            {
                "pmid": article.pmid,
                "style": style,
                "citation": format_citation(article, style=style),
            }
        )

    @staticmethod
    def validate_search_response(payload: dict[str, Any]) -> SearchResponse:
        return SearchResponse.model_validate(payload)

    @staticmethod
    def validate_article(payload: dict[str, Any]) -> Article:
        return Article.model_validate(payload)
