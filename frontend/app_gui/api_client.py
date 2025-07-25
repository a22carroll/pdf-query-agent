import requests

API_BASE_URL = "http://localhost:8000"

def upload_pdf(file_path):
    try:
        with open(file_path, "rb") as f:
            response = requests.post(f"{API_BASE_URL}/upload", files={"pdf_file": f})
        return response.status_code == 200
    except Exception as e:
        print("Upload failed:", e)
        return False

def ask_question(question):
    try:
        response = requests.post(f"{API_BASE_URL}/query", json={"question": question})
        if response.status_code == 200:
            return response.json().get("answer", "No answer received.")
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Failed to query: {e}"
