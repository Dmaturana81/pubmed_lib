"""Parser tests."""

from datetime import date

from pubmed_lib.parser import parse_entrez_article
from pubmed_lib.parser.ids import parse_pubmed_ids


def test_parse_pubmed_ids(minimal_article_record: dict) -> None:
    ids = parse_pubmed_ids(minimal_article_record["PubmedData"])
    assert ids["pubmed"] == "12345678"
    assert ids["doi"] == "10.1000/minimal.test"
    assert ids["pmc"] == "PMC999999"


def test_parse_entrez_article_minimal(minimal_article_record: dict) -> None:
    article = parse_entrez_article(minimal_article_record)
    assert article.pmid == "12345678"
    assert article.authors[0].email == "jane.smith@example.com"
    assert article.keywords == ["Testing"]
    assert "Testing" in article.mesh_major


def test_parse_entrez_article_without_keywords(no_keywords_article_record: dict) -> None:
    article = parse_entrez_article(no_keywords_article_record)
    assert article.keywords == []
    assert article.published == date(2023, 1, 1)


def test_parse_entrez_article_structured_abstract(structured_abstract_record: dict) -> None:
    article = parse_entrez_article(structured_abstract_record)
    assert "BACKGROUND:" in article.abstract
    assert "METHODS:" in article.abstract


def test_parse_entrez_article_skips_collective_author(collective_author_record: dict) -> None:
    article = parse_entrez_article(collective_author_record)
    assert len(article.authors) == 1
    assert article.authors[0].name == "Author Valid"
