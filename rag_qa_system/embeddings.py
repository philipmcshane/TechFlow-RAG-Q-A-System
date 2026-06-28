"""
Thin LangChain-compatible wrapper around ChromaDB's built-in ONNX embedding.
"""

from typing import List
import numpy as np
from langchain_core.embeddings import Embeddings
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction


class OnnxEmbeddings(Embeddings):
    """ChromaDB's ONNX all-MiniLM-L6-v2 model, adapted for LangChain."""

    def __init__(self):
        self._fn = DefaultEmbeddingFunction()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        # .tolist() converts numpy.float32 → Python float (required by ChromaDB 1.x)
        return np.array(self._fn(texts)).tolist()

    def embed_query(self, text: str) -> List[float]:
        return np.array(self._fn([text])[0]).tolist()
