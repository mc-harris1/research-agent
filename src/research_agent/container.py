"""Dependency-injection container for the research-agent pipeline.

The :class:`Container` wires together every pipeline component and
exposes a single :meth:`Container.run` entry-point that orchestrates
the full research workflow:

1. Ingest documents from a source.
2. Index them for retrieval.
3. Retrieve relevant chunks for a query.
4. Summarize the chunks.
5. Extract citations from each ingested document.
6. Generate and return a structured report.

Callers can override any component by passing a concrete implementation
to the constructor, enabling easy testing and customisation without
sub-classing the container.
"""

from __future__ import annotations

import logging

from research_agent.citation.extractor import PlaceholderCitationExtractor
from research_agent.ingestion.ingester import PlaceholderIngester
from research_agent.interfaces import (
    Citation,
    CitationExtractor,
    Document,
    DocumentIngester,
    Report,
    ReportGenerator,
    Retriever,
    Summarizer,
)
from research_agent.report.generator import PlaceholderReportGenerator
from research_agent.retrieval.retriever import PlaceholderRetriever
from research_agent.summarization.summarizer import PlaceholderSummarizer

logger = logging.getLogger(__name__)


class Container:
    """Wires all pipeline components together via constructor injection.

    Example::

        container = Container(ingester=MyIngester(), retriever=MyRetriever())
        report = container.run(source="papers/", query="transformer architectures")
    """

    def __init__(
        self,
        ingester: DocumentIngester | None = None,
        retriever: Retriever | None = None,
        summarizer: Summarizer | None = None,
        citation_extractor: CitationExtractor | None = None,
        report_generator: ReportGenerator | None = None,
    ) -> None:
        """Initialise the container with optional component overrides.

        Any component left as *None* is replaced with the corresponding
        placeholder implementation.

        Args:
            ingester: Component responsible for loading raw documents.
            retriever: Component responsible for indexing and searching chunks.
            summarizer: Component responsible for condensing retrieved chunks.
            citation_extractor: Component responsible for extracting citations.
            report_generator: Component responsible for assembling the final report.
        """
        self.ingester: DocumentIngester = ingester or PlaceholderIngester()
        self.retriever: Retriever = retriever or PlaceholderRetriever()
        self.summarizer: Summarizer = summarizer or PlaceholderSummarizer()
        self.citation_extractor: CitationExtractor = (
            citation_extractor or PlaceholderCitationExtractor()
        )
        self.report_generator: ReportGenerator = report_generator or PlaceholderReportGenerator()

    def run(self, source: str, query: str, *, top_k: int = 10) -> Report:
        """Execute the full research pipeline and return a :class:`Report`.

        Args:
            source: Opaque string identifying the document source.
            query: Natural-language research question to answer.
            top_k: Maximum number of chunks to retrieve.

        Returns:
            A :class:`Report` produced by the configured generator.
        """
        logger.info("Pipeline starting: source=%r, query=%r", source, query)

        # 1. Ingest
        documents: list[Document] = self.ingester.ingest(source)
        logger.debug("Ingested %d document(s)", len(documents))

        # 2. Index
        self.retriever.index(documents)

        # 3. Retrieve
        chunks = self.retriever.retrieve(query, top_k=top_k)
        logger.debug("Retrieved %d chunk(s)", len(chunks))

        # 4. Summarise
        summary = self.summarizer.summarize(chunks)

        # 5. Extract citations
        citations: list[Citation] = []
        for doc in documents:
            citations.extend(self.citation_extractor.extract(doc))
        logger.debug("Extracted %d citation(s)", len(citations))

        # 6. Generate report
        report = self.report_generator.generate(query, chunks, summary, citations)
        logger.info("Pipeline complete: report title=%r", report.title)
        return report
