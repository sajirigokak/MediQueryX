"""
Pinecone service — embedding generation and vector retrieval.
"""

from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from app.core.config import settings

# Initialise once
_embedder = SentenceTransformer(settings.EMBEDDING_MODEL)
_pc = Pinecone(api_key=settings.PINECONE_API_KEY)
_index = _pc.Index(settings.PINECONE_INDEX_NAME)


def embed(text: str) -> list[float]:
    """Return a normalised embedding vector for a string."""
    return _embedder.encode(text, normalize_embeddings=True).tolist()


async def retrieve_docs(query: str, top_k: int = 5) -> list[str]:
    """
    Embed the query and retrieve the top-K matching chunks from Pinecone.
    Returns a list of text strings (the chunk content).
    """
    vector = embed(query)
    response = _index.query(vector=vector, top_k=top_k, include_metadata=True)
    docs = [match["metadata"]["text"] for match in response["matches"]]
    return docs


async def upsert_chunks(chunks: list[dict]) -> int:
    """
    Upsert a list of chunks into Pinecone.
    Each chunk: {"id": str, "text": str, "metadata": dict}
    Returns the number of vectors upserted.
    """
    vectors = [
        {
            "id": chunk["id"],
            "values": embed(chunk["text"]),
            "metadata": {"text": chunk["text"], **chunk.get("metadata", {})},
        }
        for chunk in chunks
    ]
    _index.upsert(vectors=vectors)
    return len(vectors)
