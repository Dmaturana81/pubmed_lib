"""Citation formatter tests."""

from datetime import date

from pubmed_lib.citation import format_citation
from pubmed_lib.models import Article, Author


def _sample_article() -> Article:
    return Article(
        pmid="12345678",
        doi="10.1000/test",
        title="Sample Article",
        authors=[Author(name="Jane Smith")],
        journal="Test Journal",
        published=date(2024, 1, 1),
    )


def test_format_citation_apa() -> None:
    citation = format_citation(_sample_article(), style="apa")
    assert "Jane Smith" in citation
    assert "Sample Article" in citation


def test_format_citation_vancouver() -> None:
    citation = format_citation(_sample_article(), style="vancouver")
    assert citation.startswith("Jane Smith.")


def test_format_citation_bibtex() -> None:
    citation = format_citation(_sample_article(), style="bibtex")
    assert citation.startswith("@article{pmid12345678")
