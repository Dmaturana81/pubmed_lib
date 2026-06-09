"""Search response model."""

from __future__ import annotations

from pydantic import BaseModel, Field

from pubmed_lib.models.article import Article


class SearchResponse(BaseModel):
    """PubMed search results envelope."""

    query: str
    query_used: str
    total_available: int
    returned: int
    truncated: bool
    pmids: list[str] = Field(default_factory=list)
    articles: list[Article] = Field(default_factory=list)
