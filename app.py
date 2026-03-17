"""Flask web app for bidirectional Word <-> PDF conversion."""

import os
import uuid
from pathlib import Path
from flask import Flask, render_template, request, send_file, jsonify, after_this_request
from werkzeug.utils import secure_filename
from converter import convert_word_to_pdf, convert_pdf_to_word

UPLOAD_FOLDER = Path("uploads")
CONVERTED_FOLDER = Path("converted")
ALLOWED_EXTENSIONS = {".docx", ".doc", ".pdf"}
MAX_FILE_SIZE_MB = 50

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE_MB * 1024 * 1024

UPLOAD_FOLDER.mkdir(exist_ok=True)
CONVERTED_FOLDER.mkdir(exist_ok=True)


def allowed_file(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if not file.filename:
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only .docx, .doc, and .pdf files are supported"}), 400

    unique_id = uuid.uuid4().hex[:8]
    original_name = secure_filename(file.filename)
    stem = Path(original_name).stem
    suffix = Path(original_name).suffix.lower()
    saved_name = f"{unique_id}_{stem}{suffix}"
    input_path = UPLOAD_FOLDER / saved_name
    file.save(str(input_path))

    try:
        if suffix in (".docx", ".doc"):
            output_path = convert_word_to_pdf(str(input_path), str(CONVERTED_FOLDER))
            download_name = stem + ".pdf"
            mimetype = "application/pdf"
        else:
            output_path = convert_pdf_to_word(str(input_path), str(CONVERTED_FOLDER))
            download_name = stem + ".docx"
            mimetype = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        input_path.unlink(missing_ok=True)
        return jsonify({"error": str(e)}), 500

    input_path.unlink(missing_ok=True)

    @after_this_request
    def cleanup(response):
        try:
            Path(output_path).unlink(missing_ok=True)
        except Exception:
            pass
        return response

    return send_file(
        output_path,
        as_attachment=True,
        download_name=download_name,
        mimetype=mimetype,
    )


@app.errorhandler(413)
def file_too_large(_):
    return jsonify({"error": f"File too large. Maximum size is {MAX_FILE_SIZE_MB} MB."}), 413


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
