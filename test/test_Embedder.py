from rag.Embedder import Embedder
import numpy as np

def test_embedder_initialization():
    embedder = Embedder()
    assert embedder.model is not None

def test_encode_single_returns_vector():
    embedder = Embedder()
    vector = embedder.encode_single("로또 게임")
    assert isinstance(vector, np.ndarray)
    assert vector.shape[0] > 0

def test_encode_multiple_texts():
    embedder = Embedder()
    vectors = embedder.encode(["자동차 경주", "숫자 야구"])
    assert vectors.shape[0] == 2
