import os
import fitz  # PyMuPDF
import numpy as np
import faiss
import tiktoken
from .llm_interface import generate_answer
from fastapi import UploadFile

INDEX_DIM = 1536  # embedding dimension for text-embedding-ada-002
index = faiss.IndexFlatL2(INDEX_DIM)
documents = []  # list of text chunks stored

tokenizer = tiktoken.get_encoding("cl100k_base")

async def process_pdf(file: UploadFile):
    upload_dir = os.path.join(os.getcwd(), "data", "documents")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text)
    add_to_index(chunks)
    return {"message": f"Processed {file.filename}, indexed {len(chunks)} chunks."}

def extract_text_from_pdf(path: str) -> str:
    doc = fitz.open(path)
    return "\n".join(page.get_text() for page in doc)

def chunk_text(text: str, max_tokens=500):
    tokens = tokenizer.encode(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i : i + max_tokens]
        chunks.append(tokenizer.decode(chunk_tokens))
    return chunks

def embed_text(texts):
    # Call your embedding provider, e.g. OpenAI or local embeddings
    # Placeholder: random vectors for now
    return np.random.rand(len(texts), INDEX_DIM).astype("float32")

def add_to_index(chunks):
    embeddings = embed_text(chunks)
    index.add(embeddings)
    documents.extend(chunks)

async def query_pdf(query: str):
    top_k = 5
    query_embedding = embed_text([query])
    distances, indices = index.search(query_embedding, top_k)
    context_chunks = [documents[i] for i in indices[0] if i != -1]
    answer = generate_answer(query, context_chunks)
    return {"answer": answer}
