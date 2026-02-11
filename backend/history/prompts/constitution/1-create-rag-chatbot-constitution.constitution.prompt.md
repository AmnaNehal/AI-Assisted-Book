---
id: 1
title: Create RAG Chatbot Constitution
stage: constitution
date: 2026-01-02
surface: agent
model: Qwen
feature: rag-chatbot
branch: main
user: acer
command: /sp.constitution
labels: [constitution, rag, chatbot, cohere]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - null
---

## Prompt

```
/sp.constitution 
Project: Integrated RAG Chatbot for Published Book Platform (Cohere-Based)

Purpose:
Design and implement a production-grade Retrieval-Augmented Generation (RAG) chatbot embedded within a published book platform. The chatbot must answer user queries based strictly on the book's content, including a special mode where answers are generated only from user-selected text.

Core Principles:
- Source-grounded generation: All responses must be derived from retrieved or explicitly provided text
- Zero hallucination tolerance: The system must not introduce facts outside retrieved context
- Specification-first development: Architecture and behavior defined before implementation
- Modularity and extensibility: Components must be independently replaceable
- Provider independence: Agent architecture inspired by OpenAI Agents/ChatKit, but implemented using Cohere APIs (NO OpenAI API KEYS)

LLM & Embeddings Standard:
- Language Model Provider: Cohere (mandatory)
- Embedding Model: Cohere Embeddings API
- Generation Model: Cohere Command / equivalent
- OpenAI APIs are explicitly prohibited

Retrieval Architecture:
- Vector Database: Qdrant Cloud (Free Tier)
- Metadata Store: Neon Serverless Postgres
- Chunking Strategy:
  - Semantic chunking with overlap
  - Chunk size and overlap must be configurable
- Retrieval Modes:
  1. Global Book Retrieval (Qdrant-based)
  2. User-Selected Text Only (strict context isolation)

Agent & Orchestration Standards:
- Agent-style orchestration using OpenAI Agents / ChatKit patterns (architecture only)
- Explicit separation of:
  - Query understanding
  - Retrieval
  - Context validation
  - Answer generation
- Each agent step must be observable and debuggable

Backend Standards:
- Framework: FastAPI
- API Design:
  - RESTful endpoints
  - Clear request/response schemas
- Async-first implementation
- Environment-based configuration management

Frontend Integration Requirements:
- Chatbot must be embeddable within the book UI
- Support for:
  - User text selection injection
  - Conversation history
  - Streaming or near-real-time responses
- Clear UI indicators for:
  - Global RAG mode
  - Selected-text-only mode

Security & Compliance:
- API keys stored securely (environment variables only)
- No hard-coded secrets
- Input sanitization for user-provided text
- Rate limiting considerations for free-tier services

Observability & Evaluation:
- Logging of:
  - Queries
  - Retrieved document IDs
  - Model responses
- Ability to audit:
  - Which text chunks influenced an answer
- Clear error handling and fallback responses

Documentation Standards:
- Architecture diagrams (RAG flow, agent flow)
- API documentation (OpenAPI/Swagger)
- Clear setup and deployment instructions
- Explicit mention of free-tier limitations

Constraints:
- Must operate within free-tier limits of Qdrant and Neon
- No OpenAI API usage
- No training or fine-tuning of models
- Retrieval-augmented generation only

Success Criteria:
- Chatbot answers are fully grounded in book content
- Selected-text-only questions never reference outside material
- System runs locally and in deployment without configuration changes
- Clear separation between specification, implementation, and deployment
- Ready for future extension (multi-book, citations, analytics)

Development Tooling:
- Specification & planning: SpecKit Plus
- Implementation & iteration: Qwen CLI
- Version control: Git-based workflow
```

## Response snapshot

I have successfully created and updated the project constitution for the Integrated RAG Chatbot for Published Book Platform. Here's the summary:

**New version**: 1.1.0 (incremented from 1.0.0)
**Bump rationale**: Added specific principles and sections for the RAG chatbot project, which constitutes a minor version change as it adds new material guidance and requirements.

**Key changes made**:
- Replaced template placeholders with specific project details for the RAG chatbot
- Added 6 core principles specific to RAG development
- Included dedicated sections for LLM & Embeddings Standard, Retrieval Architecture, Agent & Orchestration Standards, Frontend Integration Requirements, Security & Compliance, Observability & Evaluation, Constraints, and Development Tooling
- Created a comprehensive Sync Impact Report at the top of the file
- Ensured all principles are declarative, testable, and aligned with the project requirements

**Files flagged for manual follow-up**:
- No files require immediate follow-up as all template reviews were completed

**Suggested commit message**: `docs: create constitution for RAG chatbot project v1.1.0`

The constitution now properly reflects the requirements for developing a production-grade Retrieval-Augmented Generation (RAG) chatbot embedded within a published book platform using Cohere APIs, with strict adherence to source-grounded generation and zero hallucination tolerance.

## Outcome

- ✅ Impact: Created comprehensive project constitution for RAG chatbot
- 🧪 Tests: No tests needed for constitution creation
- 📁 Files: Updated .specify/memory/constitution.md with project-specific details
- 🔁 Next prompts: Ready to proceed with specification creation
- 🧠 Reflection: Constitution properly captures all specified requirements and principles

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with feature specification based on this constitution