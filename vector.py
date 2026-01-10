import os
import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction

def store_in_chroma(chunks, embeddings, filename="document"):
    client = chromadb.PersistentClient(path="./chroma_db")

    ollama_ef = OllamaEmbeddingFunction(
        url="http://localhost:11434/api/embeddings",
        model_name="mxbai-embed-large"
    )

    collection = client.get_or_create_collection(
        name="pdf_collection",
        embedding_function=ollama_ef
    )

    # Determine file type for metadata
    extension = os.path.splitext(filename)[1].lower()

    ids = [f"{filename}_{i}_{os.urandom(4).hex()}" for i in range(len(chunks))]
    metadatas = [
        {
            "source": filename, 
            "type": extension, 
            "chunk_index": i
        } for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas
    )
    print(f"--- SUCCESS: {len(chunks)} chunks from {filename} stored ---")