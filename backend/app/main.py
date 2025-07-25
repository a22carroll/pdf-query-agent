from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from .rag_engine import process_pdf, query_pdf
import os
from fastapi.responses import FileResponse
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
    print("got file")
    return await process_pdf(file)

@app.post("/query")
async def query_document(query: str = Form(...)):
    return await query_pdf(query)

# Go up from app/ to backend/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_DIR = os.path.join(BASE_DIR, "data", "documents")

@app.get("/pdfs")
def list_pdfs():
    try:
        files = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]
        return {"files": files}
    except Exception as e:
        return {"error": str(e)}

@app.get("/pdfs/{filename}")
def get_pdf(filename: str):
    file_path = os.path.join(PDF_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/pdf', filename=filename)
    return {"error": "File not found"}

@app.delete("/pdfs/{filename}")
def delete_pdf(filename: str):
    file_path = os.path.join(PDF_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": f"{filename} deleted"}
    return {"error": "File not found"}