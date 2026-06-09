"""Shared pytest fixtures."""

from __future__ import annotations

import pytest

from tests import fixture_records


def load_pubmed_fixture(name: str) -> dict:
    """Load a named offline PubMed article record."""
    fixtures = {
        "pubmed_article_minimal.xml": fixture_records.minimal_article_record,
        "pubmed_article_no_keywords.xml": fixture_records.no_keywords_article_record,
        "pubmed_article_structured_abstract.xml": fixture_records.structured_abstract_record,
        "pubmed_author_collective.xml": fixture_records.collective_author_record,
    }
    return fixtures[name]()


@pytest.fixture
def minimal_article_record() -> dict:
    return load_pubmed_fixture("pubmed_article_minimal.xml")


@pytest.fixture
def no_keywords_article_record() -> dict:
    return load_pubmed_fixture("pubmed_article_no_keywords.xml")


@pytest.fixture
def structured_abstract_record() -> dict:
    return load_pubmed_fixture("pubmed_article_structured_abstract.xml")


@pytest.fixture
def collective_author_record() -> dict:
    return load_pubmed_fixture("pubmed_author_collective.xml")
