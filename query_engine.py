from __future__ import annotations
import json, os
from pathlib import Path
from typing import List, Tuple

from rank_bm25 import BM25Okapi
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

ROOT = Path(__file__).parent
VSTORE_DIR = ROOT / "storage/faiss_lc"
BM25_PATH = ROOT / "storage/bm25_corpus.txt"
CORPUS_JSONL = ROOT / "storage/corpus.jsonl"

SYSTEM_PROMPT = """
You are an Internal HR Knowledge Agent for Abhimanyu Industries.

Answer ONLY using the retrieved context.
If information is missing, say:
"This information is not defined in the current Abhimanyu Industries documentation."
"""

class HRQueryEngine:

    def __init__(self):
        self.top_k = 3
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
        self.vstore = FAISS.load_local(str(VSTORE_DIR), self.embeddings, allow_dangerous_deserialization=True)
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
            ("system", SYSTEM_PROMPT.strip()),
            (
                "human",
                "Question: {question}\n\nContext:\n{context}\n\nAnswer:"
            ),
        ])
        return prompt | llm | StrOutputParser()

    def classify_intent(self, q: str) -> str:
        q = q.lower()
        if any(k in q for k in ["sustain", "climate", "environment", "report", "growth", "finance", "financial", "revenue", "profit", "loss", "fiscal", "year", "quarter"]):
            return "financial"
        if any(k in q for k in ["how", "process", "apply"]):
            return "sop"
        if any(k in q for k in ["who", "what if", "when"]):
            return "faq"
        return "policy"

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

        results = list(combined.items())[:self.top_k]
        return results

    def answer_question(self, question: str) -> Tuple[str, List[str]]:
        intent = self.classify_intent(question)
        retrieved = self.retrieve(question, intent)

        if not retrieved:
            return "I'm unable to answer this based on the current Abhimanyu Industries documentation.", []

        context = "\n\n".join(t for t, _ in retrieved)
        sources = list({src for _, src in retrieved})

        answer = self.llm.invoke({
            "question": question,
            "context": context
        })

        return answer, sources
