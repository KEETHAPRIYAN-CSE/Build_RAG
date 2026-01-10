📄 Local PDF RAG System

A private, fully local Retrieval-Augmented Generation (RAG) system that allows you to chat with your PDF documents using Ollama for local LLMs and ChromaDB for vector storage — without sending any data to the cloud.

🚀 Project Overview

This project enables you to extract and query knowledge from local PDF files securely.
It follows a modular pipeline for:
PDF text extraction
Intelligent text chunking
Embedding generation
Persistent vector storage
Context-aware question answering
All processing happens locally, ensuring privacy and full control over your data.

🧠 Key Technologies
Language Model: Llama 3.2 (via Ollama)
Embedding Model: mxbai-embed-large (via Ollama)
Vector Database: ChromaDB (local persistence)
PDF Processing: pypdf
Text Chunking: Recursive Character Text Splitting

🛠️ System Flow
The system operates in two main phases:
1️⃣ Data Ingestion Phase
This phase prepares your documents for retrieval and search.

Extraction
pdfreader.py reads the PDF and extracts raw text page-by-page.

Chunking
chunker.py splits large text into smaller chunks
Chunk size: 1000 characters
Overlap: 150 characters (to preserve context)

Embedding
embedder.py converts text chunks into numerical vectors using a local embedding model.

Storage
vector.py stores vectors and metadata in a local chroma_db/ directory.

2️⃣ User Query Phase
This phase handles real-time interaction.

Vectorization
The user’s question is converted into an embedding.

Retrieval
ChromaDB retrieves the top 3 most relevant chunks from the database.

Augmentation
Retrieved content is injected into a structured prompt.

Generation
Llama 3.2 generates a response strictly based on the retrieved document context.

📂 Project File Structure
.
├── dataprocess.py      # Orchestrates the ingestion pipeline
├── pdfreader.py        # Extracts text from PDFs
├── chunker.py          # Splits text into overlapping chunks
├── embedder.py         # Generates embeddings using Ollama
├── vector.py           # Manages ChromaDB storage
├── queryprocess.py     # Handles user queries and responses
├── requirements.txt    # Python dependencies
└── chroma_db/          # Local vector database (auto-generated)

🚦 Getting Started
✅ Prerequisites

Install Ollama and ensure it is running.

Download the required models:
ollama pull mxbai-embed-large
ollama pull llama3.2

📦 Installation
Clone this repository and navigate into the project directory.

Install dependencies:
pip install -r requirements.txt

▶️ Usage
1️⃣ Add Your PDF
Place your PDF file (e.g., oops.pdf) in the project root directory.

2️⃣ Ingest the Document
Run the ingestion pipeline:
python dataprocess.py


This will:
Read the PDF
Split text into chunks
Generate embeddings
Store vectors locally in ChromaDB

3️⃣ Ask Questions
Start querying your document:
python queryprocess.py

Ask natural-language questions and receive document-grounded answers.

🔒 Privacy & Security
No cloud APIs
No data leaves your system
Fully offline after model download

⭐ Use Cases

Private document Q&A
Study and exam preparation
Technical documentation search
Research paper analysis
Secure enterprise knowledge bases
