import streamlit as st
import os
import uuid
from auth import authenticate, generate_token, verify_token
from database import initialize_vector_db, add_to_collection
from rag_utils import process_pdf, get_rag_response
from dotenv import load_dotenv

load_dotenv()

# Initialize ChromaDB
vector_db = initialize_vector_db()

# Authentication
def login_section():
    st.sidebar.title("Authentication")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        if authenticate(username, password):
            token = generate_token(username)
            st.session_state.token = token
            st.session_state.logged_in = True
            st.sidebar.success("Logged in successfully!")
        else:
            st.sidebar.error("Invalid credentials")

def main_app():
    st.title("🧠 RAG Chatbot with PDF Processing")
    
    # PDF Upload
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    if uploaded_file:
        os.makedirs("data/pdf_files", exist_ok=True)
        file_path = f"data/pdf_files/{uuid.uuid4()}.pdf"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        chunks = process_pdf(file_path)
        add_to_collection(chunks)
        st.success(f"Processed {len(chunks)} chunks from {uploaded_file.name}")
    
    # Chat Interface
    st.subheader("Chat with your documents")
    user_input = st.text_input("Ask a question about your PDFs")
    
    if st.button("Submit") and user_input:
        with st.spinner("Thinking..."):
            response = get_rag_response(user_input, vector_db)
        st.markdown(f"**Answer:** {response}")

# App Flow
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    if verify_token(st.session_state.token):
        main_app()
    else:
        st.error("Session expired. Please log in again.")
        st.session_state.logged_in = False
        login_section()
else:
    login_section()
    
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.experimental_rerun()
