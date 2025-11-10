from sentence_transformers import SentenceTransformer
import numpy as np

class Embedder:
    def __init__(self, model_name="paraphrase-multilingual-MiniLM-L12-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts, show_progress=True):
        return self.model.encode(texts, show_progress_bar=show_progress)
    
    def embed_single(self, text):
        return self.model.encode([text])[0]