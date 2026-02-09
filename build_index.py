"""
Build indexes for Abhimanyu Industries HR Agent.

- Reads from data/markdown/ (faq.md) AND data/pdfs/ (Policy, SOP)
- Chunks and embeds with sentence-transformers
- Stores vectors in FAISS (LangChain VectorStore) under storage/
- Builds and persists a simple BM25 keyword corpus for hybrid retrieval

Run:
    python build_index.py
"""
from __future__ import annotations

import os
import re
import json
from pathlib import Path
from typing import List, Tuple, Dict

from PyPDF2 import PdfReader

# LangChain components
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Keyword/BM25
from rank_bm25 import BM25Okapi

PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
MARKDOWN_DIR = DATA_DIR / "markdown"
PDF_DIR = DATA_DIR / "pdfs"

STORAGE_DIR = PROJECT_ROOT / "storage"
VSTORE_DIR = STORAGE_DIR / "faiss_lc"
BM25_PATH = STORAGE_DIR / "bm25_corpus.txt"
CORPUS_JSONL = STORAGE_DIR / "corpus.jsonl"

EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def clean_text(text: str) -> str:
    """Clean text by removing extra whitespace and fixing common PDF extraction issues."""
    # Fix hyphenated words at end of lines (e.g. "communi-\ncation" -> "communication")
    text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
    # Replace multiple newlines with a placeholder to preserve paragraphs
    text = re.sub(r'\n{2,}', ' PARAGRAPH_BREAK ', text)
    # Replace single newlines with space (treating them as line wrapping)
    text = text.replace('\n', ' ')
    # Restore paragraphs
    text = text.replace(' PARAGRAPH_BREAK ', '\n\n')
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def get_doc_type(filename: str) -> str:
    """Infer document type from filename."""
    fname = filename.lower()
    if "policy" in fname:
        return "policy"
    elif "sop" in fname or "handbook" in fname or "process" in fname:
        return "sop"
    elif "faq" in fname or "question" in fname:
        return "faq"
    return "unknown"


def load_markdown_files(md_dir: Path) -> List[Tuple[str, str, str]]:
    """Return list of (source, text, doc_type) from Markdown files."""
    out: List[Tuple[str, str, str]] = []
    if not md_dir.exists():
        return out
        
    for p in sorted(md_dir.glob("*.md")):
        try:
            doc_type = get_doc_type(p.name)
            text = p.read_text(encoding="utf-8")
            if text.strip():
                # Markdown often doesn't need heavy cleaning like PDFs, but consistency helps.
                # However, preserving structure like # Headers is important for Markdown splitting.
                # So we skip aggressive cleaning for MD.
                out.append((p.name, text, doc_type))
        except Exception as e:
            print(f"Error loading {p.name}: {e}")
            continue
    return out


def load_pdf_files(pdf_dir: Path) -> List[Tuple[str, str, str]]:
    """Return list of (source, text, doc_type) from PDF files."""
    out: List[Tuple[str, str, str]] = []
    if not pdf_dir.exists():
        return out
        
    for p in sorted(pdf_dir.glob("*.pdf")):
        try:
            doc_type = get_doc_type(p.name)
            reader = PdfReader(str(p))
            full_text = []
            for page in reader.pages:
                txt = page.extract_text() or ""
                full_text.append(txt)
            
            raw_text = "\n".join(full_text)
            cleaned = clean_text(raw_text)
            
            if cleaned.strip():
                out.append((p.name, cleaned, doc_type))
        except Exception as e:
            print(f"Error loading {p.name}: {e}")
            continue
    return out


def chunk_documents(raw_docs: List[Tuple[str, str, str]]) -> List[Document]:
    """Chunk raw (source, text, doc_type) into LangChain Documents with metadata."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,  # Strict chunking
        chunk_overlap=100,
        separators=["\n\n", "##", "\n", ". ", ".", " "]
    )
    docs: List[Document] = []
    for source, text, doc_type in raw_docs:
        for chunk in splitter.split_text(text):
            if chunk.strip():
                docs.append(Document(
                    page_content=chunk.strip(), 
                    metadata={
                        "source": source,
                        "doc_type": doc_type
                    }
                ))
    return docs


def build_faiss_vectorstore(chunks: List[Document]) -> FAISS:
    """Build and persist a FAISS vector store using sentence-transformers embeddings."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
    vstore = FAISS.from_documents(chunks, embedding=embeddings)
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    VSTORE_DIR.mkdir(parents=True, exist_ok=True)
    vstore.save_local(str(VSTORE_DIR))
    return vstore


def persist_corpus_jsonl(chunks: List[Document]) -> None:
    """Save chunk texts + metadata for BM25 and citations."""
    with open(CORPUS_JSONL, "w", encoding="utf-8") as f:
        for d in chunks:
            rec: Dict[str, str] = {
                "text": d.page_content,
                "source": d.metadata.get("source", "unknown"),
                "doc_type": d.metadata.get("doc_type", "unknown")
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def build_bm25_corpus(chunks: List[Document]) -> BM25Okapi:
    corpus_texts = [d.page_content for d in chunks]
    tokenized = [t.lower().split() for t in corpus_texts]
    bm25 = BM25Okapi(tokenized)
    # Save raw corpus for quick reload
    BM25_PATH.write_text("\n\n".join(corpus_texts), encoding="utf-8")
    return bm25


def main():
    print("Loading Abhimanyu Industries documents (PDFs & Markdown)...")
    
    all_docs: List[Tuple[str, str, str]] = []
    
    # Load Markdown
    md_docs = load_markdown_files(MARKDOWN_DIR)
    print(f"Loaded {len(md_docs)} Markdown files.")
    all_docs.extend(md_docs)
    
    # Load PDFs
    pdf_docs = load_pdf_files(PDF_DIR)
    print(f"Loaded {len(pdf_docs)} PDF files.")
    all_docs.extend(pdf_docs)

    if not all_docs:
        print("No documents found in data/markdown/ or data/pdfs/. Check your data folder.")
        return

    print(f"Total documents: {[d[0] for d in all_docs]}")

    print("Chunking documents...")
    chunks = chunk_documents(all_docs)
    print(f"Created {len(chunks)} chunks.")

    print("Building FAISS index (LangChain) with sentence-transformers embeddings...")
    _ = build_faiss_vectorstore(chunks)
    print(f"FAISS vector store saved to: {VSTORE_DIR}")

    print("Persisting corpus metadata for citations...")
    persist_corpus_jsonl(chunks)

    print("Building BM25 keyword index...")
    _ = build_bm25_corpus(chunks)
    print(f"BM25 corpus saved to: {BM25_PATH}")

    print("Done. Indexes are ready in 'storage/'.")


if __name__ == "__main__":
    main()
