
import streamlit as st
import os
import openai
from utils.pdf_loader import load_pdfs
from utils.rag_utils import embed_documents, query_llama_with_groq
import streamlit_authenticator as stauth

st.set_page_config(page_title="Legal RAG Chatbot", layout="wide")

# Setup JWT Login with multiple users
credentials = {
    'user1': {'name': 'Ali Khan', 'password': stauth.Hasher(['pass123']).generate()[0]},
    'user2': {'name': 'Zainab Raza', 'password': stauth.Hasher(['secure456']).generate()[0]}
}
authenticator = stauth.Authenticate(credentials, 'legal_app', 'abcdef', cookie_expiry_days=1)
name, auth_status, username = authenticator.login('Login', 'main')

# GROQ API Key
openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"
openai.api_type = "open_ai"
openai.api_version = None

if auth_status:
    st.success(f"Welcome {name} 👋")
    st.header("📄 Upload Law PDFs")
    uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            with open(f"data/pdf_files/{file.name}", "wb") as f:
                f.write(file.read())
        st.success("✅ Files uploaded successfully. They will be used in future chats.")

    if st.button("📌 Embed PDFs"):
        documents = load_pdfs("data/pdf_files")
        embed_documents(documents)
        st.success("✅ All documents embedded into ChromaDB")

    st.header("💬 Ask Your Legal Question")
    user_question = st.text_input("Enter your question:")
    if user_question:
        answer = query_llama_with_groq(user_question)
        st.write("### Answer:")
        st.success(answer)

elif auth_status is False:
    st.error("❌ Incorrect username or password")
elif auth_status is None:
    st.warning("🔐 Please enter your login credentials")
