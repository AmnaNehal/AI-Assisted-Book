# Data Model: Backend for Book RAG Chatbot

## Entity: Book Content
**Description**: Represents the text content of a book that has been processed and vectorized for RAG functionality
**Fields**:
- id: UUID (Primary Key)
- title: String (Book title)
- content: Text (Full text content of the book)
- metadata: JSON (Additional book information)
- created_at: DateTime
- updated_at: DateTime

## Entity: Document Chunk
**Description**: Represents a semantic chunk of book content that has been vectorized for retrieval
**Fields**:
- id: UUID (Primary Key)
- book_id: UUID (Foreign Key to Book Content)
- content: Text (Chunked content)
- chunk_index: Integer (Order of chunk in the book)
- embedding_vector: Vector (Cohere embedding vector)
- metadata: JSON (Additional chunk metadata)
- created_at: DateTime
- updated_at: DateTime

## Entity: Conversation
**Description**: Represents a series of exchanges between a user and the chatbot, including questions, responses, and context
**Fields**:
- id: UUID (Primary Key)
- session_id: String (Identifier for the conversation session)
- created_at: DateTime
- updated_at: DateTime

## Entity: Query
**Description**: Represents a single user query within a conversation
**Fields**:
- id: UUID (Primary Key)
- conversation_id: UUID (Foreign Key to Conversation)
- query_text: Text (The user's question)
- query_type: String (global or selection-based)
- selected_text: Text (Optional text selected by user)
- created_at: DateTime

## Entity: Retrieved Document
**Description**: Represents the specific segments of book content retrieved by the vector search to support a response
**Fields**:
- id: UUID (Primary Key)
- query_id: UUID (Foreign Key to Query)
- chunk_id: UUID (Foreign Key to Document Chunk)
- relevance_score: Float (Similarity score from vector search)
- content: Text (Content of the retrieved chunk)
- created_at: DateTime

## Entity: Model Response
**Description**: Represents the generated response from the Cohere model
**Fields**:
- id: UUID (Primary Key)
- query_id: UUID (Foreign Key to Query)
- response_text: Text (Generated answer)
- tokens_used: Integer (Number of tokens in the response)
- created_at: DateTime

## Entity: Query Log
**Description**: Represents the record of all user queries, system responses, and retrieved document IDs for audit purposes
**Fields**:
- id: UUID (Primary Key)
- query_id: UUID (Foreign Key to Query)
- retrieved_documents: JSON (List of retrieved document IDs)
- response_id: UUID (Foreign Key to Model Response)
- created_at: DateTime

## Entity: API Request
**Description**: Represents the data structure for requests from the frontend RagChatbot component to the backend
**Fields**:
- id: UUID (Primary Key)
- query: String (User's question)
- selected_text: String (Optional selected text)
- mode: String (global or selected-text)
- conversation_id: String (Optional conversation identifier)
- timestamp: DateTime
- processed: Boolean (Whether the request has been processed)