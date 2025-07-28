# pdf-query-agent
# 📄 PDF Query Agent

**PDF Query Agent** is a local document question-answering system that lets you upload a PDF, index its contents, and ask questions about it using natural language. The system uses a combination of PDF parsing, semantic text embeddings, FAISS vector search, and an LLM to generate grounded answers from the document content.

---

## Features

- Upload and process any PDF file
- Extracts and chunks text for efficient search
- Generates semantic embeddings using `SentenceTransformer`
- Stores and searches document chunks using FAISS
- Answers questions using context-aware prompting and an LLM (e.g. OpenAI, local model)

---

## Tech Stack

- **Backend**: FastAPI
- **Embeddings**: [SentenceTransformers](https://www.sbert.net/) (`all-MiniLM-L6-v2` or custom)
- **Vector Search**: FAISS (IndexFlatIP with optional ID tracking)
- **PDF Parsing**: PyMuPDF (`fitz`)
- **Tokenization**: `transformers` tokenizer (e.g. GPT-2)
- **LLM Answering**: Plug-in via `generate_answer(query, context_chunks)`


