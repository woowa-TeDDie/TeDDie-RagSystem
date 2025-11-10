import json
import os

from sentence_transformers import SentenceTransformer

class WoowacourseRAG:
    def __init__(self, jsonl_path="woowacourse_rag_dataset.jsonl"):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.jsonl_path = os.path.join(base_dir, jsonl_path)
        self._documents = []
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    def load_documents(self):
        with open(self.jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                record = json.loads(line)
                self._documents.append(record)
                
    def embed_text(self, text: str):
        return self.model.encode(text)

    @property
    def documents(self):
        return self._documents
