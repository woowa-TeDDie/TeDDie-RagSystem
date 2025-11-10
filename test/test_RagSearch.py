import pytest

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
    