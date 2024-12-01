from typing import Optional, List, Dict
from datetime import datetime
from pydantic import BaseModel


class SystemModel(BaseModel):
    id: str
    system_name: str
    description: str
    cloud_provider: str
    cloud_services: List[str]
    team: Dict[str, str]
    repository: Dict[str, str]
    created_at: datetime
    updated_at: Optional[datetime] = None
    type: str = "system_architecture"
