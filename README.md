# TechFlow FAQ RAG Q&A System

A retrieval-augmented generation (RAG) Q&A system built over a customer FAQ document. Ask natural-language questions and get grounded, streamed answers retrieved from the source document — no hallucination of facts that aren't there.

**Evaluation result: 13 test questions** (10 happy-path + 3 edge cases), scored by an LLM-as-judge.

---

## How it works

```
User question
     |
     v
ONNX Embeddings          <- all-MiniLM-L6-v2 via ChromaDB (no PyTorch needed)
     |
     v
ChromaDB vector search   <- top-5 most relevant FAQ chunks retrieved
     |
     v
Groq LLM (streaming)     <- llama-3.3-70b-versatile streams the answer
     |
     v
Grounded answer + section sources
```

1. **Ingest** — the FAQ document is split by section then into ~500-token chunks. Each chunk carries its section heading as metadata. Chunks are embedded with the ONNX `all-MiniLM-L6-v2` model and stored in a local ChromaDB vector database.
2. **Retrieve** — a user question is embedded the same way; the 5 most semantically similar chunks are retrieved.
3. **Generate** — those chunks are injected into a prompt and Groq's `llama-3.3-70b-versatile` streams the answer token-by-token for fast perceived response time.

---

## Project structure

```
rag_qa_system/
├── documents/
│   └── techflow_faq.md      # Source FAQ document (~2,000 words, 11 sections)
├── config.py                # All tuneable settings in one place
├── embeddings.py            # LangChain-compatible ONNX embedding wrapper
├── ingest.py                # One-time ingestion: doc -> sections -> chunks -> ChromaDB
├── rag_app.py               # Streamlit web UI (streaming responses)
├── evaluate.py              # 13-question accuracy harness (LLM-as-judge)
├── requirements.txt
└── chroma_db/               # Vector store (created by ingest.py)
```

---

## Stack

| Component | Library / Model |
|---|---|
| LLM | Groq `llama-3.3-70b-versatile` |
| Embeddings | `all-MiniLM-L6-v2` via ChromaDB ONNX runtime |
| Vector store | ChromaDB (local, persistent) |
| RAG chain | LangChain `create_retrieval_chain` |
| UI | Streamlit (streaming via `st.empty()`) |
| Evaluation | LLM-as-judge (same Groq model) |

---

## Setup

### Prerequisites

- Python 3.9+
- A [Groq API key](https://console.groq.com) (free tier available)

### Install

```bash
git clone <this-repo>
cd rag_qa_system
pip install -r requirements.txt
```

### Set your GROQ API key

```bash
# Linux / macOS
export GROQ_API_KEY="gsk_..."

# Windows PowerShell
$env:GROQ_API_KEY = "gsk_..."
```

The app will display a clear error message if the key is missing — no silent crash.

### Ingest the FAQ document

Only needs to be run once. Downloads the ONNX embedding model (~80 MB) on first run.

```bash
python ingest.py
```

Re-index after adding or editing documents:

```bash
python ingest.py --reset
```

---

## Configuration

All tuneable settings are in `config.py` — edit once and every script picks up the change:

```python
CHUNK_SIZE    = 500   # tokens per chunk
CHUNK_OVERLAP = 50    # overlap between consecutive chunks
TOP_K         = 5     # FAQ chunks retrieved per query
GROQ_MODEL    = "llama-3.3-70b-versatile"
MAX_TOKENS    = 1024
```

---

## Usage

### Streamlit app

```bash
streamlit run rag_app.py
```

Opens at `http://localhost:8501`. Type a question; the answer streams in token-by-token. Expand "FAQ sections retrieved" to see the exact source sections and their headings.

### Evaluation

Runs 13 pre-defined test questions through the full RAG pipeline and scores each answer.

```bash
python evaluate.py
```

Results are printed to the terminal and saved to `evaluation_report.txt`.

---

## Evaluation results

### 10 happy-path questions

| # | Question | Verdict |
|---|---|---|
| 1 | What pricing plans does TechFlow offer? | Correct (k=5) |
| 2 | How many projects on the Free plan? | Correct |
| 3 | What payment methods are accepted? | Correct |
| 4 | How do I reset my password? | Correct |
| 5 | How do I invite team members? | Correct |
| 6 | Does TechFlow integrate with Slack? | Correct |
| 7 | Does TechFlow have a mobile app? | Correct (k=5) |
| 8 | What is the maximum file upload size? | Correct |
| 9 | How can I export project data? | Correct |
| 10 | What is TechFlow's uptime guarantee? | Correct |

Q1 and Q7 were PARTIAL at k=3 (details in adjacent chunks not retrieved). Raising to k=5 fixes both.

### 3 edge-case questions

| # | Question | Expected behaviour |
|---|---|---|
| 11 | What is TechFlow's stock ticker symbol? | Graceful "not in FAQ" response |
| 12 | How do I bake a chocolate cake? | Polite off-topic redirect |
| 13 | How much does it cost? (ambiguous) | Lists all three pricing tiers |

---

## Extending the system

- **Add more documents**: drop additional `.md` or `.txt` files into `documents/` and re-run `python ingest.py --reset`.
- **Change the LLM**: update `GROQ_MODEL` in `config.py`, or swap `ChatGroq` for any LangChain-compatible LLM (OpenAI, Anthropic, Ollama, etc.).
- **Tune retrieval**: adjust `CHUNK_SIZE`, `CHUNK_OVERLAP`, and `TOP_K` in `config.py`.
- **Swap the embedding model**: update `embeddings.py` to use any model supported by ChromaDB or LangChain.

---

## License

MIT
