"""Parse PubMed article identifiers."""

from __future__ import annotations

from typing import Any


def parse_pubmed_ids(pubmed_data: dict[str, Any]) -> dict[str, str]:
    """Extract article identifiers from PubmedData."""
    article_ids = pubmed_data.get("ArticleIdList", [])
    ids: dict[str, str] = {}
    for item in article_ids:
        id_type = item.attributes.get("IdType")
        if id_type:
            ids[str(id_type)] = str(item)
    return ids
