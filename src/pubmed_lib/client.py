"""PubMed Entrez client."""

from __future__ import annotations

from Bio import Entrez

from pubmed_lib.config import get_from_env
from pubmed_lib.constants import SearchField, SortOrder
from pubmed_lib.models.article import Article
from pubmed_lib.models.search import SearchResponse
from pubmed_lib.parser import parse_entrez_article
from pubmed_lib.rate_limit import RateLimiter, validate_max_results


class PubMedClient:
    """Search and fetch articles from PubMed via Entrez."""

    def __init__(self, email: str | None = None, api_key: str | None = None) -> None:
        self.email = email or get_from_env("email", "ENTREZ_EMAIL")
        self.api_key = api_key or get_from_env("api_key", "ENTREZ_API_KEY", default="") or None
        self._rate_limiter = RateLimiter(has_api_key=bool(self.api_key))
        setattr(Entrez, "email", self.email)
        if self.api_key:
            setattr(Entrez, "api_key", self.api_key)

    def search(
        self,
        query: str,
        *,
        field: SearchField = SearchField.TITLE_ABSTRACT,
        max_results: int = 20,
        min_year: int | None = None,
        max_year: int | None = None,
        sort: SortOrder = SortOrder.RELEVANCE,
    ) -> SearchResponse:
        """Search PubMed and return matching PMIDs."""
        max_results = validate_max_results(max_results)
        query_used = f"{query}{field.tag}"
        self._rate_limiter.acquire()
        handle = Entrez.esearch(
            db="pubmed",
            term=query_used,
            retmax=max_results,
            retmode="xml",
            sort=sort.value,
            mindate=min_year,
            maxdate=max_year,
        )
        results = Entrez.read(handle)
        pmids = [str(pmid) for pmid in results.get("IdList", [])]
        total_available = int(results.get("Count", len(pmids)))
        returned = len(pmids)
        return SearchResponse(
            query=query,
            query_used=query_used,
            total_available=total_available,
            returned=returned,
            truncated=total_available > returned,
            pmids=pmids,
        )

    def fetch(self, pmids: list[str], *, max_articles: int = 20) -> list[Article]:
        """Fetch and parse article details for the given PMIDs."""
        if not pmids:
            return []
        max_articles = validate_max_results(max_articles)
        limited_pmids = [str(pmid) for pmid in pmids[:max_articles]]
        self._rate_limiter.acquire()
        handle = Entrez.efetch(
            db="pubmed",
            id=",".join(limited_pmids),
            retmode="xml",
        )
        results = Entrez.read(handle)
        articles = results.get("PubmedArticle") or []
        return [parse_entrez_article(article) for article in articles]

    def search_articles(
        self,
        query: str,
        *,
        field: SearchField = SearchField.TITLE_ABSTRACT,
        max_results: int = 20,
        min_year: int | None = None,
        max_year: int | None = None,
        sort: SortOrder = SortOrder.RELEVANCE,
    ) -> SearchResponse:
        """Search PubMed and fetch parsed article records."""
        search_response = self.search(
            query,
            field=field,
            max_results=max_results,
            min_year=min_year,
            max_year=max_year,
            sort=sort,
        )
        search_response.articles = self.fetch(search_response.pmids, max_articles=max_results)
        return search_response

    def get_article(self, pmid: str) -> Article:
        """Fetch a single article by PMID."""
        articles = self.fetch([pmid], max_articles=1)
        if not articles:
            raise ValueError(f"No article found for PMID {pmid}")
        return articles[0]
