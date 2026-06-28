"""
Evaluation harness — 13 test questions with LLM-as-judge scoring.
Run: python evaluate.py
Requires: GROQ_API_KEY env var, and ChromaDB already ingested (python ingest.py).
"""

import os
import sys
import time
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from embeddings import OnnxEmbeddings
from config import CHROMA_DIR, TOP_K, GROQ_MODEL, MAX_TOKENS

# 10 happy-path Q&A pairs
TEST_CASES = [
    {
        "question": "What pricing plans does TechFlow offer?",
        "expected": "Three plans: Free ($0), Pro ($12/user/month), and Enterprise (custom pricing).",
    },
    {
        "question": "How many projects can I create on the Free plan?",
        "expected": "Up to 3 projects on the Free plan.",
    },
    {
        "question": "What payment methods does TechFlow accept?",
        "expected": "Credit cards (Visa, Mastercard, Amex, Discover), PayPal, and bank transfer for Enterprise.",
    },
    {
        "question": "How do I reset my password?",
        "expected": (
            "Click 'Forgot Password?' on the login page, enter your email, "
            "check for a reset link (expires in 24 hours), and set a new password."
        ),
    },
    {
        "question": "How do I invite team members to a project?",
        "expected": (
            "Open the project, go to Settings > Members, click 'Invite Members', "
            "enter email addresses, choose a permission level, and send the invitation."
        ),
    },
    {
        "question": "Does TechFlow integrate with Slack?",
        "expected": (
            "Yes, TechFlow has a native Slack integration for real-time notifications, "
            "creating tasks from Slack, and daily digests."
        ),
    },
    {
        "question": "Does TechFlow have a mobile app?",
        "expected": "Yes, available on iOS (App Store) and Android (Google Play).",
    },
    {
        "question": "What is the maximum file upload size in TechFlow?",
        "expected": "25 MB per file.",
    },
    {
        "question": "How can I export my TechFlow project data?",
        "expected": "Export in CSV, PDF, or JSON format from the project's More Options menu.",
    },
    {
        "question": "What is TechFlow's uptime guarantee?",
        "expected": "99.9% uptime as per the SLA, equivalent to less than 8 hours 45 minutes of downtime per year.",
    },
    # 3 edge-case questions 
    {
        "question": "What is TechFlow's stock ticker symbol?",
        "expected": (
            "The system should acknowledge this is not in the FAQ and suggest "
            "contacting support. It must NOT fabricate a stock ticker."
        ),
    },
    {
        "question": "How do I bake a chocolate cake?",
        "expected": (
            "The system should recognise this as off-topic and politely decline, "
            "redirecting the user to TechFlow-related questions."
        ),
    },
    {
        "question": "How much does it cost?",
        "expected": (
            "Because no plan is specified, the system should explain all three pricing "
            "tiers: Free ($0), Pro ($12/user/month), and Enterprise (custom pricing)."
        ),
    },
]

SYSTEM_PROMPT = """You are a helpful customer support agent for TechFlow.
Use the FAQ context below to answer the customer's question accurately and concisely.
If the answer is not in the context, say so and suggest contacting support@techflow.io.
Do not answer questions unrelated to TechFlow.

Context:
{context}"""

JUDGE_PROMPT = """You are evaluating a customer support Q&A system.

Question: {question}
Expected behaviour: {expected}
System's answer: {answer}

Score the answer:
- CORRECT: Correctly handles the question -- contains the key facts for FAQ questions,
  OR gracefully declines/redirects for out-of-scope or unanswerable questions
- PARTIAL: Has some but not all key information, or only partially handles edge cases
- INCORRECT: Wrong, misleading, fabricates information, or completely misses the point

Respond with exactly one word on the first line: CORRECT, PARTIAL, or INCORRECT
Then a brief reason on the second line."""


def build_rag_chain():
    embeddings = OnnxEmbeddings()
    db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    llm = ChatGroq(model=GROQ_MODEL, max_tokens=MAX_TOKENS)
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
    ])
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(db.as_retriever(search_kwargs={"k": TOP_K}), combine_docs_chain)


def judge_answer(judge_llm, question: str, expected: str, answer: str) -> tuple:
    prompt = JUDGE_PROMPT.format(question=question, expected=expected, answer=answer)
    response = judge_llm.invoke(prompt)
    lines = response.content.strip().split("\n", 1)
    verdict = lines[0].strip().upper()
    reason = lines[1].strip() if len(lines) > 1 else ""
    if verdict not in ("CORRECT", "PARTIAL", "INCORRECT"):
        verdict = "INCORRECT"
    return verdict, reason


def run_evaluation():
    if not os.getenv("GROQ_API_KEY"):
        print("ERROR: GROQ_API_KEY not set. Run:  $env:GROQ_API_KEY = 'gsk_...'")
        sys.exit(1)

    if not os.path.exists(CHROMA_DIR):
        print("ERROR: ChromaDB not found. Run 'python ingest.py' first.")
        sys.exit(1)

    total = len(TEST_CASES)
    print("=" * 60)
    print(f"TechFlow RAG System -- Evaluation ({total} questions)")
    print("=" * 60)
    print()

    rag_chain = build_rag_chain()
    judge_llm = ChatGroq(model=GROQ_MODEL, max_tokens=150)

    scores = {"CORRECT": 0, "PARTIAL": 0, "INCORRECT": 0}
    results = []

    for i, tc in enumerate(TEST_CASES, 1):
        tag = "edge" if i > 10 else f"{i:02d}"
        print(f"[{tag}/{total}] {tc['question']}")
        result = rag_chain.invoke({"input": tc["question"]})
        answer = result["answer"]

        verdict, reason = judge_answer(judge_llm, tc["question"], tc["expected"], answer)
        scores[verdict] += 1
        results.append({**tc, "answer": answer, "verdict": verdict, "reason": reason})

        icon = {"CORRECT": "[OK]", "PARTIAL": "[~] ", "INCORRECT": "[X] "}[verdict]
        print(f"       {icon} {verdict} -- {reason}")
        print(f"       Answer: {answer[:120].strip()}{'...' if len(answer) > 120 else ''}")
        print()

        if i < total:
            time.sleep(0.5)

    # Summary 
    accuracy = (scores["CORRECT"] + 0.5 * scores["PARTIAL"]) / total * 100

    print("=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"  Correct:   {scores['CORRECT']}/{total}")
    print(f"  Partial:   {scores['PARTIAL']}/{total}")
    print(f"  Incorrect: {scores['INCORRECT']}/{total}")
    print(f"  Accuracy:  {accuracy:.1f}%  (partial = 0.5)")
    print("=" * 60)

    report_path = "evaluation_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("TechFlow RAG Evaluation Report\n")
        f.write("=" * 60 + "\n\n")
        for i, r in enumerate(results, 1):
            f.write(f"Q{i:02d}: {r['question']}\n")
            f.write(f"Expected: {r['expected']}\n")
            f.write(f"Answer:   {r['answer']}\n")
            f.write(f"Verdict:  {r['verdict']} -- {r['reason']}\n\n")
        f.write(f"Accuracy: {accuracy:.1f}%\n")
        f.write(f"Correct: {scores['CORRECT']} | Partial: {scores['PARTIAL']} | Incorrect: {scores['INCORRECT']}\n")

    print(f"\nFull report saved to {report_path}")


if __name__ == "__main__":
    run_evaluation()
