"""PubMed search field constants."""

from __future__ import annotations

from enum import StrEnum

SEARCH_TAGS: dict[str, str] = {
    "Affiliation": "[ad]",
    "All Fields": "[all]",
    "Article Identifier": "[aid]",
    "Author": "[au]",
    "Author Identifier": "[auid]",
    "EC/RN Number": "[rn]",
    "First Author Name": "[1au]",
    "Full Author Name": "[fau]",
    "Full Investigator Name": "[fir]",
    "Grant Number": "[gr]",
    "Investigator": "[ir]",
    "Journal": "[ta]",
    "Last Author Name": "[lastau]",
    "Location ID": "[lid]",
    "MeSH Major Topic": "[majr]",
    "MeSH Subheadings": "[sh]",
    "MeSH Terms": "[mh]",
    "Other Term": "[ot]",
    "PMID": "[pmid]",
    "Subset": "[sb]",
    "Text Words": "[tw]",
    "Title": "[ti]",
    "Title/Abstract": "[tiab]",
}


class SearchField(StrEnum):
    """Supported PubMed search fields."""

    AFFILIATION = "Affiliation"
    ALL_FIELDS = "All Fields"
    ARTICLE_IDENTIFIER = "Article Identifier"
    AUTHOR = "Author"
    AUTHOR_IDENTIFIER = "Author Identifier"
    EC_RN_NUMBER = "EC/RN Number"
    FIRST_AUTHOR_NAME = "First Author Name"
    FULL_AUTHOR_NAME = "Full Author Name"
    FULL_INVESTIGATOR_NAME = "Full Investigator Name"
    GRANT_NUMBER = "Grant Number"
    INVESTIGATOR = "Investigator"
    JOURNAL = "Journal"
    LAST_AUTHOR_NAME = "Last Author Name"
    LOCATION_ID = "Location ID"
    MESH_MAJOR_TOPIC = "MeSH Major Topic"
    MESH_SUBHEADINGS = "MeSH Subheadings"
    MESH_TERMS = "MeSH Terms"
    OTHER_TERM = "Other Term"
    PMID = "PMID"
    SUBSET = "Subset"
    TEXT_WORDS = "Text Words"
    TITLE = "Title"
    TITLE_ABSTRACT = "Title/Abstract"

    @property
    def tag(self) -> str:
        return SEARCH_TAGS[self.value]


class SortOrder(StrEnum):
    """PubMed esearch sort options."""

    RELEVANCE = "relevance"
    DATE = "pub_date"
    FIRST_AUTHOR = "first_author"
    JOURNAL = "journal"
    TITLE = "title"
