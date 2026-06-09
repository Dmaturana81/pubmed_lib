"""Affiliation text helpers."""

from __future__ import annotations

import re

EMAIL_PATTERN = re.compile(
    r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+"
)


def extract_email(text: str) -> str | None:
    """Extract the first email address from affiliation text."""
    if not text:
        return None
    match = EMAIL_PATTERN.search(text)
    if match is None:
        return None
    return match.group(0).strip(".;,")
