"""Parser pipeline for Entrez PubmedArticle records."""

from __future__ import annotations

from typing import Any

from pubmed_lib.models.article import Article
from pubmed_lib.models.author import Author
from pubmed_lib.parser.article import (
    parse_article_fields,
    parse_keywords,
    parse_mesh_keys,
)
from pubmed_lib.parser.author import parse_author_xml
from pubmed_lib.parser.ids import parse_pubmed_ids


def parse_entrez_article(record: dict[str, Any]) -> Article:
    """Parse a Bio.Entrez PubmedArticle dict into an Article model."""
    pubmed_data = record["PubmedData"]
    medline_citation = record["MedlineCitation"]
    article_info = medline_citation["Article"]

    ids = parse_pubmed_ids(pubmed_data)
    article_fields = parse_article_fields(article_info)
    keywords = parse_keywords(medline_citation)
    mesh_major, mesh_minor = parse_mesh_keys(medline_citation)

    authors: list[Author] = []
    for author_xml in article_fields["author_xml_list"]:
        if author_xml.attributes.get("ValidYN") == "N":
            continue
        author_data = parse_author_xml(author_xml)
        if author_data is None:
            continue
        authors.append(Author.model_validate(author_data))

    pmid = ids.get("pubmed") or str(medline_citation["PMID"])
    return Article.model_validate(
        {
            "pmid": pmid,
            "pmc": ids.get("pmc"),
            "doi": ids.get("doi"),
            "pii": ids.get("pii"),
            "title": article_fields["title"],
            "abstract": article_fields["abstract"],
            "authors": authors,
            "journal": article_fields["journal"],
            "published": article_fields["published"],
            "keywords": keywords,
            "mesh_major": mesh_major,
            "mesh_minor": mesh_minor,
        }
    )
