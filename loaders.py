import os
from langchain_community.document_loaders import PDFPlumberLoader, TextLoader

def get_document_files(folder):
    try:
        return [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith((".pdf", ".txt"))]
    except Exception as e:
        return []

def load_documents(file_path):
    try:
        if file_path.endswith(".pdf"):
            return PDFPlumberLoader(file_path).load()
        elif file_path.endswith(".txt"):
            return TextLoader(file_path).load()
        return []
    except Exception:
        return []
