
import os
from PyPDF2 import PdfReader

def load_pdfs(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            reader = PdfReader(os.path.join(folder_path, filename))
            text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
            documents.append({"filename": filename, "text": text})
    return documents
