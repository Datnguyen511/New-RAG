import streamlit as st
from loaders import get_document_files, load_documents
from processing import chunk_documents, index_documents, init_vectorstore
from qa_engine import retrieve_and_rerank, generate_answer
from style import inject_custom_css

VECTORSTORE_PATH = "faiss_index"
TEXT_FOLDER = "text"

# UI Setup
st.set_page_config(page_title="Arthritis RAG Chat", layout="centered")
st.title("🦴 Arthritis RAG Assistant")
st.markdown("---")
inject_custom_css()

# Vector DB Store
vector_db = init_vectorstore(VECTORSTORE_PATH)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

file_paths = get_document_files(TEXT_FOLDER)
all_docs = []

if file_paths:
    for file_path in file_paths:
        docs = load_documents(file_path)
        all_docs.extend(docs)
        st.success(f"Loaded: {file_path}")
    
    if all_docs:
        chunks = chunk_documents(all_docs)
        vector_db = index_documents(vector_db, chunks, VECTORSTORE_PATH)
else:
    st.warning("No files in the text/ folder.")

query = st.chat_input("Ask something about arthritis...")
if query:
    st.chat_message("user").write(query)
    st.session_state.chat_history.append({"role": "user", "content": query})

    with st.spinner("Thinking..."):
        docs = retrieve_and_rerank(vector_db, query)
        answer = generate_answer(query, docs)
    
    st.chat_message("assistant", avatar="🤖").write(answer)
    st.session_state.chat_history.append({"role": "assistant", "content": answer})

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

