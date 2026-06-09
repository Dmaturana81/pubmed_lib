"""Citation formatting helpers."""

from __future__ import annotations

from pubmed_lib.models.article import Article


def format_citation(article: Article, style: str = "apa") -> str:
    """Format an article citation string."""
    style_key = style.lower()
    authors = article.authors
    author_text = authors[0].name if len(authors) == 1 else ", ".join(a.name for a in authors[:6])
    if len(authors) > 6:
        author_text = f"{author_text}, et al."
    year = article.published.year if article.published else "n.d."
    journal = article.journal or "Unknown journal"

    if style_key == "vancouver":
        return f"{author_text}. {article.title}. {journal}. {year}. PMID: {article.pmid}."
    if style_key == "bibtex":
        key = f"pmid{article.pmid}"
        doi_part = f",\n  doi = {{{article.doi}}}" if article.doi else ""
        return (
            f"@article{{{key},\n"
            f"  title = {{{article.title}}},\n"
            f"  author = {{{author_text}}},\n"
            f"  journal = {{{journal}}},\n"
            f"  year = {{{year}}},\n"
            f"  pmid = {{{article.pmid}}}{doi_part}\n"
            f"}}"
        )
    return f"{author_text} ({year}). {article.title}. {journal}. https://pubmed.ncbi.nlm.nih.gov/{article.pmid}/"
