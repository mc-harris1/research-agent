"""Shared pytest fixtures and configuration."""

from __future__ import annotations

import pytest

from research_agent.interfaces import (
    Chunk,
    Citation,
    Document,
    Report,
    Summary,
)


@pytest.fixture()
def sample_document() -> Document:
    """Return a minimal :class:`Document` for use in tests."""
    return Document(id="doc-1", content="Hello, world!", metadata={"source": "test"})


@pytest.fixture()
def sample_chunk(sample_document: Document) -> Chunk:
    """Return a :class:`Chunk` derived from *sample_document*."""
    return Chunk(
        document_id=sample_document.id,
        content=sample_document.content,
        metadata={"index": 0},
    )


@pytest.fixture()
def sample_citation(sample_document: Document) -> Citation:
    """Return a minimal :class:`Citation` for use in tests."""
    return Citation(
        document_id=sample_document.id,
        raw_text="Author et al., 2024",
        metadata={},
    )


@pytest.fixture()
def sample_summary(sample_chunk: Chunk) -> Summary:
    """Return a :class:`Summary` built from *sample_chunk*."""
    return Summary(
        content="A brief summary.",
        source_ids=[sample_chunk.document_id],
    )


@pytest.fixture()
def sample_report(sample_citation: Citation) -> Report:
    """Return a minimal :class:`Report` for use in tests."""
    return Report(
        title="Test query",
        body="Report body.",
        citations=[sample_citation],
    )
