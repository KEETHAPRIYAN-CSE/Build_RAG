import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"

# FIX: Changed import from read_pdf to read_document
from document_reader import read_document 
from chunker import chunk_pages   
from embedder import embed_chunks
from vector import store_in_chroma

pdf_path = "oops.pdf" # Ensure this file exists in your directory

def run():
    # FIX: Changed call to read_document
    pages = read_document(pdf_path)

    chunks = chunk_pages(pages, chunk_size=1000, chunk_overlap=150)

    embedded_chunks = embed_chunks(chunks)
    
    # Store with filename for metadata
    store_in_chroma(chunks, embedded_chunks, filename=pdf_path)

if __name__ == "__main__":
    run()