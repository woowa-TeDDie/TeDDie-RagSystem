import pytest
from rag.RagSearch import WoowacourseRAG
from pathlib import Path

def test_rag_build_and_search(tmp_path):
    rag = WoowacourseRAG()
    rag.build_index()
    results = rag.search("로또", top_k=2)
    assert isinstance(results, list)
    assert len(results) == 2

def test_rag_save_and_load_index(tmp_path):
    rag1 = WoowacourseRAG()
    rag1.build_index()
    path = tmp_path / "index.bin"
    rag1.save_index(str(path))

    rag2 = WoowacourseRAG()
    rag2.load_index(str(path))
    assert rag2.index is not None
