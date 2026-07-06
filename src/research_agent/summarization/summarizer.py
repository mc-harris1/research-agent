"""Placeholder summarizer implementation.

Replace this class with a concrete summarizer backed by an LLM or
extractive summarization algorithm.
"""

from __future__ import annotations

import logging

from research_agent.interfaces import Chunk, Summarizer, Summary

logger = logging.getLogger(__name__)


class PlaceholderSummarizer(Summarizer):
    """A no-op :class:`Summarizer` that returns an empty summary.

    This serves as the default implementation wired by the DI container
    until a real summarizer is provided.
    """

    def summarize(self, chunks: list[Chunk]) -> Summary:
        """Return an empty summary (placeholder implementation).

        Args:
            chunks: Ignored in this placeholder.

        Returns:
            A :class:`Summary` with empty content.
        """
        logger.debug("PlaceholderSummarizer.summarize called with %d chunk(s)", len(chunks))
        return Summary(
            content="",
            source_ids=[chunk.document_id for chunk in chunks],
        )
