import os
import fitz  # PyMuPDF
import numpy as np
import faiss
import tiktoken
from .llm_interface import generate_answer
from fastapi import UploadFile
from sentence_transformers import SentenceTransformer
from transformers import GPT2Tokenizer

embedder = SentenceTransformer('all-MiniLM-L6-v2')
INDEX_DIM = embedder.get_sentence_embedding_dimension()
index = faiss.IndexIDMap(faiss.IndexFlatIP(INDEX_DIM))
documents = []  # list of text chunks stored

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

async def process_pdf(file: UploadFile):
    # RESET for each new document
    index.reset()
    documents.clear()

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

def chunk_text(text, max_tokens=500):
    tokens = tokenizer.encode(text)
    chunks = []
    stride = 50
    for i in range(0, len(tokens), max_tokens - stride):
        chunk_tokens = tokens[i : i + max_tokens]
        chunks.append(tokenizer.decode(chunk_tokens))
    return chunks

def embed_text(texts):
    embeddings = embedder.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return embeddings.astype("float32")

def add_to_index(chunks):
    embeddings = embed_text(chunks)
    ids = np.arange(len(documents), len(documents) + len(chunks))
    index.add_with_ids(embeddings, ids)
    documents.extend(chunks)

async def query_pdf(query: str):
    top_k = 5
    query_embedding = embed_text([query])
    distances, indices = index.search(query_embedding, top_k)
    context_chunks = [documents[i] for i in indices[0] if i != -1]
    answer = generate_answer(query, context_chunks)
    return {"answer": answer}
