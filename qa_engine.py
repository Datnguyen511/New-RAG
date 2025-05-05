from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from sentence_transformers import CrossEncoder

RERANKER = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
LLM = OllamaLLM(model="deepseek-r1:1.5b")
PROMPT_TEMPLATE = """
You are a helpful AI assistant. Use the provided context to answer the query.
If unsure, say you don't know. Be concise (max 3 sentences).

Query: {user_query}
Context: {document_context}
Answer:
"""

def retrieve_and_rerank(vector_db, query, top_k=8):
    if vector_db is None:
        return []
    docs = vector_db.similarity_search(query, k=top_k)
    if not docs:
        return []
    scores = RERANKER.predict([(query, doc.page_content) for doc in docs])
    ranked = [doc for _, doc in sorted(zip(scores, docs), key=lambda x: x[0], reverse=True)]
    return ranked[:5]

def generate_answer(query, docs):
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    chain = prompt | LLM
    return chain.invoke({"user_query": query, "document_context": context})
