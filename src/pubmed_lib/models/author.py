"""Author model."""

from __future__ import annotations

from pydantic import BaseModel, field_validator


class Author(BaseModel):
    """Parsed publication author."""

    name: str
    forename: str | None = None
    lastname: str | None = None
    initials: str | None = None
    affiliation: str | None = None
    email: str | None = None
    orcid: str | None = None

    @field_validator("name", "forename", "lastname", "initials", "affiliation", mode="before")
    @classmethod
    def normalize_optional_str(cls, value: object) -> object:
        if value is None or value == "":
            return None
        return str(value).strip()
