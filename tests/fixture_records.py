"""Offline PubMed record fixtures mimicking Bio.Entrez parser output."""

from __future__ import annotations

from typing import Any


class EntrezString(str):
    """String value with Entrez-style attributes."""

    attributes: dict[str, str]

    def __new__(cls, value: str, attributes: dict[str, str] | None = None) -> EntrezString:
        obj = str.__new__(cls, value)
        obj.attributes = attributes or {}
        return obj


class EntrezElement(dict[str, Any]):
    """Minimal Entrez-like dict with attribute access."""

    attributes: dict[str, str]

    def __init__(self, attributes: dict[str, str] | None = None, **values: Any) -> None:
        super().__init__(values)
        self.attributes = attributes or {}


def minimal_article_record() -> dict[str, Any]:
    return {
        "MedlineCitation": EntrezElement(
            PMID="12345678",
            Article=EntrezElement(
                ArticleTitle="Minimal PubMed Article for Tests",
                Abstract=EntrezElement(
                    AbstractText=["This is a minimal abstract for parser tests."]
                ),
                Journal=EntrezElement(
                    Title="Journal of Testing",
                    JournalIssue=EntrezElement(
                        PubDate=EntrezElement(Year="2024", Month="Mar", Day="15")
                    ),
                ),
                AuthorList=[
                    EntrezElement(
                        attributes={"ValidYN": "Y"},
                        ForeName="Jane",
                        LastName="Smith",
                        Initials="J",
                        Identifier=[],
                        AffiliationInfo=[
                            EntrezElement(
                                Affiliation=(
                                    "Department of Biology, Example University, "
                                    "Boston, MA, USA. jane.smith@example.com"
                                )
                            )
                        ],
                    )
                ],
            ),
            KeywordList=[
                [
                    EntrezString("Testing", {"MajorTopicYN": "Y"}),
                    EntrezString("Control", {"MajorTopicYN": "N"}),
                ]
            ],
            MeshHeadingList=[
                EntrezElement(
                    DescriptorName=EntrezString("Testing", {"MajorTopicYN": "Y"})
                ),
                EntrezElement(
                    DescriptorName=EntrezString("Humans", {"MajorTopicYN": "N"})
                ),
            ],
        ),
        "PubmedData": EntrezElement(
            ArticleIdList=[
                EntrezString("12345678", {"IdType": "pubmed"}),
                EntrezString("10.1000/minimal.test", {"IdType": "doi"}),
                EntrezString("PMC999999", {"IdType": "pmc"}),
            ]
        ),
    }


def no_keywords_article_record() -> dict[str, Any]:
    return {
        "MedlineCitation": EntrezElement(
            PMID="23456789",
            Article=EntrezElement(
                ArticleTitle="Article Without Keywords",
                Journal=EntrezElement(
                    Title="Spring Journal",
                    JournalIssue=EntrezElement(
                        PubDate=EntrezElement(MedlineDate="2023 Spring")
                    ),
                ),
                AuthorList=[
                    EntrezElement(
                        attributes={"ValidYN": "Y"},
                        ForeName="John",
                        LastName="Doe",
                        Initials="J",
                        Identifier=[],
                        AffiliationInfo=[],
                    )
                ],
            ),
        ),
        "PubmedData": EntrezElement(
            ArticleIdList=[
                EntrezString("23456789", {"IdType": "pubmed"}),
            ]
        ),
    }


def structured_abstract_record() -> dict[str, Any]:
    return {
        "MedlineCitation": EntrezElement(
            PMID="34567890",
            Article=EntrezElement(
                ArticleTitle="Structured Abstract Article",
                Abstract=EntrezElement(
                    AbstractText=[
                        {"Label": "BACKGROUND", "#text": "Background section text."},
                        {"Label": "METHODS", "#text": "Methods section text."},
                        {"Label": "RESULTS", "#text": "Results section text."},
                    ]
                ),
                Journal=EntrezElement(
                    Title="Structured Abstract Journal",
                    JournalIssue=EntrezElement(PubDate=EntrezElement(Year="2022")),
                ),
                AuthorList=[
                    EntrezElement(
                        attributes={"ValidYN": "Y"},
                        ForeName="Chris",
                        LastName="Lee",
                        Initials="C",
                        Identifier=[],
                        AffiliationInfo=[],
                    )
                ],
            ),
        ),
        "PubmedData": EntrezElement(
            ArticleIdList=[
                EntrezString("34567890", {"IdType": "pubmed"}),
            ]
        ),
    }


def collective_author_record() -> dict[str, Any]:
    return {
        "MedlineCitation": EntrezElement(
            PMID="45678901",
            Article=EntrezElement(
                ArticleTitle="Collective Authorship Article",
                Journal=EntrezElement(
                    Title="Collective Author Journal",
                    JournalIssue=EntrezElement(PubDate=EntrezElement(Year="2021")),
                ),
                AuthorList=[
                    EntrezElement(
                        attributes={"ValidYN": "Y"},
                        CollectiveName="Consortium for Testing",
                    ),
                    EntrezElement(
                        attributes={"ValidYN": "Y"},
                        ForeName="Author",
                        LastName="Valid",
                        Initials="A",
                        Identifier=[],
                        AffiliationInfo=[],
                    ),
                ],
            ),
        ),
        "PubmedData": EntrezElement(
            ArticleIdList=[
                EntrezString("45678901", {"IdType": "pubmed"}),
            ]
        ),
    }
