from pydantic import BaseModel, Field
from typing import Optional


class GlobalQueryRequest(BaseModel):
    """
    Request model for global book queries
    """
    query: str = Field(..., description="The user's question about the book content", min_length=1)
    conversation_id: Optional[str] = Field(None, description="Optional conversation identifier for maintaining context")


class SelectionQueryRequest(BaseModel):
    """
    Request model for selected text queries
    """
    query: str = Field(..., description="The user's question about the selected text", min_length=1)
    selected_text: str = Field(..., description="The text selected by the user", min_length=1)
    conversation_id: Optional[str] = Field(None, description="Optional conversation identifier for maintaining context")