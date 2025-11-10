import faiss
import numpy as np
from pathlib import Path

class FaissSearchEngine:
    def __init__(self, embedder, documents):
        self.embedder = embedder
        self.documents = documents
        self.index = None
        
    def build(self, show_progress=True):
        if not self.documents:
            raise ValueError("[ERROR] 문서가 없습니다. 문서를 먼저 로드하세요.")
        
        texts = [doc['text'] for doc in self.documents]
        embeddings = self.embedder.embed(texts, show_progress=show_progress)
        
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings.astype('float32'))
        
    def search(self, query: str, top_k: int = 3):
        if self.index is None:
            raise ValueError("[ERROR] 인덱스가 구축되지 않았습니다. build() 메서드를 먼저 호출하세요.")
        
        query_vector = self.embedder.embed([query]).astype('float32')
        distances, indices = self.index.search(query_vector, top_k)
        
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            doc = self.documents[idx].copy()
            doc['similarity_score'] = float(distance)
            results.append(doc)
        return results

    def save(self, index_path: str):
        if self.index is None:
            raise ValueError("[ERROR] 인덱스가 구축되지 않았습니다. 저장할 인덱스가 없습니다.")
        faiss.write_index(self.index, index_path)
        
    def load(self, index_path: str):
        if not Path(index_path).exists():
            raise FileNotFoundError(f"[ERROR] 지정된 경로에 인덱스 파일이 없습니다: {index_path}")
        
        self.index = faiss.read_index(index_path)