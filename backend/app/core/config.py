from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Groq
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama3-70b-8192"
    MAX_TOKENS: int = 1024
    TEMPERATURE: float = 0.2

    # Pinecone
    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str = "mediqueryX"
    PINECONE_DIMENSION: int = 384  # all-MiniLM-L6-v2

    # Embedding
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # RAG
    TOP_K_RESULTS: int = 5
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 64

    class Config:
        env_file = ".env"


settings = Settings()
