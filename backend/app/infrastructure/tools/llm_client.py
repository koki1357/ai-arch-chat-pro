from openai import OpenAI
from typing import Optional


class LLMClient:
    _instance: Optional['LLMClient'] = None
    _client: Optional[OpenAI] = None

    def __new__(cls, api_key: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, api_key: Optional[str] = None):
        if self._client is None and api_key is not None:
            self._client = OpenAI(api_key=api_key)

    @property
    def client(self) -> OpenAI:
        if self._client is None:
            raise ValueError("LLMClient has not been initialized with an API key")
        return self._client
