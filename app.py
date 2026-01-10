from flask import Flask, render_template, request, jsonify
import os
from document_reader import read_document
from chunker import chunk_pages
from embedder import embed_chunks
from vector import store_in_chroma
from queryprocess import process_query_user # Import the logic we fixed above

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.pptx', '.jpg', '.png', '.jpeg'}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf_file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['pdf_file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        pages = read_document(file_path) 
        chunks = chunk_pages(pages, chunk_size=1000, chunk_overlap=150)
        embeddings = embed_chunks(chunks)
        store_in_chroma(chunks, embeddings, filename=file.filename)
        
        return jsonify({"message": f"Successfully processed {file.filename}!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            
@app.route('/query', methods=['POST'])
def query_rag():
    data = request.json
    user_query = data.get("query")
    
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    try:
        # FIX: Use the imported function to avoid duplicate/buggy logic
        answer = process_query_user(user_query)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)