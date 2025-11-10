import pytest

from rag.RagSearch import WoowacourseRAG

def test_load_documents_returns_list():
    rag = WoowacourseRAG()
    rag.load_documents()
    assert isinstance(rag.documents(), list)
    assert len(rag.documents()) > 0
    
def test_documents_have_required_fields():
    rag = WoowacourseRAG()
    rag.load_documents()
    
    for doc in rag.documents:
        assert "repo" in doc
        assert "text" in doc
        assert "url" in doc