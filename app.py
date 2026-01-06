from flask import Flask, request, jsonify , render_template
from flask_cors import CORS
import os, uuid
from services.vector_db import splitter, vector_store 
from services.file_handling import get_loader
from services.LLM import get_chat_response 

app = Flask(__name__)

CORS(app)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    user_id = request.form.get("user_id", "default_user")

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    file_id = str(uuid.uuid4())
    save_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    file.save(save_path)

    try:
        loader = get_loader(save_path)
        documents = loader.load()

        for doc in documents:
            doc.metadata["source"] = file.filename
            doc.metadata["file_id"] = file_id
            doc.metadata["user_id"] = user_id

        chunks = splitter.split_documents(documents)
        vector_store.add_documents(chunks)
        
        return jsonify({
            "message": f"{file.filename} uploaded & indexed",
            "file_id": file_id
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_id = data.get("user_id")
    message = data.get("message")

    if not user_id or not message:
        return jsonify({"error": "user_id and message are required"}), 400

    try:
        
        response = get_chat_response(user_id, message)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)