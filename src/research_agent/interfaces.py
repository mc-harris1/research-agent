"""Core Protocol/ABC interfaces for every modular component.

All concrete implementations must satisfy one of these contracts so that
the dependency-injection container can swap them transparently.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

# ---------------------------------------------------------------------------
# Shared value objects
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Document:
    """A raw document loaded from an external source."""

    id: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Chunk:
    """A sub-section of a :class:`Document` used for retrieval."""

    document_id: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Citation:
    """A bibliographic reference extracted from a document."""

    document_id: str
    raw_text: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Summary:
    """A condensed representation of one or more :class:`Chunk` objects."""

    content: str
    source_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Report:
    """A structured research report produced from retrieved chunks."""

    title: str
    body: str
    citations: list[Citation] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Component interfaces
# ---------------------------------------------------------------------------


class DocumentIngester(ABC):
    """Load raw :class:`Document` objects from an external source."""

    @abstractmethod
    def ingest(self, source: str) -> list[Document]:
        """Ingest documents from *source* and return them.

        Args:
            source: An opaque string identifying the data source
                (e.g. a file path, URL, or database connection string).

        Returns:
            A (possibly empty) list of :class:`Document` objects.
        """


class Retriever(ABC):
    """Search a corpus and return the most relevant :class:`Chunk` objects."""

    @abstractmethod
    def retrieve(self, query: str, *, top_k: int = 10) -> list[Chunk]:
        """Retrieve the *top_k* most relevant chunks for *query*.

        Args:
            query: A natural-language search query.
            top_k: Maximum number of chunks to return.

        Returns:
            An ordered list of :class:`Chunk` objects, most relevant first.
        """

    @abstractmethod
    def index(self, documents: list[Document]) -> None:
        """Build or update the retrieval index from *documents*.

        Args:
            documents: Documents to add to the index.
        """


class Summarizer(ABC):
    """Produce a :class:`Summary` from a collection of :class:`Chunk` objects."""

    @abstractmethod
    def summarize(self, chunks: list[Chunk]) -> Summary:
        """Summarize *chunks* into a single :class:`Summary`.

        Args:
            chunks: Source chunks to condense.

        Returns:
            A :class:`Summary` encapsulating the distilled content.
        """


class CitationExtractor(ABC):
    """Extract bibliographic :class:`Citation` objects from documents."""

    @abstractmethod
    def extract(self, document: Document) -> list[Citation]:
        """Parse all citations found in *document*.

        Args:
            document: The source document to analyse.

        Returns:
            A (possibly empty) list of :class:`Citation` objects.
        """


class ReportGenerator(ABC):
    """Assemble a :class:`Report` from retrieval results and a summary."""

    @abstractmethod
    def generate(
        self,
        query: str,
        chunks: list[Chunk],
        summary: Summary,
        citations: list[Citation],
    ) -> Report:
        """Generate a structured :class:`Report`.

        Args:
            query: The original research query.
            chunks: Retrieved evidence chunks.
            summary: Pre-computed summary of the chunks.
            citations: Extracted bibliographic references.

        Returns:
            A :class:`Report` ready for consumption.
        """
