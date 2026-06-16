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

## Local Setup

### 1. Get free API keys
- **Groq**: https://console.groq.com (free tier)
- **Pinecone**: https://app.pinecone.io (free tier — create an index named `mediqueryX`, dimension `384`, metric `cosine`)

### 2. Configure environment
```bash
cp backend/.env.example backend/.env
# Fill in your GROQ_API_KEY and PINECONE_API_KEY
```

### 3. Run with Docker
```bash
docker-compose up --build
```

### 4. Seed the vector database
```bash
cd backend
pip install -r requirements.txt
python ../scripts/seed_data.py
```

### 5. Open the app
- Frontend: http://localhost:8501
- API docs: http://localhost:8000/docs

## Running without Docker

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

## Deployment (free)
- **Backend** → [Render](https://render.com) (connect GitHub repo, set env vars)
- **Frontend** → [Hugging Face Spaces](https://huggingface.co/spaces) (Streamlit SDK)
