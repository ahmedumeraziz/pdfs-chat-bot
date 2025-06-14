
import os
import openai
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"

def embed_documents(documents):
    chroma_client = chromadb.Client()
    embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = chroma_client.create_collection(name="legal_docs", embedding_function=embedding_function)
    for i, doc in enumerate(documents):
        collection.add(
            documents=[doc["text"]],
            ids=[f"doc_{i}"],
            metadatas=[{"source": doc["filename"]}]
        )
    return collection

def query_llama(prompt):
    response = openai.ChatCompletion.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]
