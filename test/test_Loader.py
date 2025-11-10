import pytest
from rag.Loader import DocumentLoader
from pathlib import Path

def test_loader_reads_jsonl(tmp_path):
    path = tmp_path / "sample.jsonl"
    data = {"repo": "java-lotto", "text": "README", "url": "https://github.com/test"}
    import json
    path.write_text(json.dumps(data) + "\n", encoding="utf-8")

    loader = DocumentLoader(str(path))
    docs = loader.load()

    assert isinstance(docs, list)
    assert len(docs) == 1
    assert docs[0]["repo"] == "java-lotto"

