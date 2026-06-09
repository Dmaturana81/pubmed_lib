"""Article model."""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field, model_validator

from pubmed_lib.models.author import Author


def build_summary(
    title: str,
    authors: list[Author],
    journal: str,
    published: date | None,
    pmid: str,
) -> str:
    """Build a short one-line article summary."""
    author_label = authors[0].name if authors else "Unknown author"
    year = published.year if published else "n.d."
    journal_label = journal or "Unknown journal"
    short_title = title if len(title) <= 120 else f"{title[:117]}..."
    return f"{author_label} ({year}) — {short_title} in {journal_label}. [PMID {pmid}]"


class Article(BaseModel):
    """Parsed PubMed article."""

    pmid: str
    pmc: str | None = None
    doi: str | None = None
    pii: str | None = None
    title: str
    abstract: str = ""
    authors: list[Author] = Field(default_factory=list)
    journal: str = ""
    published: date | None = None
    keywords: list[str] = Field(default_factory=list)
    mesh_major: list[str] = Field(default_factory=list)
    mesh_minor: list[str] = Field(default_factory=list)
    summary: str = ""

    @model_validator(mode="after")
    def populate_summary(self) -> Article:
        if not self.summary:
            self.summary = build_summary(
                self.title,
                self.authors,
                self.journal,
                self.published,
                self.pmid,
            )
        return self
