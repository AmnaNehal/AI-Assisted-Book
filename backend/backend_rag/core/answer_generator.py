import cohere
from typing import List, Dict, Any
import logging
from config.settings import settings

logger = logging.getLogger(__name__)


class AnswerGenerator:
    """
    Component for generating answers using Cohere API
    """

    def __init__(self):
        self.co = cohere.AsyncClient(settings.COHERE_API_KEY)
        self.chat_model = settings.COHERE_MODEL

    async def generate_answer(
        self,
        query: str,
        context: List[Dict[str, Any]],
        conversation_context: str = None
    ) -> Dict[str, Any]:
        try:
            formatted_context = self._format_context(context)
            prompt = self._build_prompt(query, formatted_context, conversation_context)

            resp = await self.co.chat(
                model=self.chat_model,
                message=prompt,
                temperature=0.3,
                max_tokens=250,
            )

            generated_text = (getattr(resp, "text", None) or "").strip()

            if not generated_text:
                generated_text = "I don't have enough information from the book content to answer that yet."

            return {
                "answer": generated_text,
                "tokens_used": len(generated_text.split()),
                "model_used": self.chat_model
            }

        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            raise

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Cohere embed compatible with your AsyncClient signature:
        - uses texts=[...]
        - embed-english-v3.0 requires input_type
        """
        try:
            response = await self.co.embed(
                model=settings.COHERE_EMBED_MODEL,   # embed-english-v3.0
                texts=[text],
                input_type="search_query",
            )

            embeddings = getattr(response, "embeddings", None)

            if isinstance(embeddings, list):
                return embeddings[0]

            if embeddings is not None and hasattr(embeddings, "float"):
                return embeddings.float[0]

            if isinstance(response, dict) and "embeddings" in response:
                return response["embeddings"][0]

            raise RuntimeError(f"Unexpected embed response format: {type(response)}")

        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    def _format_context(self, context: List[Dict[str, Any]]) -> str:
        if not context:
            return (
                "Relevant information from the book:\n\n"
                "(No relevant chunks were retrieved yet.)\n\n"
            )

        formatted_context = "Relevant information from the book:\n\n"
        for i, chunk in enumerate(context):
            content = chunk.get("content", "")
            relevance_score = chunk.get("relevance_score", 0)
            formatted_context += (
                f"Source {i+1} (Relevance: {relevance_score:.2f}):\n"
                f"{content}\n\n"
            )
        return formatted_context

    def _build_prompt(self, query: str, context: str, conversation_context: str = None) -> str:
        prompt = (
            "You are an AI assistant that answers questions based only on the provided information from the book.\n"
            "If the information is not present, say you don't have enough information yet.\n\n"
        )

        if conversation_context:
            prompt += f"Previous conversation context:\n{conversation_context}\n\n"

        prompt += context
        prompt += f"Question: {query}\n\nAnswer:"
        return prompt