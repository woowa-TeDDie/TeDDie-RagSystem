import os
from pathlib import Path

from rag.Loader import DocumentLoader
from rag.Embedder import Embedder
from rag.SearchEngine import FaissSearchEngine

class WoowacourseRAG:
    def __init__(self, jsonl_path="woowacourse_rag_dataset.jsonl"):
        self.loader = DocumentLoader(jsonl_path)
        self._documents = []
        self.embedder = Embedder()
        self.model = self.embedder.model
        self.engine = None 

    def load_documents(self):
        self._documents = self.loader.load()
                
    def embed_text(self, text: str):
        return self.embedder.encode_single(text)
    
    def build_index(self):
        if not self.documents:
            self.load_documents()

        self.engine = FaissSearchEngine(self.embedder, self.documents)
        self.engine.build()
        return self.engine.index
    
    def search(self, query: str, top_k: int = 3):
        if self.engine is None or self.engine.index is None:
            raise ValueError("[ERROR] 인덱스가 구축되지 않았습니다. build_index()를 먼저 호출하세요.")
        return self.engine.search(query, top_k)
    
    def save_index(self, index_path: str):
        if self.engine is None or self.engine.index is None:
            raise ValueError("[ERROR] 인덱스가 구축되지 않았습니다. 저장할 인덱스가 없습니다.")
        self.engine.save(index_path)

    def load_index(self, index_path: str = "faiss_index.bin"):
        if not Path(index_path).exists():
            raise FileNotFoundError(f"[ERROR] 지정된 경로에 인덱스 파일이 없습니다: {index_path}")

        if not self.documents:
            self.load_documents()

        self.engine = FaissSearchEngine(self.embedder, self.documents)
        self.engine.load(index_path)
        
    @property
    def index(self):
        return None if not self.engine else self.engine.index

    @property
    def documents(self):
        return self._documents
