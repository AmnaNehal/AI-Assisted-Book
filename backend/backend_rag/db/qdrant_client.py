from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


class QdrantConnector:
    """
    Connector class for interacting with Qdrant vector database
    NOTE: Using sync QdrantClient, so DO NOT use await on client methods.
    """

    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            prefer_grpc=False
        )
        self.collection_name = settings.QDRANT_COLLECTION_NAME

    async def create_collection(self):
        """
        Create the collection for storing book content chunks if it doesn't exist
        """
        try:
            collections = self.client.get_collections()  # ✅ no await
            collection_names = [col.name for col in collections.collections]

            if self.collection_name not in collection_names:
                # Cohere embed-english-v3.0 = 1024 dims (v3)
                self.client.create_collection(  # ✅ no await
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=1024,
                        distance=models.Distance.COSINE
                    )
                )
                logger.info(f"Created collection: {self.collection_name}")
            else:
                logger.info(f"Collection {self.collection_name} already exists")

        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            raise

    async def insert_chunks(self, chunks: List[Dict[str, Any]]):
        """
        Insert document chunks into the Qdrant collection
        Each chunk should have: id, content, embedding, metadata
        """
        try:
            points = []
            for chunk in chunks:
                point = models.PointStruct(
                    id=chunk["id"],
                    vector=chunk["embedding"],
                    payload={
                        "content": chunk["content"],
                        "book_id": chunk.get("book_id"),
                        "chunk_index": chunk.get("chunk_index"),
                        "metadata": chunk.get("metadata", {})
                    }
                )
                points.append(point)

            self.client.upsert(  # ✅ no await
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"Inserted {len(chunks)} chunks into Qdrant")

        except Exception as e:
            logger.error(f"Error inserting chunks: {e}")
            raise

    async def search_chunks(self, query_embedding: List[float], limit: int = 5, filters: Optional[Dict] = None):
        """
        Search for relevant chunks based on query embedding
        """
        try:
            search_filter = None
            if filters:
                filter_conditions = []
                for key, value in filters.items():
                    filter_conditions.append(
                        models.FieldCondition(
                            key=key,
                            match=models.MatchValue(value=value)
                        )
                    )
                if filter_conditions:
                    search_filter = models.Filter(must=filter_conditions)

            results = self.client.search(  # ✅ no await
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                query_filter=search_filter,
                with_payload=True
            )

            formatted_results = []
            for result in results:
                payload = result.payload or {}
                formatted_results.append({
                    "id": str(result.id),
                    "content": payload.get("content", ""),
                    "relevance_score": float(result.score),
                    "metadata": payload.get("metadata", {}),
                    "book_id": payload.get("book_id"),
                    "chunk_index": payload.get("chunk_index")
                })

            logger.info(f"Found {len(formatted_results)} relevant chunks")
            return formatted_results

        except Exception as e:
            logger.error(f"Error searching chunks: {e}")
            raise

    async def delete_collection(self):
        """
        Delete the collection (useful for testing or re-initialization)
        """
        try:
            self.client.delete_collection(collection_name=self.collection_name)  # ✅ no await
            logger.info(f"Deleted collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
            raise