# Book_Creation_UsingAI

# Book RAG Chatbot Backend

Backend service for a Retrieval-Augmented Generation (RAG) chatbot that allows users to ask questions about book content. The system uses FastAPI for the backend, Qdrant Cloud for vector storage, Neon Serverless Postgres for metadata, and Cohere API for embeddings and text generation.

## Features

- **Question Answering**: Ask questions about book content and receive accurate answers
- **Selected Text Mode**: Ask questions about only user-selected text
- **Conversation History**: Maintain context across multiple exchanges
- **Full Logging**: All queries, retrieved document IDs, and model responses are logged
- **Free-tier Optimized**: Designed to operate within free-tier limits of Qdrant and Neon

## Architecture

The system follows an agent-style architecture with clear separation of concerns:

- **Query Parser**: Processes and interprets user queries
- **Qdrant Connector**: Handles vector storage and retrieval
- **Neon Connector**: Manages metadata storage
- **Context Validator**: Ensures responses are grounded in provided context
- **Answer Generator**: Uses Cohere API to generate responses
- **RAG Orchestrator**: Coordinates the entire RAG process

## Prerequisites

- Python 3.11 or higher
- pip package manager
- Access to Cohere API
- Access to Qdrant Cloud
- Access to Neon Serverless Postgres

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   cd backend_rag
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file in the `backend_rag` directory with the following content:
   ```env
   COHERE_API_KEY=your_cohere_api_key
   QDRANT_API_KEY=your_qdrant_api_key
   QDRANT_URL=your_qdrant_url
   NEON_DB_URL=your_neon_db_url
   ```

5. Run the application:
   ```bash
   cd backend_rag
   uvicorn main:app --reload --port 8000
   ```

The API will be available at `http://localhost:8000`.

## API Endpoints

### Health Check
- `GET /status` - Check if the service is running and healthy

### Query Endpoints
- `POST /query-global` - Query the full book content
- `POST /query-selection` - Query only user-selected text

## API Documentation

Once the application is running, you can access the interactive API documentation at:
- `http://localhost:8000/docs` (Swagger UI)
- `http://localhost:8000/redoc` (ReDoc)

## Testing the API

### Query the Full Book
```bash
curl -X POST "http://localhost:8000/query-global" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main themes in this book?",
    "conversation_id": "test_conv_1"
  }'
```

### Query Selected Text Only
```bash
curl -X POST "http://localhost:8000/query-selection" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What does this passage mean?",
    "selected_text": "This is the selected text that the user wants to ask about...",
    "conversation_id": "test_conv_2"
  }'
```

## Configuration

The application can be configured via environment variables in the `.env` file:

- `COHERE_API_KEY`: Your Cohere API key
- `QDRANT_API_KEY`: Your Qdrant API key
- `QDRANT_URL`: Your Qdrant cluster URL
- `NEON_DB_URL`: Your Neon Postgres connection string
- `HOST`: Host to run the server on (default: 0.0.0.0)
- `PORT`: Port to run the server on (default: 8000)
- `RELOAD`: Whether to enable auto-reload (default: True)

## Free-tier Limitations

This system is designed to operate within the free-tier limits of Qdrant and Neon. The rate limiting component helps ensure compliance with API usage limits.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

[Specify your license here]