# 📚 DocuQuery

> An intelligent document question-answering system powered by **RAG (Retrieval-Augmented Generation)**

**DocuQuery** enables users to ask natural-language questions and receive **accurate, source-grounded answers** directly from internal documents — **no hallucinations, only facts**.

This project demonstrates a **scalable RAG architecture** that was:
- First validated using **employee-facing HR documents** (policies, SOPs, FAQs)
- Then extended to **financial analytics documents**, including a realistic **Company Financial Analysis Report**

The same architecture supports both **operational knowledge** and **financial & business insight extraction**, mirroring real enterprise AI workflows.

---

## ✨ Features

- 🔍 **Hybrid Search** – Combines semantic (FAISS) and keyword (BM25) retrieval  
- 📄 **Multi-Format Support** – Works with PDFs and Markdown files  
- 🎯 **Source Citations** – Every answer is backed by source documents  
- 🚫 **Hallucination Control** – Responses are strictly document-grounded  
- 💬 **Interactive UI** – Clean Gradio interface for easy querying  

---

## 🏦 Financial Analytics Context

In addition to HR documents, DocuQuery processes **financial analysis reports** prepared in an analyst-style format, covering:

- Historical **sales and revenue trends**
- **Cost of Goods Sold (COGS)** and operating expenses
- **Gross profit, net profit, and margin analysis**
- Business drivers and performance insights
- Market and economic context
- Analyst conclusions supporting forecasting and investment decisions

This reflects real-world usage in **financial analytics, strategy, and decision-support teams**.

---

## 📁 Project Structure

The project follows a clean and modular structure to clearly separate  
**data, indexing logic, retrieval engine, and user interface**.

```text
docuquery/
│
├── data/
│   ├── pdfs/
│   │   ├── hr_documents/          # HR Policies & SOP documents
│   │   └── financial_reports/     # Financial analysis & performance PDFs
│   │
│   └── markdown/                 # FAQ documents (Markdown)
│
├── storage/                      # Generated indexes (FAISS + BM25)
│
├── build_index.py                # Builds vector & keyword indexes
├── query_engine.py               # Hybrid RAG query engine (FAISS + BM25 + LLM)
├── gradio_app.py                 # Interactive Web UI (Gradio)
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation



---

## 🚀 Quick Start

### 1️⃣ Clone the repository
```bash
git clone https://github.com/YeshwanthDandu180903/docuquery.git
cd docuquery

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Build the index
python build_index.py

4️⃣ Launch the chatbot
python gradio_app.py


Open your browser at http://localhost:7860 and start asking questions.

💡 Example Queries
HR & Operational Queries

"How many leaves can I carry forward?"

"What is the notice period for resignation?"

"What is the WFH approval process?"

Financial Analytics Queries

"Summarize the company’s financial performance from FY 2021 to FY 2025."

"How did sales growth impact net profit margins?"

"What were the major cost drivers affecting profitability?"

"Identify key financial risks mentioned in the report."

"What insights support future forecasting and investment decisions?"

🛠️ Tech Stack

LlamaIndex – RAG orchestration

FAISS – Vector similarity search

BM25 – Keyword-based retrieval

Gradio – Interactive web UI

OpenAI / HuggingFace / Groq – Embeddings and LLMs

📋 How It Works

Document loading from PDFs and Markdown files

Text chunking for efficient retrieval

Hybrid indexing using FAISS and BM25

Natural-language user query

Retrieval of relevant document chunks

Grounded response generation via LLM

Source citation for transparency

🎯 Use Cases

✅ HR Policy & Employee Knowledge Chatbots

✅ Financial Report & Performance Analysis

✅ Cost, Expense & Profitability Insights

✅ Business & Investment Decision Support

✅ Risk & Compliance Document Review

✅ Internal Knowledge & Analytics Systems

📝 Document Hierarchy

Policy – Highest authority (rules & regulations)

SOP – Procedural guidance

FAQ – Clarifications and common questions

Financial Analysis Reports – Analyst-style business insights

⚠️ Disclaimer

All documents are fictional and created solely for demonstration and learning purposes.
This project showcases document intelligence and financial analytics workflows, not real company data.

🤝 Contributing

Contributions are welcome:

Add new document formats

Improve retrieval accuracy

Extend financial analytics coverage

Add evaluation metrics

📄 License

MIT License – free to use for learning and portfolio projects.

⭐ Show Your Support

If you found this project helpful, please ⭐ the repository and share it with others learning about RAG and financial analytics.

Built with ❤️ to demonstrate scalable RAG systems for operational and financial intelligence
