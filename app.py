from tasks import process_document_task
import os 
from flask import request, jsonify
from werkzeug.utils import secure_filename
from flask import Flask
from models import db, Document 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

    # home function

UPLOAD_FOLDER = 'storage/documents'
os.makedirs(UPLOAD_FOLDER, exist_ok = True)

@app.route('/')
def home():
    return "Mini-Dify API is running!"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error":"No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)

    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    new_doc = Document(filename=filename, storage_path = file_path)
    db.session.add(new_doc)
    db.session.commit()
    process_document_task.delay(new_doc.id)

    return jsonify({
        "message": f"file {filename} uploaded and recorded!",
        "document_id": new_doc.id,
        "status": "PROCESSING_STARTED"
                    }),202

@app.route('/documents', methods=['GET'])
def list_documents():
    all_docs = Document.query.all()

    output = []
    for doc in all_docs:
        output.append({
            "id":doc.id,
            "filename": doc.filename,
            "status": doc.status,
            "path": doc.storage_path
        })

    return jsonify(output)

@app.route('/search', methods=['GET'])
def search_documents():
    
    query = request.args.get('q', '')

    if not query:
        return jsonify({"error": "Missing search query"}), 400
    
    results = Document.query.filter(
        Document.filename.contains(query),
        Document.status == 'COMPLETED'
    ).all()

    data = []
    for doc in results:
        data.append({
            "id": doc.id,
            "filename": doc.storage_path
            "path": doc.storage_path
        })

    return jsonify(data), 200




if __name__ == '__main__':
    app.run(debug=True)
