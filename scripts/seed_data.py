"""
Run this once to seed Pinecone with sample medical FAQ data.
Usage: python scripts/seed_data.py
"""

import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../backend"))

from app.services.pinecone_service import upsert_chunks
from app.api.ingest import chunk_text
from app.core.config import settings
import uuid

SAMPLE_FAQS = [
    """Hypertension (high blood pressure) is a condition where blood pressure is consistently
    above 130/80 mmHg. Risk factors include obesity, smoking, lack of exercise, high sodium intake,
    and family history. It is often called a silent killer because it has no symptoms.
    Regular monitoring and lifestyle changes are key to management.""",

    """Type 2 diabetes occurs when the body does not use insulin properly. Symptoms include
    frequent urination, excessive thirst, fatigue, and blurred vision. It is managed through
    diet, exercise, and sometimes medication. A HbA1c level above 6.5% is diagnostic.""",

    """Common cold symptoms include runny nose, sore throat, cough, and mild fever. It is caused
    by rhinoviruses. There is no cure; treatment is supportive with rest, fluids, and
    over-the-counter medications. Antibiotics are not effective against viral infections.""",

    """Asthma is a chronic lung condition causing airway inflammation and narrowing. Symptoms
    include wheezing, shortness of breath, and chest tightness. Triggers include allergens,
    exercise, cold air, and respiratory infections. It is managed with inhalers.""",

    """HIPAA (Health Insurance Portability and Accountability Act) protects patient health
    information. Covered entities must implement safeguards for protected health information (PHI).
    Patients have the right to access their own records and request corrections.""",
]


async def main():
    print("Seeding Pinecone with sample medical FAQ data...")
    all_chunks = []
    for text in SAMPLE_FAQS:
        chunks = chunk_text(text, chunk_size=settings.CHUNK_SIZE, overlap=settings.CHUNK_OVERLAP)
        for chunk in chunks:
            all_chunks.append({
                "id": str(uuid.uuid4()),
                "text": chunk,
                "metadata": {"source": "seed_data"},
            })

    count = await upsert_chunks(all_chunks)
    print(f"✅ Upserted {count} vectors to Pinecone index '{settings.PINECONE_INDEX_NAME}'")


if __name__ == "__main__":
    asyncio.run(main())
