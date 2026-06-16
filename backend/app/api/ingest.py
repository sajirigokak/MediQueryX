"""
Ingest endpoint — accepts raw text, chunks it, embeds and upserts to Pinecone.
Chunking strategy: fixed-size with overlap (configurable in settings).
"""

import uuid
from fastapi import APIRouter, HTTPException
from app.models.schemas import IngestRequest, IngestResponse
from app.services.pinecone_service import upsert_chunks
from app.core.config import settings

router = APIRouter()


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """
    Split text into overlapping fixed-size chunks (by word count).
    Overlap helps preserve context across chunk boundaries.
    """
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


@router.post("/", response_model=IngestResponse)
async def ingest(request: IngestRequest):
    """
    Chunk, embed, and upsert documents into Pinecone.
    """
    try:
        all_chunks = []
        for text in request.texts:
            chunks = chunk_text(
                text,
                chunk_size=settings.CHUNK_SIZE,
                overlap=settings.CHUNK_OVERLAP,
            )
            for chunk in chunks:
                all_chunks.append({
                    "id": str(uuid.uuid4()),
                    "text": chunk,
                    "metadata": {"source": request.source},
                })

        upserted = await upsert_chunks(all_chunks)

        return IngestResponse(
            vectors_upserted=upserted,
            chunks_created=len(all_chunks),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
