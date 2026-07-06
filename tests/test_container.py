"""Tests for the dependency-injection :class:`Container`."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from research_agent.citation.extractor import PlaceholderCitationExtractor
from research_agent.container import Container
from research_agent.ingestion.ingester import PlaceholderIngester
from research_agent.interfaces import (
    Chunk,
    Citation,
    CitationExtractor,
    Document,
    DocumentIngester,
    Report,
    ReportGenerator,
    Retriever,
    Summarizer,
    Summary,
)
from research_agent.report.generator import PlaceholderReportGenerator
from research_agent.retrieval.retriever import PlaceholderRetriever
from research_agent.summarization.summarizer import PlaceholderSummarizer


@pytest.mark.unit
class TestContainerDefaults:
    def test_defaults_to_placeholder_components(self) -> None:
        container = Container()
        assert isinstance(container.ingester, PlaceholderIngester)
        assert isinstance(container.retriever, PlaceholderRetriever)
        assert isinstance(container.summarizer, PlaceholderSummarizer)
        assert isinstance(container.citation_extractor, PlaceholderCitationExtractor)
        assert isinstance(container.report_generator, PlaceholderReportGenerator)

    def test_run_with_all_placeholders_returns_report(self) -> None:
        container = Container()
        report = container.run(source="any", query="test query")
        assert isinstance(report, Report)
        assert report.title == "test query"

    def test_run_empty_pipeline_produces_fallback_body(self) -> None:
        container = Container()
        report = container.run(source="s", query="q")
        assert "(no summary available)" in report.body


@pytest.mark.unit
class TestContainerInjection:
    def test_accepts_custom_ingester(self) -> None:
        mock_ingester: DocumentIngester = MagicMock(spec=DocumentIngester)
        mock_ingester.ingest.return_value = []  # type: ignore[attr-defined]
        container = Container(ingester=mock_ingester)
        assert container.ingester is mock_ingester

    def test_accepts_custom_retriever(self) -> None:
        mock_retriever: Retriever = MagicMock(spec=Retriever)
        mock_retriever.retrieve.return_value = []  # type: ignore[attr-defined]
        container = Container(retriever=mock_retriever)
        assert container.retriever is mock_retriever

    def test_accepts_custom_summarizer(self) -> None:
        mock_summarizer: Summarizer = MagicMock(spec=Summarizer)
        container = Container(summarizer=mock_summarizer)
        assert container.summarizer is mock_summarizer

    def test_accepts_custom_citation_extractor(self) -> None:
        mock_extractor: CitationExtractor = MagicMock(spec=CitationExtractor)
        container = Container(citation_extractor=mock_extractor)
        assert container.citation_extractor is mock_extractor

    def test_accepts_custom_report_generator(self) -> None:
        mock_generator: ReportGenerator = MagicMock(spec=ReportGenerator)
        container = Container(report_generator=mock_generator)
        assert container.report_generator is mock_generator


@pytest.mark.unit
class TestContainerPipelineOrchestration:
    """Verify that :meth:`Container.run` calls each component in the correct order."""

    def _make_mocks(
        self,
        documents: list[Document],
        chunks: list[Chunk],
        summary: Summary,
        citations: list[Citation],
        report: Report,
    ) -> Container:
        """Build a container whose components are configured mocks."""
        ingester = MagicMock(spec=DocumentIngester)
        ingester.ingest.return_value = documents

        retriever = MagicMock(spec=Retriever)
        retriever.retrieve.return_value = chunks

        summarizer = MagicMock(spec=Summarizer)
        summarizer.summarize.return_value = summary

        extractor = MagicMock(spec=CitationExtractor)
        extractor.extract.return_value = citations

        generator = MagicMock(spec=ReportGenerator)
        generator.generate.return_value = report

        return Container(
            ingester=ingester,
            retriever=retriever,
            summarizer=summarizer,
            citation_extractor=extractor,
            report_generator=generator,
        )

    def test_ingester_called_with_source(
        self, sample_document: Document, sample_report: Report
    ) -> None:
        container = self._make_mocks(
            documents=[sample_document],
            chunks=[],
            summary=Summary(content="s"),
            citations=[],
            report=sample_report,
        )
        container.run(source="my-source", query="q")
        container.ingester.ingest.assert_called_once_with("my-source")  # type: ignore[attr-defined]

    def test_retriever_indexed_with_documents(
        self, sample_document: Document, sample_report: Report
    ) -> None:
        container = self._make_mocks(
            documents=[sample_document],
            chunks=[],
            summary=Summary(content="s"),
            citations=[],
            report=sample_report,
        )
        container.run(source="s", query="q")
        container.retriever.index.assert_called_once_with([sample_document])  # type: ignore[attr-defined]

    def test_retriever_called_with_query_and_top_k(
        self, sample_document: Document, sample_report: Report
    ) -> None:
        container = self._make_mocks(
            documents=[sample_document],
            chunks=[],
            summary=Summary(content="s"),
            citations=[],
            report=sample_report,
        )
        container.run(source="s", query="my query", top_k=5)
        container.retriever.retrieve.assert_called_once_with("my query", top_k=5)  # type: ignore[attr-defined]

    def test_citation_extractor_called_per_document(
        self,
        sample_document: Document,
        sample_chunk: Chunk,
        sample_citation: Citation,
        sample_report: Report,
    ) -> None:
        doc2 = Document(id="doc-2", content="second doc")
        container = self._make_mocks(
            documents=[sample_document, doc2],
            chunks=[sample_chunk],
            summary=Summary(content="s"),
            citations=[sample_citation],
            report=sample_report,
        )
        container.run(source="s", query="q")
        assert container.citation_extractor.extract.call_count == 2  # type: ignore[attr-defined]

    def test_report_generator_receives_all_components(
        self,
        sample_document: Document,
        sample_chunk: Chunk,
        sample_citation: Citation,
        sample_report: Report,
    ) -> None:
        summary = Summary(content="summ")
        container = self._make_mocks(
            documents=[sample_document],
            chunks=[sample_chunk],
            summary=summary,
            citations=[sample_citation],
            report=sample_report,
        )
        result = container.run(source="s", query="my query")
        container.report_generator.generate.assert_called_once_with(  # type: ignore[attr-defined]
            "my query", [sample_chunk], summary, [sample_citation]
        )
        assert result is sample_report
