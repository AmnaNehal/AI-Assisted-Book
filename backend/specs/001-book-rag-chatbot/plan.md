# Implementation Plan: Backend for Book RAG Chatbot

**Branch**: `001-book-rag-chatbot` | **Date**: 2026-01-02 | **Spec**: [Backend for Book RAG Chatbot](spec.md)
**Input**: Feature specification from `/specs/001-book-rag-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a backend service for a Retrieval-Augmented Generation (RAG) chatbot that allows users to ask questions about book content. The system uses FastAPI for the backend, Qdrant Cloud for vector storage, Neon Serverless Postgres for metadata, and Cohere API for embeddings and text generation. The backend provides REST API endpoints for both global book queries and user-selected text queries, with full logging and observability capabilities.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, Cohere Python SDK, Qdrant Python client, SQLAlchemy async, asyncpg, Pydantic
**Storage**: Qdrant Cloud (vector store), Neon Serverless Postgres (metadata store)
**Testing**: pytest with integration and unit test frameworks
**Target Platform**: Linux server (cloud deployment with local development support)
**Project Type**: Web backend service
**Performance Goals**: <5 second response time for queries, support 100+ concurrent users
**Constraints**: Must operate within free-tier limits of Qdrant and Neon, no OpenAI API usage, zero hallucination tolerance
**Scale/Scope**: Single book support initially, with extensibility for multiple books

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Source-grounded generation: System will retrieve from book content before generating responses
- ✅ Zero hallucination tolerance: Responses will be strictly based on retrieved content
- ✅ Specification-first development: Implementation follows detailed specification
- ✅ Modularity and extensibility: Components have well-defined interfaces
- ✅ Provider independence: Using Cohere APIs as specified, not OpenAI
- ✅ Async-first implementation: All endpoints will be async for performance
- ✅ LLM & Embeddings Standard: Using Cohere exclusively for embeddings and generation
- ✅ Retrieval Architecture: Using Qdrant for vector storage and Neon for metadata
- ✅ Agent & Orchestration Standards: Implementing clear separation of concerns
- ✅ Backend Standards: Using FastAPI as required
- ✅ Security & Compliance: API keys via environment variables only
- ✅ Free-tier Operation: Design respects free-tier limitations

## Project Structure

### Documentation (this feature)

```text
specs/001-book-rag-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend_rag/
├── api/
│   ├── __init__.py
│   ├── query.py          # Query endpoints (global and selection-based)
│   └── health.py         # Health check endpoint
├── core/
│   ├── __init__.py
│   ├── rag_orchestrator.py  # Main RAG logic and agent orchestration
│   ├── query_parser.py      # Query understanding component
│   ├── context_validator.py # Context validation component
│   └── answer_generator.py  # Answer generation component
├── db/
│   ├── __init__.py
│   ├── qdrant_client.py     # Qdrant vector store connector
│   ├── neon_connector.py    # Neon Postgres connector
│   └── models.py            # Database models
├── schemas/
│   ├── __init__.py
│   ├── request.py           # Request schemas (Pydantic models)
│   └── response.py          # Response schemas (Pydantic models)
├── utils/
│   ├── __init__.py
│   ├── chunking.py          # Text chunking utilities
│   ├── logging.py           # Logging utilities
│   └── validation.py        # Input validation utilities
├── config/
│   ├── __init__.py
│   └── settings.py          # Environment configuration
├── main.py                  # FastAPI application entry point
├── requirements.txt         # Python dependencies
└── .env.example             # Example environment variables file
```

**Structure Decision**: Web application backend structure selected to support the RAG chatbot functionality with clear separation of concerns. The backend will be developed in the backend_rag directory with modules for API endpoints, core RAG logic, database connectivity, data schemas, utilities, and configuration.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
