"""Placeholder report generator implementation.

Replace this class with a concrete generator that uses templates,
a document-assembly library, or an LLM to produce polished reports.
"""

from __future__ import annotations

import logging

from research_agent.interfaces import (
    Chunk,
    Citation,
    Report,
    ReportGenerator,
    Summary,
)

logger = logging.getLogger(__name__)


class PlaceholderReportGenerator(ReportGenerator):
    """A minimal :class:`ReportGenerator` that assembles a plain-text report.

    This serves as the default implementation wired by the DI container
    until a real generator is provided.
    """

    def generate(
        self,
        query: str,
        chunks: list[Chunk],
        summary: Summary,
        citations: list[Citation],
    ) -> Report:
        """Assemble a bare-bones report from the supplied components.

        Args:
            query: The original research query used as the report title.
            chunks: Retrieved evidence chunks (unused in placeholder).
            summary: Pre-computed summary included verbatim in the body.
            citations: Extracted references appended to the body.

        Returns:
            A :class:`Report` containing the query, summary, and citations.
        """
        logger.debug(
            "PlaceholderReportGenerator.generate called: query=%r, chunks=%d, citations=%d",
            query,
            len(chunks),
            len(citations),
        )
        body_parts = [summary.content] if summary.content else ["(no summary available)"]
        return Report(
            title=query,
            body="\n\n".join(body_parts),
            citations=list(citations),
        )
