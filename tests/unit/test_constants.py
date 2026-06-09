"""Constants tests."""

from pubmed_lib.constants import SEARCH_TAGS, SearchField


def test_search_field_title_abstract_tag() -> None:
    assert SearchField.TITLE_ABSTRACT.tag == "[tiab]"
    assert SEARCH_TAGS["Title/Abstract"] == "[tiab]"
