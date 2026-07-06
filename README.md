# research-agent

An AI-assisted research workflow for literature discovery, synthesis, and knowledge extraction.

## Overview

`research-agent` is a production-ready Python library that provides modular, swappable components for building end-to-end research pipelines:

| Component | Interface | Default placeholder |
|---|---|---|
| Document ingestion | `DocumentIngester` | `PlaceholderIngester` |
| Retrieval | `Retriever` | `PlaceholderRetriever` |
| Summarization | `Summarizer` | `PlaceholderSummarizer` |
| Citation extraction | `CitationExtractor` | `PlaceholderCitationExtractor` |
| Report generation | `ReportGenerator` | `PlaceholderReportGenerator` |

Every component is wired together by a lightweight dependency-injection `Container` that accepts concrete implementations at construction time, making it straightforward to swap in real LLM-backed or vector-store-backed implementations without modifying the pipeline orchestration logic.

## Quickstart

```python
from research_agent.container import Container

# Use all placeholder components (safe default)
container = Container()
report = container.run(source="papers/", query="transformer architectures")
print(report.title)
print(report.body)
```

Inject a custom ingester:

```python
from research_agent.container import Container
from my_package import MyIngester, MyRetriever

container = Container(ingester=MyIngester(), retriever=MyRetriever())
report = container.run(source="s3://bucket/papers/", query="attention mechanisms")
```

## Project layout

```
src/research_agent/
├── interfaces.py          # ABCs and value objects (Document, Chunk, Citation, …)
├── container.py           # DI container / pipeline orchestrator
├── ingestion/             # DocumentIngester implementations
├── retrieval/             # Retriever implementations
├── summarization/         # Summarizer implementations
├── citation/              # CitationExtractor implementations
└── report/                # ReportGenerator implementations

tests/
├── conftest.py            # shared fixtures
├── test_interfaces.py     # value-object tests
├── test_placeholders.py   # placeholder component tests
└── test_container.py      # DI container / pipeline tests
```

## Development setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Install uv (once)
pip install uv

# Create virtual environment and install all dev dependencies
uv sync --extra dev

# Activate the environment
source .venv/bin/activate
```

## Running checks

```bash
# Lint
uv run ruff check src/ tests/

# Format
uv run ruff format src/ tests/

# Type check
uv run pyright src/

# Tests with coverage
uv run pytest tests/ -v
```

## Pre-commit hooks

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

## CI

GitHub Actions runs lint, type-check, and tests on every push and pull-request targeting `main`. See [`.github/workflows/ci.yml`](.github/workflows/ci.yml).
