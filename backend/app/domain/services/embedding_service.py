from typing import List, Dict
import numpy as np
from openai import OpenAI
import pickle
from pathlib import Path


class EmbeddingService:
    def __init__(self, api_key: str, cache_dir: str = "embeddings_cache"):
        self.client = OpenAI(api_key=api_key)
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _get_cache_path(self, text: str) -> Path:
        """キャッシュファイルのパスを生成"""
        import hashlib
        text_hash = hashlib.md5(text.encode()).hexdigest()
        return self.cache_dir / f"{text_hash}.pkl"

    def get_embedding(self, text: str, use_cache: bool = True) -> np.ndarray:
        """テキストのembeddingを取得（キャッシュ対応）"""
        cache_path = self._get_cache_path(text)

        if use_cache and cache_path.exists():
            with open(cache_path, 'rb') as f:
                return pickle.load(f)

        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
            dimensions=1536
        )

        embedding = np.array(response.data[0].embedding)

        if use_cache:
            with open(cache_path, 'wb') as f:
                pickle.dump(embedding, f)

        return embedding

    def calculate_similarity(self, query: str, documents: List[Dict])-> List[Dict]:
        """クエリと各ドキュメントの類似度を計算"""
        query_embedding = self.get_embedding(query)

        results = []
        for doc in documents:
            doc_embedding = self.get_embedding(doc['description'])
            similarity = np.dot(query_embedding, doc_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
            )
            doc_copy = doc.copy()
            doc_copy['similarity'] = float(similarity * 100)
            results.append(doc_copy)

        return sorted(results, key=lambda x: x['similarity'], reverse=True)
