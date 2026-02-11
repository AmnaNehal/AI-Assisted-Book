import re
from typing import Optional
from config.settings import settings


def validate_query_text(query: str) -> bool:
    """
    Validate the query text
    """
    if not query or not query.strip():
        return False
    
    # Check if query is too short
    if len(query.strip()) < 3:
        return False
    
    # Check if query is too long (to prevent abuse)
    if len(query) > 1000:
        return False
    
    return True


def validate_selected_text(selected_text: str) -> bool:
    """
    Validate the selected text
    """
    if not selected_text or not selected_text.strip():
        return False
    
    # Check if selected text is too short
    if len(selected_text.strip()) < 5:
        return False
    
    # Check if selected text is too long (to prevent token limit issues)
    if len(selected_text) > 5000:
        return False
    
    return True


def validate_conversation_id(conversation_id: Optional[str]) -> bool:
    """
    Validate the conversation ID format
    """
    if not conversation_id:
        return True  # Conversation ID is optional
    
    # Basic validation: alphanumeric and hyphens/underscores
    pattern = r'^[a-zA-Z0-9_-]+$'
    return bool(re.match(pattern, conversation_id))


def sanitize_input(text: str) -> str:
    """
    Sanitize input text to prevent injection attacks
    """
    if not text:
        return text
    
    # Remove potentially dangerous characters/sequences
    sanitized = text.replace('<script', '').replace('javascript:', '')
    sanitized = sanitized.replace('vbscript:', '').replace('onerror', '')
    sanitized = sanitized.replace('onload', '')
    
    return sanitized


def validate_cohere_response(response: str) -> bool:
    """
    Validate that the Cohere response is appropriate
    """
    if not response or not response.strip():
        return False
    
    # Check for common hallucination indicators
    if "I don't know" in response or "I'm not sure" in response:
        return False  # These indicate the model couldn't find relevant info
    
    return True