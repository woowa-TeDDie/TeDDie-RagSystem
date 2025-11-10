import pytest
from rag.SearchEngine import FaissSearchEngine
from rag.Embedder import Embedder

def test_build_index_creates_faiss_index():
    embedder = Embedder()
    docs = [
        {"repo": "java-lotto", "text": "Lotto game", "url": ""},
        {"repo": "java-racingcar", "text": "Car racing", "url": ""}
    ]
    engine = FaissSearchEngine(embedder, docs)
    engine.build()
    assert engine.index is not None
    assert engine.index.ntotal == 2

def test_search_returns_results():
    embedder = Embedder()
    docs = [
        {"repo": "java-lotto", "text": "Lotto game", "url": ""},
        {"repo": "java-racingcar", "text": "Car racing", "url": ""}
    ]
    engine = FaissSearchEngine(embedder, docs)
    engine.build()
    results = engine.search("lotto", top_k=1)
    assert isinstance(results, list)
    assert "repo" in results[0]
    assert "similarity_score" in results[0]
