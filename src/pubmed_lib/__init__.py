"""PubMed library for search, fetch, and parse."""

from pubmed_lib.client import PubMedClient
from pubmed_lib.models import Article, Author, SearchResponse

__all__ = ["PubMedClient", "Article", "Author", "SearchResponse"]
__version__ = "1.0.0"
