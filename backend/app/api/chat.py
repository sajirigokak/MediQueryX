from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.core.graph import rag_graph

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Run a user query through the full LangGraph pipeline:
    retrieve → rerank → generate → validate
    """
    try:
        initial_state = {
            "query": request.query,
            "conversation_history": [m.model_dump() for m in request.conversation_history],
            "retrieved_docs": [],
            "reranked_docs": [],
            "answer": "",
            "is_safe": True,
            "error": None,
        }

        result = await rag_graph.ainvoke(initial_state)

        return ChatResponse(
            answer=result["answer"],
            sources_used=len(result["reranked_docs"]),
            is_safe=result["is_safe"],
            error=result.get("error"),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
