from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Boolean, Float
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from typing import List, Optional
from uuid import uuid4
from datetime import datetime


def generate_uuid():
    return str(uuid4())


class Base(AsyncAttrs, DeclarativeBase):
    pass


class BookContent(Base):
    """
    Represents the text content of a book that has been processed and vectorized for RAG functionality
    """
    __tablename__ = "book_content"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    book_metadata: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationship to document chunks
    chunks: Mapped[List["DocumentChunk"]] = relationship(back_populates="book", cascade="all, delete-orphan")


class DocumentChunk(Base):
    """
    Represents a semantic chunk of book content that has been vectorized for retrieval
    """
    __tablename__ = "document_chunks"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    book_id: Mapped[str] = mapped_column(String, ForeignKey("book_content.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    embedding_vector: Mapped[Optional[str]] = mapped_column(Text)  # Store as JSON string
    chunk_metadata: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationship to book
    book: Mapped["BookContent"] = relationship(back_populates="chunks")

    # Relationship to retrieved documents
    retrieved_docs: Mapped[List["RetrievedDocument"]] = relationship(back_populates="chunk")


class Conversation(Base):
    """
    Represents a series of exchanges between a user and the chatbot, including questions, responses, and context
    """
    __tablename__ = "conversations"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    session_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationship to queries
    queries: Mapped[List["Query"]] = relationship(back_populates="conversation")


class Query(Base):
    """
    Represents a single user query within a conversation
    """
    __tablename__ = "queries"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    conversation_id: Mapped[str] = mapped_column(String, ForeignKey("conversations.id"), nullable=False)
    query_text: Mapped[str] = mapped_column(Text, nullable=False)
    query_type: Mapped[str] = mapped_column(String(50), nullable=False)  # 'global' or 'selection'
    selected_text: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    conversation: Mapped["Conversation"] = relationship(back_populates="queries")
    retrieved_docs: Mapped[List["RetrievedDocument"]] = relationship(back_populates="query")
    response: Mapped["ModelResponse"] = relationship(back_populates="query", uselist=False)


class RetrievedDocument(Base):
    """
    Represents the specific segments of book content retrieved by the vector search to support a response
    """
    __tablename__ = "retrieved_documents"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    query_id: Mapped[str] = mapped_column(String, ForeignKey("queries.id"), nullable=False)
    chunk_id: Mapped[str] = mapped_column(String, ForeignKey("document_chunks.id"), nullable=False)
    relevance_score: Mapped[float] = mapped_column(Float, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    query: Mapped["Query"] = relationship(back_populates="retrieved_docs")
    chunk: Mapped["DocumentChunk"] = relationship(back_populates="retrieved_docs")


class ModelResponse(Base):
    """
    Represents the generated response from the Cohere model
    """
    __tablename__ = "model_responses"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    query_id: Mapped[str] = mapped_column(String, ForeignKey("queries.id"), nullable=False, unique=True)
    response_text: Mapped[str] = mapped_column(Text, nullable=False)
    tokens_used: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationship
    query: Mapped["Query"] = relationship(back_populates="response")


class QueryLog(Base):
    """
    Represents the record of all user queries, system responses, and retrieved document IDs for audit purposes
    """
    __tablename__ = "query_logs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    query_id: Mapped[str] = mapped_column(String, ForeignKey("queries.id"), nullable=False)
    retrieved_documents: Mapped[Optional[dict]] = mapped_column(JSON)  # List of retrieved document IDs
    response_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("model_responses.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    query: Mapped["Query"] = relationship()
    response: Mapped[Optional["ModelResponse"]] = relationship()


class APIRequest(Base):
    """
    Represents the data structure for requests from the frontend RagChatbot component to the backend
    """
    __tablename__ = "api_requests"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    query: Mapped[str] = mapped_column(Text, nullable=False)
    selected_text: Mapped[Optional[str]] = mapped_column(Text)
    mode: Mapped[str] = mapped_column(String(50), nullable=False)  # 'global' or 'selected-text'
    conversation_id: Mapped[Optional[str]] = mapped_column(String)
    timestamp: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    processed: Mapped[bool] = mapped_column(Boolean, default=False)