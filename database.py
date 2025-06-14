import chromadb
from chromadb.utils import embedding_functions
import os

def initialize_vector_db():
    client = chromadb.PersistentClient(path="chroma_storage")
    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    return client.get_or_create_collection(
        name="pdf_knowledge",
        embedding_function=embedding_func
    )

def add_to_collection(chunks: list):
    collection = initialize_vector_db()
    ids = [str(uuid.uuid4()) for _ in chunks]
    collection.add(documents=chunks, ids=ids)
