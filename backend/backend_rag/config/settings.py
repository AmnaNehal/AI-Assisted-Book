from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "Book RAG Chatbot Backend"
    APP_DESCRIPTION: str = "Backend service for a Retrieval-Augmented Generation (RAG) chatbot that allows users to ask questions about book content"
    APP_VERSION: str = "1.0.0"
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # API Keys and URLs
    COHERE_API_KEY: str
    QDRANT_API_KEY: str
    QDRANT_URL: str
    NEON_DB_URL: str
    
    # Cohere settings
    COHERE_MODEL: str = "command-r-08-2024"  # Default Cohere model
    COHERE_EMBED_MODEL: str = "embed-english-v3.0"  # Default embedding model
    
    # Qdrant settings
    QDRANT_COLLECTION_NAME: str = "book_content_chunks"
    
    # Application settings
    MAX_CONCURRENT_REQUESTS: int = 100
    RESPONSE_TIMEOUT: int = 30  # seconds
    CHUNK_SIZE: int = 512  # tokens
    OVERLAP_SIZE: int = 50  # tokens
    
    class Config:
        env_file = ".env"


settings = Settings()