import json
import os
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

class WoowacourseRAG:
    def __init__(self, jsonl_path="woowacourse_rag_dataset.jsonl"):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.jsonl_path = os.path.join(base_dir, jsonl_path)
        self._documents = []
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.index = None

    def load_documents(self):
        with open(self.jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                record = json.loads(line)
                self._documents.append(record)
                
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
        
    @property
    def documents(self):
        return self._documents
