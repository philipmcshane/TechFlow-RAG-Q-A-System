"""Tests for embeddings.py — OnnxEmbeddings output type, shape, and consistency.

These tests use the local ONNX model (all-MiniLM-L6-v2) and make no API calls.
The model is downloaded once to ~/.cache on first run (~80 MB).
"""

import pytest
from embeddings import OnnxEmbeddings

EXPECTED_DIM = 384  # all-MiniLM-L6-v2 output dimension


@pytest.fixture(scope="module")
def emb():
    return OnnxEmbeddings()


def test_embed_query_returns_list(emb):
    result = emb.embed_query("What is TechFlow?")
    assert isinstance(result, list)


def test_embed_query_elements_are_python_floats(emb):
    result = emb.embed_query("test query")
    assert all(type(v) is float for v in result), (
        "Expected native Python floats, not numpy.float32 — "
        "ChromaDB 1.x rejects numpy scalar types"
    )


def test_embed_query_correct_dimension(emb):
    result = emb.embed_query("dimension check")
    assert len(result) == EXPECTED_DIM


def test_embed_documents_returns_list_of_lists(emb):
    result = emb.embed_documents(["Hello", "World"])
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(row, list) for row in result)


def test_embed_documents_count_matches_input(emb):
    texts = ["one", "two", "three"]
    result = emb.embed_documents(texts)
    assert len(result) == len(texts)


def test_embed_documents_consistent_dimension(emb):
    result = emb.embed_documents(["foo", "bar", "baz"])
    dims = {len(row) for row in result}
    assert dims == {EXPECTED_DIM}, f"Expected all rows to be {EXPECTED_DIM}-d, got {dims}"


def test_embed_documents_elements_are_python_floats(emb):
    result = emb.embed_documents(["float type check"])
    assert all(type(v) is float for v in result[0])


def test_query_and_document_same_dimension(emb):
    q = emb.embed_query("consistency check")
    docs = emb.embed_documents(["consistency check"])
    assert len(q) == len(docs[0])
