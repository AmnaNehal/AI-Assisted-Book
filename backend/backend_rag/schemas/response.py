from pydantic import BaseModel, Field
from typing import Optional, List


class RetrievedChunk(BaseModel):
    """
    Model for a retrieved chunk of content
    """
    chunk_id: str = Field(..., description="Unique identifier for the retrieved chunk")
    content: str = Field(..., description="The content of the retrieved chunk")
    relevance_score: float = Field(..., description="Relevance score of the chunk to the query", ge=0.0, le=1.0)


class QueryResponse(BaseModel):
    """
    Response model for query endpoints
    """
    answer: str = Field(..., description="The generated answer based on the book content")
    retrieved_chunks: List[RetrievedChunk] = Field(..., description="List of chunks that were retrieved and used to generate the answer")
    query_id: str = Field(..., description="Unique identifier for the query")
    conversation_id: Optional[str] = Field(None, description="Conversation identifier if context was maintained")