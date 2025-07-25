from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from .rag_engine import process_pdf, query_pdf

app = FastAPI()

# Allow requests from frontend (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    return await process_pdf(file)

@app.post("/query")
async def query_document(query: str = Form(...)):
    return await query_pdf(query)
