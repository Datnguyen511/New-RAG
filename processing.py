import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

EMBEDDING_MODEL = OllamaEmbeddings(model="deepseek-r1:1.5b")

def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
    return splitter.split_documents(documents)

def init_vectorstore(path):
    if os.path.exists(path):
        return FAISS.load_local(path, EMBEDDING_MODEL, allow_dangerous_deserialization=True)
    return None

def index_documents(vector_db, chunks, path):
    docs = []
    for i, doc in enumerate(chunks):
        metadata = doc.metadata
        metadata["chunk_id"] = i
        docs.append(Document(page_content=doc.page_content, metadata=metadata))

    if vector_db is None:
        vector_db = FAISS.from_documents(docs, EMBEDDING_MODEL)
    else:
        vector_db.add_documents(docs)

    vector_db.save_local(path)
    return vector_db


