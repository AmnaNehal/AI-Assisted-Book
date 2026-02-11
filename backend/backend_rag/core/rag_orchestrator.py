from typing import Dict, Any, List, Optional
from core.query_parser import QueryParser
from core.context_validator import ContextValidator
from core.answer_generator import AnswerGenerator
from db.qdrant_client import QdrantConnector
from db.neon_connector import NeonConnector
from db.models import Conversation, Query as QueryModel, ModelResponse
from utils.validation import validate_query_text, validate_selected_text, sanitize_input
from utils.logging import log_query, log_retrieved_documents, log_model_response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging
import uuid

logger = logging.getLogger(__name__)


class RAGOrchestrator:
    """
    Main component that orchestrates the RAG process
    """

    def __init__(self, db_session: Optional[AsyncSession] = None):
        self.query_parser = QueryParser()
        self.context_validator = ContextValidator()
        self.answer_generator = AnswerGenerator()
        self.qdrant_connector = QdrantConnector()
        self.neon_connector = NeonConnector()
        self.db_session = db_session

    async def process_global_query(self, query: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a query against the full book content
        """
        # Sanitize and validate input
        sanitized_query = sanitize_input(query)
        if not validate_query_text(sanitized_query):
            raise ValueError("Invalid query text")

        # Log the query
        log_query(sanitized_query, conversation_id, "global")

        # Conversation context (optional)
        if conversation_id and self.db_session:
           try:
            conversation_context = await self._get_conversation_context(conversation_id)
           except Exception as e:
            logger.error(f"Conversation context disabled due to DB error: {e}")
            conversation_context = None

        # Parse query (optional usage)
        _ = self.query_parser.parse_query(sanitized_query)

        # Embedding
        query_embedding = await self.answer_generator.generate_embedding(sanitized_query)

        # Qdrant search
        retrieved_chunks = await self.qdrant_connector.search_chunks(
            query_embedding=query_embedding,
            limit=3
        )

        # Log retrieved docs
        log_retrieved_documents(retrieved_chunks, f"query_{uuid.uuid4()}")

        # Generate answer
        answer_result = await self.answer_generator.generate_answer(
            query=sanitized_query,
            context=retrieved_chunks,
            conversation_context=conversation_context
        )

        # Validate grounding
        validation_result = self.context_validator.validate_global_context(
            query=sanitized_query,
            retrieved_chunks=retrieved_chunks,
            response=answer_result["answer"]
        )

        if not validation_result["is_valid"]:
            logger.warning(f"Answer validation failed: {validation_result['issues']}")

        # ✅ Store query + response only (NO retrieved_documents insert)
        query_record = None
        if self.db_session:
            query_record = await self._store_query_and_response_only(
                conversation_id=conversation_id,
                query_text=sanitized_query,
                query_type="global",
                response_text=answer_result["answer"],
                tokens_used=answer_result["tokens_used"]
            )

        # Log model response
        log_model_response(
            answer_result["answer"],
            f"query_{uuid.uuid4()}",
            answer_result["tokens_used"]
        )

        # ✅ IMPORTANT: API response expects chunk_id (not id)
        formatted_chunks = [
            {
                "chunk_id": str(c.get("id")),
                "content": c.get("content", ""),
                "relevance_score": float(c.get("relevance_score", 0.0)),
                "metadata": c.get("metadata", {}),
                "book_id": c.get("book_id"),
                "chunk_index": c.get("chunk_index"),
            }
            for c in retrieved_chunks
        ]

        return {
            "answer": answer_result["answer"],
            "retrieved_chunks": formatted_chunks,
            "query_id": query_record.id if query_record else f"query_{uuid.uuid4()}",
            "conversation_id": conversation_id,
            "validation_result": validation_result
        }

    async def process_selection_query(self, query: str, selected_text: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a query against only the selected text
        """
        sanitized_query = sanitize_input(query)
        sanitized_selected_text = sanitize_input(selected_text)

        if not validate_query_text(sanitized_query):
            raise ValueError("Invalid query text")

        if not validate_selected_text(sanitized_selected_text):
            raise ValueError("Invalid selected text")

        log_query(sanitized_query, conversation_id, "selection")

        conversation_context = None
       


        # Virtual chunk
        virtual_chunk = {
            "id": f"selection_{uuid.uuid4()}",
            "content": sanitized_selected_text,
            "relevance_score": 1.0,
            "metadata": {},
            "book_id": "selected_text",
            "chunk_index": 0
        }

        retrieved_chunks = [virtual_chunk]
        log_retrieved_documents(retrieved_chunks, f"query_{uuid.uuid4()}")

        answer_result = await self.answer_generator.generate_answer(
            query=sanitized_query,
            context=retrieved_chunks,
            conversation_context=conversation_context
        )

        validation_result = self.context_validator.validate_selected_text_context(
            query=sanitized_query,
            selected_text=sanitized_selected_text,
            response=answer_result["answer"]
        )

        if not validation_result["is_valid"]:
            logger.warning(f"Selected text validation failed: {validation_result['issues']}")

        query_record = None
        if self.db_session:
            query_record = await self._store_query_and_response_only(
                conversation_id=conversation_id,
                query_text=sanitized_query,
                query_type="selection",
                response_text=answer_result["answer"],
                tokens_used=answer_result["tokens_used"],
                selected_text=sanitized_selected_text
            )

        log_model_response(
            answer_result["answer"],
            f"query_{uuid.uuid4()}",
            answer_result["tokens_used"]
        )

        formatted_chunks = [
            {
                "chunk_id": str(c.get("id")),
                "content": c.get("content", ""),
                "relevance_score": float(c.get("relevance_score", 0.0)),
                "metadata": c.get("metadata", {}),
                "book_id": c.get("book_id"),
                "chunk_index": c.get("chunk_index"),
            }
            for c in retrieved_chunks
        ]

        return {
            "answer": answer_result["answer"],
            "retrieved_chunks": formatted_chunks,
            "query_id": query_record.id if query_record else f"query_{uuid.uuid4()}",
            "conversation_id": conversation_id,
            "validation_result": validation_result
        }

    async def _get_conversation_context(self, session_id: str) -> Optional[str]:
        """
        session_id = frontend wala conversation_id (e.g. default_conversation)
        DB me Conversation.session_id me store hota hai, aur QueryModel.conversation_id me Conversation.id
        """
        if not self.db_session:
            return None

        try:
            # Find conversation row by session_id
            conv_res = await self.db_session.execute(
                select(Conversation).where(Conversation.session_id == session_id)
            )
            conv = conv_res.scalar_one_or_none()
            if not conv:
                return None

            # Get last 3 queries
            q_res = await self.db_session.execute(
                select(QueryModel)
                .where(QueryModel.conversation_id == conv.id)
                .order_by(QueryModel.created_at.desc())
                .limit(3)
            )
            queries = q_res.scalars().all()
            if not queries:
                return None

            context_parts = []
            for q in reversed(queries):
                context_parts.append(f"Q: {q.query_text}")
                if q.response:
                    context_parts.append(f"A: {q.response.response_text}")

            return "\n".join(context_parts)

        except Exception as e:
            logger.error(f"Error retrieving conversation context: {e}")
            return None

    async def _store_query_and_response_only(
        self,
        conversation_id: Optional[str],
        query_text: str,
        query_type: str,
        response_text: str,
        tokens_used: int,
        selected_text: Optional[str] = None
    ):
        """
        ✅ IMPORTANT:
        Hum retrieved_documents store nahi kar rahe, kyun ke Qdrant chunk ids
        Postgres document_chunks table me exist nahi karte (website ingest case).
        """
        if not self.db_session:
            class MockQuery:
                id = f"query_{uuid.uuid4()}"
            return MockQuery()

        try:
            # Get or create Conversation by session_id
            if conversation_id:
                res = await self.db_session.execute(
                    select(Conversation).where(Conversation.session_id == conversation_id)
                )
                conversation = res.scalar_one_or_none()
                if not conversation:
                    conversation = Conversation(session_id=conversation_id)
                    self.db_session.add(conversation)
                    await self.db_session.commit()
                    await self.db_session.refresh(conversation)
            else:
                conversation_id = f"conv_{uuid.uuid4()}"
                conversation = Conversation(session_id=conversation_id)
                self.db_session.add(conversation)
                await self.db_session.commit()
                await self.db_session.refresh(conversation)

            # Store Query
            query_record = QueryModel(
                conversation_id=conversation.id,
                query_text=query_text,
                query_type=query_type,
                selected_text=selected_text
            )
            self.db_session.add(query_record)
            await self.db_session.commit()
            await self.db_session.refresh(query_record)

            # Store Response
            response_record = ModelResponse(
                query_id=query_record.id,
                response_text=response_text,
                tokens_used=tokens_used
            )
            self.db_session.add(response_record)
            await self.db_session.commit()

            return query_record

        except Exception as e:
            logger.error(f"Error storing query in database: {e}")
            class MockQuery:
                id = f"query_{uuid.uuid4()}"
            return MockQuery()