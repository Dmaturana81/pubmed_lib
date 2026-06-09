"""Parse PubMed author records."""

from __future__ import annotations

from typing import Any

from pubmed_lib.affiliation import extract_email


def parse_author_xml(author_xml: dict[str, Any]) -> dict[str, Any] | None:
    """Parse a single Entrez author record into Author fields."""
    if "CollectiveName" in author_xml:
        return None

    identifiers = author_xml.get("Identifier") or []
    orcid = str(identifiers[0]) if identifiers else None

    affiliation_infos = author_xml.get("AffiliationInfo") or []
    affiliation = ";".join(
        str(info["Affiliation"]) for info in affiliation_infos if info.get("Affiliation")
    )

    forename = str(author_xml.get("ForeName", "")).strip()
    lastname = str(author_xml.get("LastName", "")).strip()
    initials = str(author_xml.get("Initials", "")).strip() or None
    name = f"{forename} {lastname}".strip()

    return {
        "name": name,
        "forename": forename or None,
        "lastname": lastname or None,
        "initials": initials,
        "affiliation": affiliation or None,
        "email": extract_email(affiliation),
        "orcid": orcid,
    }
