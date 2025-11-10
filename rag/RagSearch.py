import json
import os

class WoowacourseRAG:
    def __init__(self, jsonl_path="woowacourse_rag_dataset.jsonl"):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.jsonl_path = os.path.join(base_dir, jsonl_path)
        self._documents = []

    def load_documents(self):
        with open(self.jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                record = json.loads(line)
                self._documents.append(record)

    @property
    def documents(self):
        """_documents 리스트를 읽기 전용으로 접근할 수 있도록 함."""
        return self._documents
