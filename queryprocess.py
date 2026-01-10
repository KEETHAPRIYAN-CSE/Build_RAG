import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
import ollama

def process_query_user(user_query: str):
    # 1. Connect to local ChromaDB
    client = chromadb.PersistentClient(path="./chroma_db")

    # 2. Re-initialize embedding function
    ollama_ef = OllamaEmbeddingFunction(
        url="http://localhost:11434/api/embeddings",
        model_name="mxbai-embed-large"
    )

    # 3. Access collection
    collection = client.get_collection(
        name="pdf_collection", 
        embedding_function=ollama_ef
    )

    # 4. RETRIEVAL
    results = collection.query(
        query_texts=[user_query],
        n_results=3 
    )

    retrieved_docs = results['documents'][0]
    metadatas = results['metadatas'][0]
    
    context_parts = []
    # FIX: Corrected indentation for the loop
    for doc, meta in zip(retrieved_docs, metadatas):
        source_info = f"[Source: {meta.get('source', 'Unknown')}]"
        context_parts.append(f"{source_info}\n{doc}")
    
    # FIX: Define the 'context' variable by joining the parts
    context = "\n\n".join(context_parts)
    
    print(f"--- Context retrieved from {len(retrieved_docs)} chunks ---")

    # 5. GENERATION
    prompt = f"""
    You are a helpful assistant. Use the provided context to answer the user's question.
    If the answer is not in the context, say you don't know.
    
    CONTEXT:
    {context}
    
    USER QUESTION: 
    {user_query}
    
    ANSWER:
    """

    response = ollama.generate(
        model="llama3.2", 
        prompt=prompt
    )

    return response['response']

if __name__ == "__main__":
    query = input("Enter your question: ")
    answer = process_query_user(query)
    print("\n--- LLM RESPONSE ---")
    print(answer)