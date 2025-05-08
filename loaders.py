import os
import hashlib
import json
from langchain_community.document_loaders import PDFPlumberLoader, TextLoader

def get_document_files(folder):
    try:
        return [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith((".pdf", ".txt"))]
    except Exception as e:
        return []

def load_documents(file_path):
    try:
        if file_path.lower().endswith(".pdf"):
            return PDFPlumberLoader(file_path).load()
        elif file_path.lower().endswith(".txt"):
            return TextLoader(file_path).load()
        return []
    except Exception:
        return []

# Hashing so we wont need reprocessing & reindexing everytime
def compute_file_hash(path):
    hasher = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return None

def load_hash_index(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_hash_index(filename, index):
    try:
        with open(filename, "w") as f:
            json.dump(index, f, indent=2)
    except Exception:
        pass

def get_new_or_changed_files(file_paths, old_hash_index):
    new_files = []
    new_hash_index = {}

    for path in file_paths:
        file_hash = compute_file_hash(path)
        new_hash_index[path] = file_hash

        if old_hash_index.get(path) != file_hash:
            new_files.append(path)

    return new_files, new_hash_index
