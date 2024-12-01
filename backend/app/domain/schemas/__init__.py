from typing import List, Dict, Optional
from pydantic import BaseModel
from datetime import datetime


class SystemArchitecture(BaseModel):
    id: str
    system_name: str
    description: str
    cloud_provider: str
    cloud_services: List[str]
    team: Dict[str, str]
    repository: Dict[str, str]
    created_at: str
    updated_at: Optional[str]
    type: str = "system_architecture"
    similarity: Optional[float] = None


class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: datetime = datetime.utcnow()


class SearchResponse(BaseModel):
    count: int
    documents: List[SystemArchitecture]
