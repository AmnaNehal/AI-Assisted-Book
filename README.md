
# 📚 AI-Assisted Book — Production-Ready RAG Chatbot

A full-stack Retrieval-Augmented Generation (RAG) chatbot system that enables users to ask contextual questions about a book and receive grounded, accurate answers powered by semantic vector search and LLM generation.

Designed with production deployment, scalability, and clean architecture principles in mind.

---

## 🔍 Project Overview

This system combines:

* 🔎 **Semantic search** using Qdrant vector database
* 🧠 **LLM-based answer generation** via Cohere
* ⚡ **Async FastAPI backend**
* 🌐 **Modern React + Docusaurus frontend**
* ☁️ **Cloud deployment (Render + Vercel)**

The chatbot ensures responses are grounded in retrieved book content, minimizing hallucinations and improving answer reliability.

---

## 🏗 Architecture

```
User Question
      ↓
Cohere Embedding (embed-english-v3.0)
      ↓
Qdrant Vector Search
      ↓
Top-K Relevant Chunks
      ↓
Prompt Construction (Context + Query)
      ↓
Cohere Chat Model
      ↓
Validated, Grounded Response
```

---

## ⚙️ Tech Stack

### Backend

* **FastAPI (Python 3.11)**
* Async SQLAlchemy
* Cohere v5 API
* Qdrant Cloud (vector database)
* Neon PostgreSQL (conversation persistence)

### Frontend

* React
* Docusaurus
* TypeScript
* Modular component architecture

### Deployment

* Backend: Render
* Frontend: Vercel
* Environment-based configuration
* CORS-managed API access

---

## 🧠 Core Engineering Highlights

### ✅ Retrieval-Augmented Generation (RAG)

* Query embedding generation
* Semantic similarity search
* Context-aware prompt engineering
* Response validation layer

### ✅ Async-first Backend

* Fully async request handling
* Non-blocking database access
* Clean separation of concerns:

  * `core/` (RAG orchestration)
  * `api/` (routes)
  * `db/` (data layer)
  * `utils/` (logging & validation)

### ✅ Production Deployment Ready

* Environment variable configuration
* Proper `.gitignore`
* Cloud vector DB integration
* CORS configuration for multi-origin deployment

### ✅ Frontend Engineering

* Scrollable chat UI
* Typing indicator
* Auto-scroll behavior
* Clean modular styling
* Environment-based backend switching

---

## 📁 Project Structure

```
backend/
  backend_rag/
    api/
    core/
    db/
    config/
    utils/
    main.py

frontend_book/
  src/
    components/RagChatbot/
    theme/Layout/
```

---

## 🚀 Performance Optimizations

* Reduced retrieval chunk count
* Controlled max token generation
* Optional embedding caching
* Async database usage
* Clean prompt construction

---

## 🔐 Security & Environment Handling

* No secrets committed
* Environment-based configuration
* Separate dev and production backend URLs
* Proper CORS management

---

## 📡 API Endpoint

### POST `/api/query-global`

```json
{
  "query": "What is ROS 2 nervous system?",
  "conversation_id": "default_conversation"
}
```

Returns:

* Generated answer
* Retrieved chunks
* Validation result
* Query metadata

---

## 📈 Future Improvements

* Streaming responses
* Re-ranking layer
* Vector cache layer
* Token usage analytics
* Multi-book indexing

---

## 💼 Resume Value

This project demonstrates:

* End-to-end full-stack development
* LLM integration in production context
* Vector database implementation
* Cloud deployment workflows
* Async Python architecture
* Scalable modular code structure
* Real-world AI system engineering

---

## 👨‍💻 Author

Full-stack AI Engineer focused on scalable RAG systems, production-ready LLM integrations, and modern cloud deployment architecture.


