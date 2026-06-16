from pydantic import BaseModel
from typing import List, Optional


class Message(BaseModel):
    role: str   # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    query: str
    conversation_history: List[Message] = []


class ChatResponse(BaseModel):
    answer: str
    sources_used: int
    is_safe: bool
    error: Optional[str] = None


class IngestRequest(BaseModel):
    texts: List[str]
    source: str = "manual"


class IngestResponse(BaseModel):
    vectors_upserted: int
    chunks_created: int
