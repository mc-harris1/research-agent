"""Placeholder retriever implementation.

Replace this class with a concrete retriever backed by a vector store,
BM25 index, or hybrid search engine.
"""

from __future__ import annotations

import logging

from research_agent.interfaces import Chunk, Document, Retriever

logger = logging.getLogger(__name__)


class PlaceholderRetriever(Retriever):
    """A no-op :class:`Retriever` that always returns an empty result set.

    This serves as the default implementation wired by the DI container
    until a real retriever is provided.
    """

    def __init__(self) -> None:
        self._index: list[Document] = []

    def index(self, documents: list[Document]) -> None:
        """Store documents for future retrieval (in-memory placeholder).

        Args:
            documents: Documents to add to the index.
        """
        logger.debug("PlaceholderRetriever.index called with %d document(s)", len(documents))
        self._index.extend(documents)

    def retrieve(self, query: str, *, top_k: int = 10) -> list[Chunk]:
        """Return an empty chunk list (placeholder implementation).

        Args:
            query: Ignored in this placeholder.
            top_k: Ignored in this placeholder.

        Returns:
            An empty list.
        """
        logger.debug("PlaceholderRetriever.retrieve called with query=%r", query)
        return []
