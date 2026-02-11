# Quickstart Guide: Backend for Book RAG Chatbot

## Prerequisites

- Python 3.11 or higher
- pip package manager
- Git
- Access to Cohere API
- Access to Qdrant Cloud
- Access to Neon Serverless Postgres

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
cd backend_rag
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the `backend_rag` directory with the following content:


```

### 5. Run the Application
```bash
cd backend_rag
uvicorn main:app --reload --port 8000
```

The API will be available at `http://127.0.0.1:8005`.

### 6. API Documentation
Once the application is running, you can access the interactive API documentation at:
- `http://127.0.0.1:8005/docs` (Swagger UI)
- `http://127.0.0.1:8005/redoc` (ReDoc)

## Testing the API

### Query the Full Book
```bash
curl -X POST "http://127.0.0.1:8005/query-global" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main themes in this book?",
    "conversation_id": "test_conv_1"
  }'
```

### Query Selected Text Only
```bash
curl -X POST "http://127.0.0.1:8005/query-selection" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What does this passage mean?",
    "selected_text": "This is the selected text that the user wants to ask about...",
    "conversation_id": "test_conv_2"
  }'
```

### Health Check
```bash
curl -X GET "http://127.0.0.1:8005/status"
```

## Next Steps

1. **Vectorize your book content**: Use the vectorization pipeline to process your book content and store it in Qdrant
2. **Integrate with frontend**: Connect the backend API to your frontend component at `frontend_book/src/components/RagChatbot/`
3. **Configure logging**: Set up logging infrastructure to capture all queries and responses as required by the specification
4. **Performance testing**: Run load tests to ensure the system can handle 100+ concurrent users