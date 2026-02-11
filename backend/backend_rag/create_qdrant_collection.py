import asyncio
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import VectorParams, Distance
from config.settings import settings

async def main():
    client = AsyncQdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY
    )

    name = settings.QDRANT_COLLECTION_NAME  # book_content_chunks

    exists = await client.collection_exists(collection_name=name)
    if not exists:
        # embed-english-v3.0 vectors are 1024 dims
        await client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
        )
        print(f"✅ Qdrant collection created: {name}")
    else:
        print(f"✅ Qdrant collection already exists: {name}")

    await client.close()

if __name__ == "__main__":
    asyncio.run(main())