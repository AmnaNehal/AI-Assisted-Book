import logging
from datetime import datetime
from typing import Dict, Any, Optional
from config.settings import settings


def setup_logging():
    """
    Set up logging configuration for the application
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("app.log")
        ]
    )


def log_query(query: str, conversation_id: Optional[str] = None, query_type: str = "global"):
    """
    Log a query to the database or file
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Query received: {query[:50]}... (conversation: {conversation_id}, type: {query_type})")


def log_retrieved_documents(documents: list, query_id: str):
    """
    Log the retrieved documents for a query
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Retrieved {len(documents)} documents for query {query_id}")


def log_model_response(response: str, query_id: str, tokens_used: int):
    """
    Log the model response
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Generated response for query {query_id} ({tokens_used} tokens): {response[:50]}...")


def log_error(error: str, context: str = ""):
    """
    Log an error with context
    """
    logger = logging.getLogger(__name__)
    logger.error(f"Error in {context}: {error}")


def log_api_request(request_data: Dict[str, Any], request_id: str):
    """
    Log an API request
    """
    logger = logging.getLogger(__name__)
    logger.info(f"API request {request_id}: {request_data.get('query', '')[:50]}...")