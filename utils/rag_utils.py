import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import openai

embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="legal_docs", embedding_function=embedding_function)

def embed_documents(documents):
    for i, doc in enumerate(documents):
        collection.add(
            documents=[doc["text"]],
            ids=[f"doc_{i}"],
            metadatas=[{"source": doc["filename"]}]
        )

def query_llama_with_groq(question):
    results = collection.query(query_texts=[question], n_results=1)
    context = results['documents'][0][0] if results['documents'] else "No relevant data found."

    messages = [
        {"role": "system", "content": "You are a helpful legal assistant. Use the legal context to answer the user's question."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
    ]

    response = openai.ChatCompletion.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=0.5
    )
    return response['choices'][0]['message']['content']
