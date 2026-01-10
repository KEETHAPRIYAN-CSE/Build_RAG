from flask import Flask, render_template, request, jsonify
import os
from pdfreader import read_pdf
from chunker import chunk_pages
from embedder import embed_chunks
from vector import store_in_chroma

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf_file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['pdf_file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        try:
            # Using your existing logic
            pages = read_pdf(file_path)
            chunks = chunk_pages(pages, chunk_size=1000, chunk_overlap=150)
            embeddings = embed_chunks(chunks)
            store_in_chroma(chunks, embeddings, pdf_name=file.filename)
            
            return jsonify({"message": f"Successfully processed {len(chunks)} chunks!"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)