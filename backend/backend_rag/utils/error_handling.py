from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
import logging
import traceback

logger = logging.getLogger(__name__)


class CustomException(Exception):
    """Custom exception for the application"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler for the application
    """
    logger.error(f"Global exception: {exc}\nTraceback: {traceback.format_exc()}")
    
    if isinstance(exc, CustomException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.message}
        )
    
    # For other exceptions, return a generic error message
    return JSONResponse(
        status_code=500,
        content={"error": "An internal server error occurred"}
    )


def setup_error_handlers(app: FastAPI):
    """
    Set up error handlers for the FastAPI application
    """
    app.add_exception_handler(Exception, global_exception_handler)


def handle_validation_error(error: Exception) -> Dict[str, Any]:
    """
    Handle validation errors specifically
    """
    logger.warning(f"Validation error: {error}")
    return {
        "error": "Invalid input data",
        "details": str(error)
    }


def handle_database_error(error: Exception) -> Dict[str, Any]:
    """
    Handle database errors specifically
    """
    logger.error(f"Database error: {error}")
    return {
        "error": "Database operation failed",
        "details": str(error)
    }


def handle_external_service_error(service_name: str, error: Exception) -> Dict[str, Any]:
    """
    Handle errors from external services (Cohere, Qdrant, etc.)
    """
    logger.error(f"Error from {service_name}: {error}")
    return {
        "error": f"External service {service_name} is unavailable",
        "details": str(error)
    }