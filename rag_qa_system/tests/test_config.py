"""Tests for config.py — verify all constants exist and have sensible values."""

from pathlib import Path
import config


def test_docs_dir_is_path():
    assert isinstance(config.DOCS_DIR, Path)


def test_chroma_dir_is_str():
    assert isinstance(config.CHROMA_DIR, str)
    assert len(config.CHROMA_DIR) > 0


def test_chunk_size_positive_int():
    assert isinstance(config.CHUNK_SIZE, int)
    assert config.CHUNK_SIZE > 0


def test_chunk_overlap_less_than_chunk_size():
    assert config.CHUNK_OVERLAP < config.CHUNK_SIZE


def test_chunk_overlap_non_negative():
    assert config.CHUNK_OVERLAP >= 0


def test_top_k_positive_int():
    assert isinstance(config.TOP_K, int)
    assert config.TOP_K > 0


def test_groq_model_non_empty_string():
    assert isinstance(config.GROQ_MODEL, str)
    assert len(config.GROQ_MODEL) > 0


def test_max_tokens_positive_int():
    assert isinstance(config.MAX_TOKENS, int)
    assert config.MAX_TOKENS > 0
