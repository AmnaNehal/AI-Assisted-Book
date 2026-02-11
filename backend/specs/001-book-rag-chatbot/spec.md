# Feature Specification: Backend for Book RAG Chatbot

**Feature Branch**: `001-book-rag-chatbot`
**Created**: 2026-01-02
**Status**: Draft
**Input**: User description: "Target audience: Readers and students of the book who want interactive question-answering. Developers and educators who want to embed context-aware chatbots in educational content. Focus: Build a production-grade Retrieval-Augmented Generation (RAG) chatbot embedded in the book UI. Answer questions strictly from the book's content, including a "user-selected text only" mode. Backend integration using FastAPI, Qdrant Cloud Free Tier, and Neon Serverless Postgres. Generation using Cohere Command / Embeddings API (no OpenAI keys). Ensure modularity, observability, and compliance with free-tier limitations. Success criteria: Chatbot answers are fully grounded in retrieved book content. Selected-text-only queries never reference outside material. FastAPI endpoints handle global and selection-based queries correctly. Cohere embeddings and command models return accurate, context-aware responses. Qdrant vector store is correctly configured and returns relevant embeddings. Frontend integrates seamlessly with book UI, supporting conversation history and streaming responses. All queries, retrieved document IDs, and model responses are logged for audit and debugging. Deployment works locally and within free-tier cloud constraints. Constraints: Vector Database: Qdrant Cloud Free Tier .Metadata Store: Neon Serverless Postgres .LLM & Embedding.No OpenAI API usage. Async-first backend with REST endpoints. Frontend must allow user text selection injection and conversation history. Must operate entirely within free-tier limits. No training or fine-tuning of models; RAG-based generation only. Not building: OpenAI API-based chatbot. Paid-tier infrastructure dependencies. Multi-book cross-referencing (future phase only). End-to-end training or fine-tuning of LLM. Timeline / Phase: Phase I: Backend prototype + vectorization of book content. Phase II: Frontend integration with selection-based query mode. Phase III: Observability, logging, and deployment. Development Tooling: Specification & planning: SpecKit Plus Implementation & iteration: Qwen CLI Version control: Git-based workflow"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Backend API for Book Content Question Answering (Priority: P1)

As a frontend application, I want to send user questions to the backend API and receive accurate answers based only on the book's content, so that I can provide users with responses grounded in the book's information.

**Why this priority**: This is the core functionality of the RAG system - processing user questions and returning accurate, book-based answers via API endpoints.

**Independent Test**: Can be fully tested by sending various questions to the backend API and verifying that responses are grounded in the book's text without referencing external sources.

**Acceptance Scenarios**:

1. **Given** the backend is running with book content indexed, **When** a question is sent to the API endpoint, **Then** the backend returns an accurate answer based solely on the book's content.
2. **Given** a question has been received by the backend, **When** the response is generated, **Then** the response includes relevant citations or references to the specific parts of the book that support the answer.

---

### User Story 2 - Backend API for Selected Text Question Answering (Priority: P2)

As a frontend application, I want to send user-selected text along with questions to the backend API, so that I can get responses that are based only on the selected text without referencing other parts of the book.

**Why this priority**: This provides a more focused and precise way to interact with the book content, allowing for deeper analysis of specific passages.

**Independent Test**: Can be tested by sending selected text with questions to the backend API and verifying that responses only reference the provided text without including other book content.

**Acceptance Scenarios**:

1. **Given** the backend receives selected text with a related question, **When** the response is generated, **Then** the response is based only on the provided text and does not reference other parts of the book.

---

### User Story 3 - Backend API for Conversation History and Context (Priority: P3)

As a frontend application, I want to maintain conversation history with the backend, so that I can have a natural dialogue with follow-up questions that reference previous exchanges.

**Why this priority**: This enhances the user experience by allowing for more natural, contextual conversations rather than isolated questions.

**Independent Test**: Can be tested by sending a multi-turn conversation to the backend and verifying that it maintains context from previous exchanges.

**Acceptance Scenarios**:

1. **Given** I am in a conversation with the backend, **When** I send a follow-up question that references previous context, **Then** the backend understands and responds appropriately based on the conversation history.

---

### Edge Cases

- What happens when the book content is very large and the vector search takes too long?
- How does the system handle ambiguous questions that could refer to multiple parts of the book?
- What happens when a user asks a question about content that doesn't exist in the book?
- How does the system handle very long text selections that might exceed model token limits?
- What happens when the Cohere API is temporarily unavailable?
- How does the system handle concurrent requests from multiple users?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide REST API endpoints for processing user questions about book content
- **FR-002**: System MUST provide API endpoints for "selected text only" mode where questions are answered based solely on provided text
- **FR-003**: System MUST retrieve relevant book content using vector search in Qdrant to support the RAG functionality
- **FR-004**: System MUST integrate with Cohere API for generating responses based on retrieved content
- **FR-005**: System MUST maintain conversation history to support contextual dialogue
- **FR-006**: System MUST provide streaming responses via API to support frontend streaming functionality
- **FR-007**: System MUST log all queries, retrieved document IDs, and model responses for audit and debugging purposes
- **FR-008**: System MUST support book content vectorization for RAG functionality
- **FR-009**: System MUST ensure responses are fully grounded in retrieved book content without hallucination
- **FR-010**: System MUST provide async-first API endpoints to handle concurrent requests efficiently

*Example of marking unclear requirements:*

- **FR-011**: System MUST support PDF and plain text formats for book content vectorization
- **FR-012**: System MUST support anonymous API access without user authentication for initial implementation

### Key Entities *(include if feature involves data)*

- **Book Content**: Represents the text content of a book that has been processed and vectorized for RAG functionality
- **Conversation**: Represents a series of exchanges between a user and the chatbot, including questions, responses, and context
- **Retrieved Document**: Represents the specific segments of book content retrieved by the vector search to support a response
- **Query Log**: Represents the record of all user queries, system responses, and retrieved document IDs for audit purposes
- **API Request**: Represents the data structure for requests from the frontend RagChatbot component to the backend

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 95% of backend responses are fully grounded in retrieved book content without hallucination
- **SC-002**: Selected-text-only queries never reference material outside the provided text (0% cross-referencing error rate)
- **SC-003**: API endpoints respond to user questions with an average latency of under 5 seconds
- **SC-004**: 90% of user questions receive relevant, accurate answers based on the book content
- **SC-005**: The backend can handle at least 100 concurrent API requests without performance degradation
- **SC-006**: All queries, retrieved document IDs, and model responses are successfully logged for 100% of interactions
- **SC-007**: The backend API integrates seamlessly with the frontend RagChatbot component at frontend_book/src/components/RagChatbot/
