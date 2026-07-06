"""Tests for the placeholder component implementations."""

from __future__ import annotations

import pytest

from research_agent.citation.extractor import PlaceholderCitationExtractor
from research_agent.ingestion.ingester import PlaceholderIngester
from research_agent.interfaces import (
    Chunk,
    Citation,
    CitationExtractor,
    Document,
    DocumentIngester,
    ReportGenerator,
    Retriever,
    Summarizer,
)
from research_agent.report.generator import PlaceholderReportGenerator
from research_agent.retrieval.retriever import PlaceholderRetriever
from research_agent.summarization.summarizer import PlaceholderSummarizer

# ---------------------------------------------------------------------------
# PlaceholderIngester
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestPlaceholderIngester:
    def test_implements_interface(self) -> None:
        ingester = PlaceholderIngester()
        assert isinstance(ingester, DocumentIngester)

    def test_returns_empty_list(self, sample_document: Document) -> None:
        ingester = PlaceholderIngester()
        result = ingester.ingest("any-source")
        assert result == []

    def test_accepts_any_source_string(self) -> None:
        ingester = PlaceholderIngester()
        for source in ("", "path/to/file.pdf", "https://example.com/api"):
            assert ingester.ingest(source) == []


# ---------------------------------------------------------------------------
# PlaceholderRetriever
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestPlaceholderRetriever:
    def test_implements_interface(self) -> None:
        retriever = PlaceholderRetriever()
        assert isinstance(retriever, Retriever)

    def test_retrieve_returns_empty_list(self) -> None:
        retriever = PlaceholderRetriever()
        assert retriever.retrieve("query") == []

    def test_retrieve_respects_top_k_signature(self) -> None:
        retriever = PlaceholderRetriever()
        assert retriever.retrieve("query", top_k=5) == []

    def test_index_accepts_documents(self, sample_document: Document) -> None:
        retriever = PlaceholderRetriever()
        retriever.index([sample_document])
        # Index call must not raise; internal state is captured
        assert sample_document in retriever._index

    def test_index_accumulates_documents(self, sample_document: Document) -> None:
        retriever = PlaceholderRetriever()
        retriever.index([sample_document])
        retriever.index([sample_document])
        assert len(retriever._index) == 2


# ---------------------------------------------------------------------------
# PlaceholderSummarizer
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestPlaceholderSummarizer:
    def test_implements_interface(self) -> None:
        summarizer = PlaceholderSummarizer()
        assert isinstance(summarizer, Summarizer)

    def test_returns_empty_summary_for_empty_input(self) -> None:
        summarizer = PlaceholderSummarizer()
        result = summarizer.summarize([])
        assert result.content == ""
        assert result.source_ids == []

    def test_captures_document_ids(self, sample_chunk: Chunk) -> None:
        summarizer = PlaceholderSummarizer()
        result = summarizer.summarize([sample_chunk])
        assert sample_chunk.document_id in result.source_ids


# ---------------------------------------------------------------------------
# PlaceholderCitationExtractor
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestPlaceholderCitationExtractor:
    def test_implements_interface(self) -> None:
        extractor = PlaceholderCitationExtractor()
        assert isinstance(extractor, CitationExtractor)

    def test_returns_empty_list(self, sample_document: Document) -> None:
        extractor = PlaceholderCitationExtractor()
        assert extractor.extract(sample_document) == []


# ---------------------------------------------------------------------------
# PlaceholderReportGenerator
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestPlaceholderReportGenerator:
    def test_implements_interface(self) -> None:
        generator = PlaceholderReportGenerator()
        assert isinstance(generator, ReportGenerator)

    def test_uses_query_as_title(
        self,
        sample_chunk: Chunk,
        sample_citation: Citation,
    ) -> None:
        from research_agent.interfaces import Summary

        generator = PlaceholderReportGenerator()
        summary = Summary(content="Test summary.")
        report = generator.generate("my query", [sample_chunk], summary, [sample_citation])
        assert report.title == "my query"

    def test_body_contains_summary(
        self,
        sample_chunk: Chunk,
        sample_citation: Citation,
    ) -> None:
        from research_agent.interfaces import Summary

        generator = PlaceholderReportGenerator()
        summary = Summary(content="Meaningful summary content.")
        report = generator.generate("q", [sample_chunk], summary, [sample_citation])
        assert "Meaningful summary content." in report.body

    def test_body_placeholder_when_summary_empty(
        self, sample_chunk: Chunk, sample_citation: Citation
    ) -> None:
        from research_agent.interfaces import Summary

        generator = PlaceholderReportGenerator()
        summary = Summary(content="")
        report = generator.generate("q", [sample_chunk], summary, [])
        assert "(no summary available)" in report.body

    def test_citations_forwarded(self, sample_chunk: Chunk, sample_citation: Citation) -> None:
        from research_agent.interfaces import Summary

        generator = PlaceholderReportGenerator()
        summary = Summary(content="s")
        report = generator.generate("q", [sample_chunk], summary, [sample_citation])
        assert sample_citation in report.citations
