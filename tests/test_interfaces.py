"""Tests for the shared value objects in :mod:`research_agent.interfaces`."""

from __future__ import annotations

import pytest

from research_agent.interfaces import (
    Chunk,
    Citation,
    Document,
    Report,
    Summary,
)


@pytest.mark.unit
class TestDocument:
    def test_creation_with_required_fields(self) -> None:
        doc = Document(id="d1", content="text")
        assert doc.id == "d1"
        assert doc.content == "text"
        assert doc.metadata == {}

    def test_creation_with_metadata(self) -> None:
        doc = Document(id="d2", content="body", metadata={"url": "https://example.com"})
        assert doc.metadata["url"] == "https://example.com"

    def test_frozen(self) -> None:
        from dataclasses import FrozenInstanceError

        doc = Document(id="d3", content="c")
        with pytest.raises(FrozenInstanceError):
            doc.id = "new-id"  # type: ignore[misc]


@pytest.mark.unit
class TestChunk:
    def test_creation(self, sample_chunk: Chunk) -> None:
        assert sample_chunk.document_id == "doc-1"
        assert sample_chunk.content == "Hello, world!"

    def test_frozen(self, sample_chunk: Chunk) -> None:
        from dataclasses import FrozenInstanceError

        with pytest.raises(FrozenInstanceError):
            sample_chunk.content = "mutated"  # type: ignore[misc]


@pytest.mark.unit
class TestCitation:
    def test_creation(self, sample_citation: Citation) -> None:
        assert sample_citation.document_id == "doc-1"
        assert sample_citation.raw_text == "Author et al., 2024"

    def test_default_metadata(self) -> None:
        c = Citation(document_id="x", raw_text="Ref")
        assert c.metadata == {}


@pytest.mark.unit
class TestSummary:
    def test_creation(self, sample_summary: Summary) -> None:
        assert sample_summary.content == "A brief summary."
        assert "doc-1" in sample_summary.source_ids

    def test_default_source_ids(self) -> None:
        s = Summary(content="empty")
        assert s.source_ids == []


@pytest.mark.unit
class TestReport:
    def test_creation(self, sample_report: Report) -> None:
        assert sample_report.title == "Test query"
        assert sample_report.body == "Report body."
        assert len(sample_report.citations) == 1

    def test_default_citations(self) -> None:
        r = Report(title="t", body="b")
        assert r.citations == []
