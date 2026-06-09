"""Parse PubMed article metadata."""

from __future__ import annotations

import re
from datetime import date
from typing import Any


def _parse_published_date(article_info: dict[str, Any]) -> date | None:
    published_date = article_info["Journal"]["JournalIssue"]["PubDate"]
    article_dates = article_info.get("ArticleDate") or []
    if article_dates:
        date_dict = {key.lower(): int(value) for key, value in article_dates[0].items()}
        return date(**date_dict)
    if "Year" in published_date:
        return date(int(published_date["Year"]), 1, 1)
    if "MedlineDate" in published_date:
        medline_date = str(published_date["MedlineDate"])
        matches = re.findall(r"\d{4}", medline_date)
        if matches:
            return date(int(matches[0]), 1, 1)
        return date(int(medline_date[:4]), 1, 1)
    return None


def _parse_abstract(article_info: dict[str, Any]) -> str:
    abstract_info = article_info.get("Abstract") or {}
    abstract_parts = abstract_info.get("AbstractText") or []
    if not abstract_parts:
        return ""
    chunks: list[str] = []
    for part in abstract_parts:
        if isinstance(part, dict):
            label = part.get("Label")
            text = str(part.get("#text", part))
            chunks.append(f"{label}: {text}" if label else text)
        else:
            chunks.append(str(part))
    return ". ".join(chunk for chunk in chunks if chunk)


def parse_keywords(citation_info: dict[str, Any]) -> list[str]:
    """Parse author keywords marked as major topics."""
    keyword_list = citation_info.get("KeywordList") or []
    if not keyword_list:
        return []
    return [str(item) for item in keyword_list[0] if item.attributes.get("MajorTopicYN") == "Y"]


def parse_mesh_keys(citation_info: dict[str, Any]) -> tuple[list[str], list[str]]:
    """Parse major and minor MeSH descriptor names."""
    mesh_keys = citation_info.get("MeshHeadingList") or []
    mesh_major = [
        str(item["DescriptorName"])
        for item in mesh_keys
        if item["DescriptorName"].attributes.get("MajorTopicYN") == "Y"
    ]
    mesh_minor = [
        str(item["DescriptorName"])
        for item in mesh_keys
        if item["DescriptorName"].attributes.get("MajorTopicYN") == "N"
    ]
    return mesh_major, mesh_minor


def parse_article_fields(article_info: dict[str, Any]) -> dict[str, Any]:
    """Parse core article fields from MedlineCitation Article."""
    return {
        "title": str(article_info["ArticleTitle"]),
        "abstract": _parse_abstract(article_info),
        "journal": str(article_info["Journal"]["Title"]),
        "published": _parse_published_date(article_info),
        "author_xml_list": article_info.get("AuthorList") or [],
    }
