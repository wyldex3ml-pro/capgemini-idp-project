"""
app.py
------
Main Flask application. Ties together:
  1. ocr_processor.py   -> reads the document
  2. nlp_extractor.py   -> pulls out key fields
  3. classifier.py      -> labels the document type
  4. database.py        -> stores the result
And serves a simple dashboard (templates/index.html) to upload files
and view processed results.
"""

from flask import Flask, request, render_template, redirect, url_for
import os

from ocr_processor import extract_text_from_file
from nlp_extractor import extract_fields
from classifier import classify_document
from database import init_db, save_document, get_all_documents

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

init_db()  # create the table if it doesn't exist yet


@app.route("/", methods=["GET"])
def index():
    documents = get_all_documents()
    return render_template("index.html", documents=documents)


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("document")
    if not file or file.filename == "":
        return redirect(url_for("index"))

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    # --- The IDP pipeline ---
    raw_text = extract_text_from_file(filepath)      # Step 1: OCR
    fields = extract_fields(raw_text)                  # Step 2: Extraction
    doc_type = classify_document(raw_text)              # Step 3: Classification
    save_document(file.filename, doc_type, fields, raw_text)  # Step 4: Store

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
