from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
import logging
from schemas.request import GlobalQueryRequest, SelectionQueryRequest
from schemas.response import QueryResponse
from core.rag_orchestrator import RAGOrchestrator
from db.neon_connector import NeonConnector
from utils.logging import log_api_request
from utils.validation import validate_query_text, validate_selected_text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
import uuid

logger = logging.getLogger(__name__)
router = APIRouter()
neon_connector = NeonConnector()


# Dependency to get DB session
async def get_db_session():
    async with neon_connector.async_session() as session:
        yield session


@router.post("/query-global", response_model=QueryResponse)
async def query_global(request: GlobalQueryRequest, db_session: AsyncSession = Depends(get_db_session)):
    """
    Endpoint to query the full book content
    """
    try:
        # Log the API request
        request_id = f"req_{uuid.uuid4()}"
        log_api_request(request.dict(), request_id)

        # Create RAG orchestrator with DB session
        rag_orchestrator = RAGOrchestrator(db_session=db_session)

        # Process the query through the RAG orchestrator
        result = await rag_orchestrator.process_global_query(
            query=request.query,
            conversation_id=request.conversation_id
        )

        # Format the response
        response = QueryResponse(
            answer=result["answer"],
            retrieved_chunks=result["retrieved_chunks"],
            query_id=result["query_id"],
            conversation_id=result["conversation_id"]
        )

        return response
    except ValueError as e:
        logger.error(f"Validation error in query-global: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing global query: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/query-selection", response_model=QueryResponse)
async def query_selection(request: SelectionQueryRequest, db_session: AsyncSession = Depends(get_db_session)):
    """
    Endpoint to query only user-selected text
    """
    try:
        # Log the API request
        request_id = f"req_{uuid.uuid4()}"
        log_api_request(request.dict(), request_id)

        # Create RAG orchestrator with DB session
        rag_orchestrator = RAGOrchestrator(db_session=db_session)

        # Process the query through the RAG orchestrator
        result = await rag_orchestrator.process_selection_query(
            query=request.query,
            selected_text=request.selected_text,
            conversation_id=request.conversation_id
        )

        # Format the response
        response = QueryResponse(
            answer=result["answer"],
            retrieved_chunks=result["retrieved_chunks"],
            query_id=result["query_id"],
            conversation_id=result["conversation_id"]
        )

        return response
    except ValueError as e:
        logger.error(f"Validation error in query-selection: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing selection query: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")