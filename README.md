# MediQuery-X v2

Healthcare RAG chatbot powered by **LangGraph**, **FastAPI**, **Pinecone**, and **Groq**.

## Architecture

```
User Query
    │
    ▼
FastAPI /chat endpoint
    │
    ▼
LangGraph Pipeline
  ├── retrieve  →  Pinecone semantic search
  ├── rerank    →  keyword overlap scoring
  ├── generate  →  Groq (llama3-70b) grounded answer
  └── validate  →  safety classifier
    │
    ▼
Streamlit Frontend
```

## Stack
| Layer | Tech |
|---|---|
| Orchestration | LangGraph |
| Backend API | FastAPI + Docker |
| Vector DB | Pinecone |
| LLM | Groq (llama3-70b-8192) |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Frontend | Streamlit |
| Deployment | Render (backend) + HF Spaces (frontend) |

I have attached screenshots of the application as well. This runs on localhost at present. 

