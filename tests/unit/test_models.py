"""Model tests."""

from datetime import date

from pubmed_lib.models import Article, Author


def test_article_summary_is_generated() -> None:
    article = Article(
        pmid="1",
        title="Sample title",
        authors=[Author(name="Jane Smith")],
        journal="Test Journal",
        published=date(2024, 1, 1),
    )
    assert "Jane Smith" in article.summary
    assert "PMID 1" in article.summary


def test_author_email_optional() -> None:
    author = Author(name="Jane Smith", email=None)
    assert author.email is None
