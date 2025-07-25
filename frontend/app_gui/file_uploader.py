import os
import requests

def upload_pdf(filepath, server_url="http://localhost:8000"):
    with open(filepath, "rb") as f:
        files = {'file': (os.path.basename(filepath), f, 'application/pdf')}
        response = requests.post(f"{server_url}/upload", files=files)
    return response.json()
