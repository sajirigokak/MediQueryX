"""
Groq service — LLM answer generation and safety validation.
Manages token budgets explicitly per the JD requirement.
"""

from groq import AsyncGroq
from app.core.config import settings

_client = AsyncGroq(api_key=settings.GROQ_API_KEY)

SYSTEM_PROMPT = """You are MediQuery-X, a helpful and cautious medical information assistant.
Answer ONLY using the provided context. If the context doesn't contain enough information,
say so clearly. Never fabricate medical facts. Always recommend consulting a doctor for
personal medical decisions. Keep answers concise and in plain language."""

SAFETY_PROMPT = """You are a medical content safety classifier.
Respond with ONLY 'safe' or 'unsafe'.
Flag as unsafe if the response: gives specific dosage advice, diagnoses a condition,
recommends stopping prescribed medication, or contains dangerous/misleading medical claims.
Response to evaluate: {answer}"""


async def generate_answer(
    query: str,
    context: str,
    history: list[dict],
) -> str:
    """
    Generate a grounded answer using Groq.
    Token budget: MAX_TOKENS from settings (default 1024).
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Include last 4 turns of history to manage token budget
    messages.extend(history[-4:])

    messages.append({
        "role": "user",
        "content": f"Context:\n{context}\n\nQuestion: {query}",
    })

    response = await _client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=messages,
        max_tokens=settings.MAX_TOKENS,
        temperature=settings.TEMPERATURE,
    )
    return response.choices[0].message.content


async def check_safety(answer: str) -> bool:
    """
    Run a lightweight safety check on the generated answer.
    Returns True if safe, False if flagged.
    """
    response = await _client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[{
            "role": "user",
            "content": SAFETY_PROMPT.format(answer=answer),
        }],
        max_tokens=10,
        temperature=0.0,
    )
    verdict = response.choices[0].message.content.strip().lower()
    return verdict == "safe"
