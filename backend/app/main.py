from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.chat import router as chat_router
from app.api.ingest import router as ingest_router
from app.core.config import settings

app = FastAPI(
    title="MediQuery-X",
    description="Healthcare RAG chatbot powered by LangGraph + Groq + Pinecone",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(ingest_router, prefix="/api/v1/ingest", tags=["ingest"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "2.0.0"}
