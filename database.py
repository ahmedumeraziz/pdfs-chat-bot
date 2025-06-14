import os
import uuid
from chromadb.config import Settings
import chromadb

# Configure ChromaDB settings
CHROMA_SETTINGS = Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="chroma_storage",
    anonymized_telemetry=False
)

def initialize_vector_db():
    # Create storage directory if it doesn't exist
    os.makedirs("chroma_storage", exist_ok=True)
    
    client = chromadb.Client(CHROMA_SETTINGS)
    
    # Create or get collection with proper embedding function
    embedding_function = chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    return client.get_or_create_collection(
        name="pdf_knowledge",
        embedding_function=embedding_function
    )

def add_to_collection(chunks: list):
    try:
        collection = initialize_vector_db()
        ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
        collection.add(
            documents=chunks,
            ids=ids
        )
        return True
    except Exception as e:
        print(f"Error adding to collection: {e}")
        return False
