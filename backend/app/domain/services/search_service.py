from typing import List

from ..schemas import SystemArchitecture
from ...infrastructure.repositories.system_repository import SystemRepository
from .embedding_service import EmbeddingService


class SearchService:
    def __init__(self, repository: SystemRepository, embedding_service: EmbeddingService):
        self.repository = repository
        self.embedding_service = embedding_service

    def search_similar_systems(self, query: str) -> List[SystemArchitecture]:
        """
        類似システムを検索
        """
        try:
            # 全システムを取得
            all_systems = self.repository.get_all_systems()

            if not all_systems:
                return []

            # 類似度計算
            systems_with_similarity = self.embedding_service.calculate_similarity(
                query=query,
                systems=[system.dict() for system in all_systems]
            )

            # SystemArchitectureオブジェクトに変換
            return [SystemArchitecture(**system) for system in systems_with_similarity]

        except Exception as e:
            raise Exception(f"Failed to search systems: {str(e)}")
