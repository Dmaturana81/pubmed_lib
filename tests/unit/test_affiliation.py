"""Affiliation helper tests."""

from pubmed_lib.affiliation import extract_email


def test_extract_email_finds_subdomain_address() -> None:
    assert extract_email("Contact user@mail.example.com for details.") == "user@mail.example.com"


def test_extract_email_returns_none_when_missing() -> None:
    assert extract_email("No email here") is None
