"""
Ingest TechFlow FAQ documents into ChromaDB.
Run this once before starting the app: python ingest.py
Re-index after document changes:        python ingest.py --reset
"""

import re
import shutil
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document
from embeddings import OnnxEmbeddings
from config import DOCS_DIR, CHROMA_DIR, CHUNK_SIZE, CHUNK_OVERLAP


def _section_documents(doc: Document) -> list[Document]:
    """Split a raw document into per-section Documents, each tagged with section metadata."""
    sections: list[Document] = []
    current_section = "Overview"
    current_lines: list[str] = []

    for line in doc.page_content.split("\n"):
        match = re.match(r"^##\s+(.+)$", line)
        if match:
            if current_lines:
                sections.append(Document(
                    page_content="\n".join(current_lines).strip(),
                    metadata={**doc.metadata, "section": current_section},
                ))
            current_section = match.group(1).strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        sections.append(Document(
            page_content="\n".join(current_lines).strip(),
            metadata={**doc.metadata, "section": current_section},
        ))

    return [s for s in sections if s.page_content]


def ingest(reset: bool = False):
    if reset and DOCS_DIR.parent.joinpath(CHROMA_DIR).exists():
        shutil.rmtree(CHROMA_DIR)
        print(f"Removed existing ChromaDB at {CHROMA_DIR}/")

    print("Loading documents...")
    raw_docs: list[Document] = []
    for ext in ("*.md", "*.txt"):
        for path in DOCS_DIR.glob(ext):
            loader = TextLoader(str(path), encoding="utf-8")
            raw_docs.extend(loader.load())

    if not raw_docs:
        raise FileNotFoundError(f"No .md or .txt files found in {DOCS_DIR}/")

    print(f"  Loaded {len(raw_docs)} document(s)")

    # Split into per-section documents first so each chunk carries a section label
    section_docs: list[Document] = []
    for doc in raw_docs:
        section_docs.extend(_section_documents(doc))
    print(f"  Identified {len(section_docs)} sections")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(section_docs)
    print(f"  Split into {len(chunks)} chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")

    print("Loading ONNX embedding model (downloads ~80 MB on first run)...")
    embeddings = OnnxEmbeddings()

    print("Storing in ChromaDB...")
    Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_DIR)
    print(f"  Stored {len(chunks)} chunks in {CHROMA_DIR}/")
    print("\nDone! Run:  streamlit run rag_app.py")


if __name__ == "__main__":
    import sys
    ingest(reset="--reset" in sys.argv)
