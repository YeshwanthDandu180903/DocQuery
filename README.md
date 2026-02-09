# 📚 DocuQuery

> An intelligent document question-answering system powered by RAG (Retrieval-Augmented Generation)

**DocuQuery** lets you ask questions and get accurate answers directly from your documents—no hallucinations, just facts.

This demo uses HR documents (policies, SOPs, FAQs) from a fictional company to showcase how RAG can be applied to any document collection.

---

## ✨ Features

- 🔍 **Hybrid Search** - Combines semantic (FAISS) and keyword (BM25) retrieval
- 📄 **Multi-Format Support** - Works with PDFs and Markdown files
- 🎯 **Source Citations** - Every answer links back to source documents
- 🚫 **No Hallucinations** - Answers only from your documents
- 💬 **Interactive UI** - Clean Gradio interface for easy querying

---

## 📂 Project Structure

``
docuquery/
│
├── data/
│   ├── pdfs/              # PDF documents (policies, SOPs)
│   └── markdown/          # Markdown files (FAQs)
│
├── storage/               # Generated indexes (FAISS + BM25)
│
├── build_index.py         # Index builder
├── query_engine.py        # RAG query engine
├── gradio_app.py          # Web UI
├── requirements.txt       # Python dependencies
└── README.md
```



## 🚀 Quick Start

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/docuquery.git
cd docuquery
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Build the index
```bash
python build_index.py
```

### 4️⃣ Launch the chatbot
```bash
python gradio_app.py
```

Open your browser at `http://localhost:7860` and start asking questions!

---

## 💡 Example Queries

Try asking:

- *"How many leaves can I carry forward?"*
- *"What's the process for applying for sick leave?"*
- *"Can I work from home?"*
- *"What is the notice period for resignation?"*

---

## 🛠️ Tech Stack

- **LlamaIndex** - RAG orchestration
- **FAISS** - Vector similarity search
- **BM25** - Keyword-based retrieval
- **Gradio** - Interactive web UI
- **OpenAI/HuggingFace** - Embeddings and LLM

---

## 📋 How It Works

1. **Document Loading** - Reads PDFs and Markdown files
2. **Chunking** - Splits documents into searchable segments
3. **Indexing** - Creates vector (FAISS) and keyword (BM25) indexes
4. **Query** - User asks a question
5. **Retrieval** - Finds most relevant document chunks
6. **Generation** - LLM generates answer using retrieved context
7. **Citation** - Shows source documents for transparency

---

## 🎯 Use Cases

This architecture works for:

- ✅ HR Policy Chatbots
- ✅ Technical Documentation Q&A
- ✅ Legal Document Search
- ✅ Customer Support Knowledge Bases
- ✅ Internal Wiki Search
- ✅ Research Paper Q&A

---

## 📝 Document Hierarchy

In this demo, documents follow a priority system:

1. **Policy** (Highest Authority) - Company rules and regulations
2. **SOP** (Procedures) - Step-by-step processes
3. **FAQ** (Clarifications) - Common questions and answers

---

## ⚠️ Disclaimer

This project uses **fictional company documents** for demonstration purposes only. It's designed as a learning resource and portfolio project.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Add new document formats
- Improve retrieval accuracy
- Enhance the UI
- Add evaluation metrics

---

## 📄 License

MIT License - feel free to use this for learning and building your own projects.

---

## ⭐ Show Your Support

If you found this helpful, please star the repo and share it with others learning about RAG!

---

**Built with ❤️ to demonstrate practical RAG implementation**
```

---
