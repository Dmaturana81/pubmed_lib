"""PubMedClient integration tests with mocked Entrez."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from tests.conftest import load_pubmed_fixture

from pubmed_lib.client import PubMedClient


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> PubMedClient:
    monkeypatch.setenv("ENTREZ_EMAIL", "test@example.com")
    return PubMedClient()


def test_search_articles_returns_truncated_flag(client: PubMedClient) -> None:
    search_result = {
        "IdList": ["12345678", "23456789"],
        "Count": "999",
    }
    fetch_result = {"PubmedArticle": [load_pubmed_fixture("pubmed_article_minimal.xml")]}

    with patch("pubmed_lib.client.Entrez.esearch", return_value=MagicMock()) as esearch, patch(
        "pubmed_lib.client.Entrez.read",
        side_effect=[search_result, fetch_result],
    ), patch("pubmed_lib.client.Entrez.efetch", return_value=MagicMock()):
        response = client.search_articles("diabetes", max_results=2)

    esearch.assert_called_once()
    assert response.returned == 2
    assert response.truncated is True
    assert response.total_available == 999
    assert len(response.articles) == 1
    assert response.articles[0].pmid == "12345678"


def test_get_article(client: PubMedClient) -> None:
    fetch_result = {"PubmedArticle": [load_pubmed_fixture("pubmed_article_minimal.xml")]}
    with patch("pubmed_lib.client.Entrez.efetch", return_value=MagicMock()), patch(
        "pubmed_lib.client.Entrez.read",
        return_value=fetch_result,
    ):
        article = client.get_article("12345678")
    assert article.pmid == "12345678"
