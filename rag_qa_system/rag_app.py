"""TechFlow FAQ RAG assistant — Streamlit UI (compatible with Streamlit 1.12)."""

import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_core.messages import SystemMessage, HumanMessage
from embeddings import OnnxEmbeddings
from config import CHROMA_DIR, TOP_K, GROQ_MODEL, MAX_TOKENS

SYSTEM_PROMPT = """You are a helpful customer support agent for TechFlow, \
a cloud-based project management platform.

Use the FAQ context below to answer the customer's question accurately and \
concisely. Cite specific details (prices, limits, steps) when present in the context.

If the answer is not covered by the context, say:
"I don't have that information in our FAQ. Please reach out to \
support@techflow.io and our team will help."

Context:
{context}"""


@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def load_retriever():
    embeddings = OnnxEmbeddings()
    db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    return db.as_retriever(search_kwargs={"k": TOP_K})


@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def load_llm():
    return ChatGroq(model=GROQ_MODEL, max_tokens=MAX_TOKENS)


# Page config 
st.set_page_config(page_title="TechFlow FAQ Assistant", page_icon="🤖")

with st.sidebar:
    st.title("TechFlow FAQ Assistant")
    st.markdown(
        f"""
**Stack**
- 🦜 LangChain retrieval chain
- 🗄️ ChromaDB vector store
- ⚡ ONNX `all-MiniLM-L6-v2` embeddings
- ⚡ Groq `{GROQ_MODEL}` generation
- 🎈 Streamlit UI

**How it works**

1. Your question is embedded and matched against FAQ chunks in ChromaDB
2. The top {TOP_K} most relevant sections are retrieved
3. The LLM streams a grounded answer from those sections

---
Run `python evaluate.py` in a terminal to score 13 test questions.
        """
    )

# Guards: API key and DB must exist
if not os.getenv("GROQ_API_KEY"):
    st.error(
        "**GROQ_API_KEY not set.**\n\n"
        "Set it before launching:\n"
        "```\n$env:GROQ_API_KEY = 'gsk_...'\n```\n"
        "Then refresh this page."
    )
    st.stop()

if not os.path.exists(CHROMA_DIR):
    st.error(
        "**ChromaDB not found.**  \n"
        "Run `python ingest.py` in your terminal first, then refresh this page."
    )
    st.stop()

retriever = load_retriever()
llm = load_llm()

#  Main UI 
st.title("🤖 TechFlow FAQ Assistant")
st.caption("Powered by RAG — answers are grounded in the official FAQ document.")

if "history" not in st.session_state:
    st.session_state.history = []

# Display conversation history
for entry in st.session_state.history:
    with st.container():
        st.markdown(f"**You:** {entry['question']}")
        st.markdown(f"**Assistant:** {entry['answer']}")
        if entry.get("sources"):
            with st.expander(f"📚 {len(entry['sources'])} FAQ sections retrieved"):
                for j, src in enumerate(entry["sources"], 1):
                    section = src.get("section", f"Excerpt {j}")
                    text = src.get("text", "")
                    st.markdown(f"**{section}**")
                    st.markdown(f"> {text[:350]}{'...' if len(text) > 350 else ''}")
        st.markdown("---")

# Input form
with st.form(key="qa_form", clear_on_submit=True):
    question = st.text_input(
        "Ask a question about TechFlow:",
        placeholder="e.g. How many projects can I have on the Free plan?",
    )
    submitted = st.form_submit_button("Ask ➔")

if submitted and question.strip():
    q = question.strip()

    # Retrieve relevant chunks
    try:
        context_docs = retriever.invoke(q)
    except Exception as e:
        st.error(f"Retrieval failed: {e}")
        st.stop()

    context_text = "\n\n".join(doc.page_content for doc in context_docs)
    messages = [
        SystemMessage(content=SYSTEM_PROMPT.format(context=context_text)),
        HumanMessage(content=q),
    ]

    # Stream the answer into a placeholder
    st.markdown(f"**You:** {q}")
    st.markdown("**Assistant:**")
    answer_placeholder = st.empty()
    full_answer = ""

    try:
        for chunk in llm.stream(messages):
            full_answer += chunk.content
            answer_placeholder.markdown(full_answer + "|")
        answer_placeholder.markdown(full_answer)
    except Exception as e:
        answer_placeholder.error(f"Generation failed: {e}")
        st.stop()

    sources = [
        {
            "section": doc.metadata.get("section", "FAQ"),
            "text": doc.page_content.strip(),
        }
        for doc in context_docs
    ]

    st.session_state.history.append({
        "question": q,
        "answer": full_answer,
        "sources": sources,
    })
    st.experimental_rerun()
