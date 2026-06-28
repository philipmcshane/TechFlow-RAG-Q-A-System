"""Central configuration — edit here to tune the RAG pipeline without touching other files."""

from pathlib import Path

DOCS_DIR   = Path("./documents")
CHROMA_DIR = "./chroma_db"
CHUNK_SIZE    = 500
CHUNK_OVERLAP = 50
TOP_K         = 5   # chunks retrieved per query 
GROQ_MODEL = "llama-3.3-70b-versatile"
MAX_TOKENS = 1024
