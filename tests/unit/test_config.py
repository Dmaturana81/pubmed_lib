"""Config helper tests."""

import pytest

from pubmed_lib.config import get_from_env


def test_get_from_env_raises_when_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ENTREZ_EMAIL", raising=False)
    with pytest.raises(ValueError, match="ENTREZ_EMAIL"):
        get_from_env("email", "ENTREZ_EMAIL")


def test_get_from_env_returns_value(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ENTREZ_EMAIL", "test@example.com")
    assert get_from_env("email", "ENTREZ_EMAIL") == "test@example.com"
