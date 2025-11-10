from pathlib import Path
import os
import json

class DocumentLoader:
    def __init__(self, jsonl_path="woowacourse_rag_dataset.jsonl"):
        base_dir = Path(os.path.dirname(os.path.dirname(__file__)))
        self.path = base_dir / jsonl_path
        
    def load(self):
        if not self.path.exists():
            raise FileNotFoundError(f"[ERROR] 지정된 경로에 JSONL 파일이 없습니다: {self.path}")
        with open(self.path, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f]
