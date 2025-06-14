
import streamlit as st
from utils.pdf_loader import load_pdfs
from utils.rag_utils import embed_documents, query_llama

st.title("🧑‍⚖️ Legal AI Assistant")

if st.button("Embed PDFs"):
    docs = load_pdfs("data/law_pdfs")
    collection = embed_documents(docs)
    st.success("Documents embedded into ChromaDB!")

user_query = st.text_input("Ask a legal question:")
if user_query:
    results = collection.query(query_texts=[user_query], n_results=1)
    context = results['documents'][0][0]
    final_prompt = f"Context: {context}\n\nQuestion: {user_query}"
    answer = query_llama(final_prompt)
    st.write("### Answer:", answer)
