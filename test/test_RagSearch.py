import pytest
from pathlib import Path

from rag.RagSearch import WoowacourseRAG

def test_load_documents_returns_list():
    rag = WoowacourseRAG()
    rag.load_documents()
    
    assert isinstance(rag.documents, list)
    assert len(rag.documents) > 0

def test_documents_have_required_fields():
    rag = WoowacourseRAG()
    rag.load_documents()

    for doc in rag.documents:
        assert "repo" in doc
        assert "text" in doc
        assert "url" in doc
    
def test_embedding_model_initialization():
    rag = WoowacourseRAG()
    assert rag.model is not None
    
def test_embedding_single_test_returns_vector():
    rag = WoowacourseRAG()
    text = "자동차 경주 게임"
    embedding = rag.embed_text(text)
    
    assert embedding is not None
    assert len(embedding.shape) == 1
    assert embedding.shape[0] > 0

def test_build_index_creates_faiss_index():
    rag = WoowacourseRAG()
    rag.build_index()
    
    assert rag.index is not None
    
def test_index_contains_all_documents():
    rag = WoowacourseRAG()
    rag.build_index()
    
    assert rag.index.ntotal == len(rag.documents)
    
def test_build_index_loads_documents_automatically():
    rag = WoowacourseRAG()
    rag.build_index()
    
    assert len(rag.documents) > 0
    
def test_search_returns_list():
    rag = WoowacourseRAG()
    rag.build_index()
    
    results = rag.search("자동차 경주", top_k=3)
    
    assert isinstance(results, list)
    assert len(results) == 3


def test_search_result_has_required_fields():
    rag = WoowacourseRAG()
    rag.build_index()
    
    results = rag.search("로또", top_k=1)
    result = results[0]
    
    assert "repo" in result
    assert "text" in result
    assert "url" in result
    assert "similarity_score" in result


def test_search_returns_most_similar_first():
    rag = WoowacourseRAG()
    rag.build_index()
    
    results = rag.search("숫자 야구", top_k=3)
    scores = [r["similarity_score"] for r in results]
    
    assert scores == sorted(scores)


def test_search_without_index_raises_error():
    rag = WoowacourseRAG()
    
    with pytest.raises(ValueError, match="인덱스"):
        rag.search("query")


def test_search_with_different_top_k():
    rag = WoowacourseRAG()
    rag.build_index()
    
    results_2 = rag.search("TDD", top_k=2)
    results_5 = rag.search("TDD", top_k=5)
    
    assert len(results_2) == 2
    assert len(results_5) == 5
    
def test_save_index_creates_file(tmp_path):
    rag = WoowacourseRAG()
    rag.build_index()
    
    index_path = tmp_path / "test_index.bin"
    rag.save_index(str(index_path))
    
    assert index_path.exists()
    
def test_save_without_index_raises_error():
    rag = WoowacourseRAG()
    
    with pytest.raises(ValueError, match="인덱스"):
        rag.save_index("test.bin")
