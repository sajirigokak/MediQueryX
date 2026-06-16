"""
LangGraph graph definition for MediQuery-X.

Graph flow:
  retrieve → rerank → generate → validate → END
                                    ↓ (if unsafe)
                                  refuse
"""

from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from app.services.pinecone_service import retrieve_docs
from app.services.groq_service import generate_answer, check_safety
from app.core.config import settings


# ── State ──────────────────────────────────────────────────────────────────────

class GraphState(TypedDict):
    query: str
    conversation_history: List[dict]   # [{role, content}, ...]
    retrieved_docs: List[str]
    reranked_docs: List[str]
    answer: str
    is_safe: bool
    error: Optional[str]


# ── Nodes ──────────────────────────────────────────────────────────────────────

async def retrieve_node(state: GraphState) -> GraphState:
    """Retrieve top-K relevant chunks from Pinecone."""
    try:
        docs = await retrieve_docs(state["query"], top_k=settings.TOP_K_RESULTS)
        return {**state, "retrieved_docs": docs}
    except Exception as e:
        return {**state, "retrieved_docs": [], "error": str(e)}


async def rerank_node(state: GraphState) -> GraphState:
    """
    Simple reranking: score each chunk by keyword overlap with query.
    Replace with a cross-encoder for production.
    """
    query_terms = set(state["query"].lower().split())
    scored = []
    for doc in state["retrieved_docs"]:
        doc_terms = set(doc.lower().split())
        score = len(query_terms & doc_terms)
        scored.append((score, doc))
    scored.sort(reverse=True)
    reranked = [doc for _, doc in scored[:3]]  # keep top 3 after rerank
    return {**state, "reranked_docs": reranked}


async def generate_node(state: GraphState) -> GraphState:
    """Generate an answer grounded in the retrieved context."""
    context = "\n\n".join(state["reranked_docs"])
    answer = await generate_answer(
        query=state["query"],
        context=context,
        history=state["conversation_history"],
    )
    return {**state, "answer": answer}


async def validate_node(state: GraphState) -> GraphState:
    """Check if the generated answer is safe and medically appropriate."""
    is_safe = await check_safety(state["answer"])
    return {**state, "is_safe": is_safe}


async def refuse_node(state: GraphState) -> GraphState:
    """Return a safe fallback for flagged responses."""
    return {
        **state,
        "answer": (
            "I'm sorry, I can't provide a reliable answer to that question. "
            "Please consult a licensed healthcare provider for medical advice."
        ),
    }


# ── Routing ────────────────────────────────────────────────────────────────────

def route_after_validate(state: GraphState) -> str:
    return "end" if state["is_safe"] else "refuse"


# ── Graph ──────────────────────────────────────────────────────────────────────

def build_graph() -> StateGraph:
    graph = StateGraph(GraphState)

    graph.add_node("retrieve", retrieve_node)
    graph.add_node("rerank", rerank_node)
    graph.add_node("generate", generate_node)
    graph.add_node("validate", validate_node)
    graph.add_node("refuse", refuse_node)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "rerank")
    graph.add_edge("rerank", "generate")
    graph.add_edge("generate", "validate")
    graph.add_conditional_edges(
        "validate",
        route_after_validate,
        {"end": END, "refuse": "refuse"},
    )
    graph.add_edge("refuse", END)

    return graph.compile()


# Compile once at startup
rag_graph = build_graph()
