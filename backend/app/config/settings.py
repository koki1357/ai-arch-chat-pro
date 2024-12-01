from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Azure Functions
    AZURE_FUNCTION_URL: str

    # OpenAI
    OPENAI_API_KEY: str

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "logs"

    # Embedding Cache
    EMBEDDING_CACHE_DIR: str = "embeddings_cache"
    USE_EMBEDDING_CACHE: bool = True

    class Config:
        env_file = ".env"
