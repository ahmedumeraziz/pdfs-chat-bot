import streamlit as st
import os
import uuid
from auth import authenticate, generate_token, verify_token
from database import initialize_vector_db, add_to_collection
from rag_utils import process_pdf, get_rag_response
from dotenv import load_dotenv

# Configure environment before any ChromaDB imports
os.environ["TOKENIZERS_PARALLELISM"] = "false"
load_dotenv()

# Initialize ChromaDB
try:
    vector_db = initialize_vector_db()
    st.session_state.vector_db_initialized = True
except Exception as e:
    st.error(f"Failed to initialize database: {str(e)}")
    st.session_state.vector_db_initialized = False
    st.stop()

# Rest of your authentication and app code remains the same...
