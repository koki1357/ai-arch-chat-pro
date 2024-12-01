import os
import requests
from typing import List

from ..models.system_model import SystemModel


class SystemRepository:
    def __init__(self):
        self.base_url = os.getenv('AZURE_FUNCTION_URL')

    def get_all_systems(self) -> List[SystemModel]:
        """全システムを取得"""
        try:
            response = requests.get(f"{self.base_url}/select-all-system")
            if response.status_code == 200:
                data = response.json()
                return [SystemModel(**item) for item in data["documents"]]
            return []
        except Exception as e:
            raise Exception(f"Failed to fetch systems: {str(e)}")
