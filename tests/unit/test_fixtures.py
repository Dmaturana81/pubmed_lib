"""Fixture smoke tests."""

from tests.conftest import load_pubmed_fixture


def test_offline_fixtures_load() -> None:
    for name in (
        "pubmed_article_minimal.xml",
        "pubmed_article_no_keywords.xml",
        "pubmed_article_structured_abstract.xml",
        "pubmed_author_collective.xml",
    ):
        record = load_pubmed_fixture(name)
        assert "MedlineCitation" in record
        assert "PubmedData" in record
