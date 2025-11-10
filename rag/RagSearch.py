import os
import faiss
import numpy as np

from pathlib import Path
from sentence_transformers import SentenceTransformer

from Loader import DocumentLoader

class WoowacourseRAG:
    def __init__(self, jsonl_path="woowacourse_rag_dataset.jsonl"):
        self.loader = DocumentLoader(jsonl_path)
        self._documents = []
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.index = None

    def load_documents(self):
        self._documents = self.loader.load()
                
    def embed_text(self, text: str):
        return self.model.encode(text)
    
    def build_index(self):
        if not self.documents:
            self.load_documents()

        texts = [doc['text'] for doc in self.documents]
        embeddings = self.model.encode(texts, show_progress_bar=True)
        
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype('float32'))
        
    def search(self, query: str, top_k: int = 3):
        if self.index is None:
            raise ValueError("[ERROR] 인덱스가 구축되지 않았습니다. build_index() 메서드를 먼저 호출하세요.")
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(
            query_embedding.astype('float32'), 
            top_k
        )
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            doc = self.documents[idx].copy()
            doc['similarity_score'] = float(distance)
            results.append(doc)
        return results
    
    def save_index(self, index_path: str):
        if self.index is None:
            raise ValueError("[ERROR] 인덱스가 구축되지 않았습니다. 저장할 인덱스가 없습니다.")
        faiss.write_index(self.index, index_path)
        
    def load_index(self, index_path: str = "faiss_index.bin"):
        if not Path(index_path).exists():
            raise FileNotFoundError(f"[ERROR] 지정된 경로에 인덱스 파일이 없습니다: {index_path}")
        
        if not self.documents:
            self.load_documents()
            
        self.index = faiss.read_index(index_path)
        
    @property
    def documents(self):
        return self._documents
