"""Placeholder citation extractor implementation.

Replace this class with a concrete extractor powered by regex rules,
a dedicated bibliography parser, or an LLM-based extraction pipeline.
"""

from __future__ import annotations

import logging

from research_agent.interfaces import Citation, CitationExtractor, Document

logger = logging.getLogger(__name__)


class PlaceholderCitationExtractor(CitationExtractor):
    """A no-op :class:`CitationExtractor` that always returns an empty list.

    This serves as the default implementation wired by the DI container
    until a real extractor is provided.
    """

    def extract(self, document: Document) -> list[Citation]:
        """Return an empty citation list (placeholder implementation).

        Args:
            document: Ignored in this placeholder.

        Returns:
            An empty list.
        """
        logger.debug(
            "PlaceholderCitationExtractor.extract called for document_id=%r",
            document.id,
        )
        return []
