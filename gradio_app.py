from __future__ import annotations
import json, os
from pathlib import Path
from typing import List, Tuple

import gradio as gr
from rank_bm25 import BM25Okapi

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# =========================================================
# PERSON CONTEXT (Knowledge of the Person)
# =========================================================
PERSON_PROFILE = {
    "name": "Yeshwanth Dandu",
    "role": "Fresher",
    "department": "Data Science",
    "location": "Hyderabad",
    "access_level": "Employee"
}

# =========================================================
# CONFIG
# =========================================================
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

ROOT = Path(__file__).parent
VSTORE_DIR = ROOT / "storage/faiss_lc"
CORPUS_JSONL = ROOT / "storage/corpus.jsonl"

SYSTEM_PROMPT = """
You are a Person-Aware Internal Knowledge Agent for Abhimanyu Industries.

User Context:
- Role: {role}
- Department: {department}
- Access Level: {access_level}

Rules:
- Answer ONLY using the retrieved context.
- If information is missing, say:
  "This information is not defined in the current Abhimanyu Industries documentation."
"""

# =========================================================
# RAG QUERY ENGINE
# =========================================================
class RAGQueryEngine:

    def __init__(self, person_context: dict):
        self.person = person_context
        self.top_k = 3

        self.embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
        self.vstore = FAISS.load_local(
            str(VSTORE_DIR),
            self.embeddings,
            allow_dangerous_deserialization=True
        )

        self.corpus = self._load_corpus()
        self.bm25 = BM25Okapi([c["text"].lower().split() for c in self.corpus])
        self.llm = self._build_llm()

    def _load_corpus(self):
        with open(CORPUS_JSONL, encoding="utf-8") as f:
            return [json.loads(l) for l in f]

    def _build_llm(self):
        llm = ChatGroq(
            model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
            temperature=0
        )

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                SYSTEM_PROMPT.format(
                    role=self.person["role"],
                    department=self.person["department"],
                    access_level=self.person["access_level"]
                )
            ),
            (
                "human",
                "Question: {question}\n\nContext:\n{context}\n\nAnswer:"
            ),
        ])

        return prompt | llm | StrOutputParser()

    # ---------------- Intent Routing ----------------
    def classify_intent(self, q: str) -> str:
        q = q.lower()
        if any(k in q for k in [
            "finance", "financial", "revenue", "profit", "loss",
            "cost", "expense", "margin", "fiscal", "year", "quarter"
        ]):
            return "financial"
        if any(k in q for k in ["how", "process", "apply"]):
            return "sop"
        if any(k in q for k in ["who", "when", "what if"]):
            return "faq"
        return "policy"

    # ---------------- Hybrid Retrieval ----------------
    def retrieve(self, q: str, intent: str):
        vec_docs = self.vstore.similarity_search(q, k=20)
        vec_docs = [d for d in vec_docs if d.metadata["doc_type"] == intent]

        scores = self.bm25.get_scores(q.lower().split())
        kw_docs = [
            (self.corpus[i], scores[i])
            for i in range(len(scores))
            if self.corpus[i]["doc_type"] == intent
        ]
        kw_docs.sort(key=lambda x: x[1], reverse=True)

        combined = {}
        for d in vec_docs:
            combined[d.page_content] = d.metadata["source"]
        for rec, _ in kw_docs:
            combined.setdefault(rec["text"], rec["source"])

        return list(combined.items())[:self.top_k]

    # ---------------- Answer ----------------
    def answer_question(self, question: str) -> Tuple[str, List[str]]:
        intent = self.classify_intent(question)
        retrieved = self.retrieve(question, intent)

        if not retrieved:
            return (
                "This information is not defined in the current Abhimanyu Industries documentation.",
                []
            )

        context = "\n\n".join(t for t, _ in retrieved)
        sources = list({src for _, src in retrieved})

        answer = self.llm.invoke({
            "question": question,
            "context": context
        })

        return answer, sources


# =========================================================
# GRADIO APP
# =========================================================
engine = None

def get_engine():
    global engine
    if engine is None:
        engine = RAGQueryEngine(PERSON_PROFILE)
    return engine

def respond(message, history):
    try:
        rag = get_engine()
        answer, sources = rag.answer_question(message)

        response = answer
        if sources:
            response += "\n\n---\n📚 Sources Used:\n"
            for s in sources:
                response += f"- {s}\n"

        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})
        return history, ""

    except Exception as e:
        history.append({"role": "assistant", "content": f"⚠️ Error: {e}"})
        return history, ""


custom_css = """
body, .gradio-container {
    background-color: #020617 !important;
    color: #e5e7eb !important;
    font-family: Inter, system-ui, sans-serif;
}
textarea, input {
    background-color: #020617 !important;
    color: #e5e7eb !important;
}
.message.user {
    background-color: #1e293b !important;
}
.message.bot {
    background-color: #020617 !important;
}
"""

with gr.Blocks(css=custom_css) as demo:

    gr.Markdown("""
    # 🏢 Abhimanyu Industries – Intelligent RAG Assistant
    """)

    chatbot = gr.Chatbot(height=420)

    with gr.Row():
        msg = gr.Textbox(placeholder="Ask HR or Financial questions...", scale=4)
        send = gr.Button("Send", scale=1)

    send.click(respond, [msg, chatbot], [chatbot, msg])
    msg.submit(respond, [msg, chatbot], [chatbot, msg])

    gr.Markdown(
        "⚠️ Responses are generated strictly from internal documents using role-aware RAG."
    )

# =========================================================
# LAUNCH
# =========================================================
if __name__ == "__main__":
    print("🚀 Launching Person-Aware RAG Chatbot...")
    demo.launch(share=True)
