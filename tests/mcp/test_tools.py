"""MCP tool handler tests."""

import json
from unittest.mock import MagicMock

import pytest

from pubmed_lib.models import Article, Author, SearchResponse
from pubmed_mcp.tools import PubMedTools


@pytest.fixture
def mock_client() -> MagicMock:
    client = MagicMock()
    client.search.return_value = SearchResponse(
        query="diabetes",
        query_used="diabetes[tiab]",
        total_available=100,
        returned=1,
        truncated=True,
        pmids=["12345678"],
    )
    article = Article(
        pmid="12345678",
        title="Sample",
        authors=[Author(name="Jane Smith")],
        journal="Test Journal",
    )
    client.fetch.return_value = [article]
    client.search_articles.return_value = SearchResponse(
        query="diabetes",
        query_used="diabetes[tiab]",
        total_available=100,
        returned=1,
        truncated=True,
        pmids=["12345678"],
        articles=[article],
    )
    client.get_article.return_value = article
    return client


def test_pubmed_search_returns_json_without_articles(mock_client: MagicMock) -> None:
    tools = PubMedTools(client=mock_client)
    payload = json.loads(tools.pubmed_search("diabetes"))
    assert payload["truncated"] is True
    assert payload["pmids"] == ["12345678"]
    assert payload["articles"] == []


def test_pubmed_fetch_returns_valid_articles(mock_client: MagicMock) -> None:
    tools = PubMedTools(client=mock_client)
    payload = json.loads(tools.pubmed_fetch(["12345678"]))
    article = PubMedTools.validate_article(payload["articles"][0])
    assert article.pmid == "12345678"


def test_pubmed_format_citation(mock_client: MagicMock) -> None:
    tools = PubMedTools(client=mock_client)
    payload = json.loads(tools.pubmed_format_citation("12345678", style="apa"))
    assert payload["style"] == "apa"
    assert "Jane Smith" in payload["citation"]
