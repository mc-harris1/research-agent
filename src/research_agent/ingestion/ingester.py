"""Placeholder document ingester implementation.

Replace this class with a concrete ingester that loads documents from a
real data source (file system, database, web API, etc.).
"""

from __future__ import annotations

import logging

from research_agent.interfaces import Document, DocumentIngester

logger = logging.getLogger(__name__)


class PlaceholderIngester(DocumentIngester):
    """A no-op :class:`DocumentIngester` that always returns an empty list.

    This serves as the default implementation wired by the DI container
    until a real ingester is provided.
    """

    def ingest(self, source: str) -> list[Document]:
        """Return an empty document list (placeholder implementation).

        Args:
            source: Ignored in this placeholder.

        Returns:
            An empty list.
        """
        logger.debug("PlaceholderIngester.ingest called with source=%r", source)
        return []
