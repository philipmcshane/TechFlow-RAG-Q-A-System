"""Tests for ingest.py — _section_documents section-splitting logic.

These are pure Python tests.
"""

from langchain_core.documents import Document
from ingest import _section_documents


def _doc(text: str, source: str = "test.md") -> Document:
    return Document(page_content=text, metadata={"source": source})


#  Section splitting 
def test_single_section_heading():
    sections = _section_documents(_doc("## Pricing\n\nWe have three plans."))
    assert len(sections) == 1
    assert sections[0].metadata["section"] == "Pricing"


def test_multiple_sections_names():
    text = (
        "## Section One\n\nContent one.\n\n"
        "## Section Two\n\nContent two."
    )
    sections = _section_documents(_doc(text))
    assert [s.metadata["section"] for s in sections] == ["Section One", "Section Two"]


def test_no_headings_defaults_to_overview():
    sections = _section_documents(_doc("Plain text with no headings."))
    assert len(sections) == 1
    assert sections[0].metadata["section"] == "Overview"


def test_preamble_before_first_heading_is_excluded():
    """Empty content before the first ## heading should be filtered out."""
    text = "\n\n## Real Section\n\nActual content here."
    sections = _section_documents(_doc(text))
    assert len(sections) == 1
    assert sections[0].metadata["section"] == "Real Section"


def test_h1_heading_becomes_overview_preamble():
    """Single-hash headings (#) don't start a new section — they land in Overview."""
    text = "# Document Title\n\n## Section A\n\nContent."
    sections = _section_documents(_doc(text))
    # Overview preamble carries the H1 line; Section A carries the content
    assert len(sections) == 2
    assert sections[0].metadata["section"] == "Overview"
    assert "Document Title" in sections[0].page_content
    assert sections[1].metadata["section"] == "Section A"


#  Metadata propagation
def test_source_metadata_inherited():
    sections = _section_documents(_doc("## FAQ\n\nSome content.", source="faq.md"))
    assert sections[0].metadata["source"] == "faq.md"


def test_section_metadata_key_set():
    sections = _section_documents(_doc("## About\n\nInfo."))
    assert "section" in sections[0].metadata


# Content integrity 
def test_no_empty_sections_returned():
    """The filter at the end of _section_documents drops any empty-content documents."""
    text = "\n\n## Heading\n\nContent."
    sections = _section_documents(_doc(text))
    assert all(s.page_content.strip() for s in sections)


def test_content_preserved_across_split():
    text = "## Uptime\n\nWe guarantee 99.9% uptime."
    sections = _section_documents(_doc(text))
    assert "99.9%" in sections[0].page_content


def test_three_sections_correct_count():
    text = (
        "## Alpha\n\nAlpha content.\n\n"
        "## Beta\n\nBeta content.\n\n"
        "## Gamma\n\nGamma content."
    )
    sections = _section_documents(_doc(text))
    assert len(sections) == 3
