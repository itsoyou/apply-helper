import os

from flask import Blueprint, jsonify, render_template, request
from werkzeug.utils import secure_filename

from apply_helper.assistant import (
    add_question,
    checking_status,
    create_thread,
    run_assistant,
)
from apply_helper.config import Config
from apply_helper.file_manager import allowed_file, upload_pdf_to_vector_store

main_routes = Blueprint("main", __name__)


@main_routes.route("/")
def index():
    return render_template("index.html")


@main_routes.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(file_path)

        vector_store_id = upload_pdf_to_vector_store(
            Config.CLIENT, Config.ASSISTANT_ID, file_path
        )
        os.remove(file_path)

        if vector_store_id:
            return (
                jsonify(
                    {"message": "File uploaded and processed successfully."}
                ),
                200,
            )
        else:
            return jsonify({"error": "Failed to process file."}), 500

    return jsonify({"error": "Invalid file type."}), 400


@main_routes.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    question = data.get("question")
    if not question:
        return jsonify({"error": "No question provided."}), 400
    if not Config.THREAD_ID:
        Config.THREAD_ID = create_thread()
    add_question(Config.THREAD_ID, question)
    run_response = run_assistant(Config.THREAD_ID, Config.ASSISTANT_ID)
    run_id = run_response.id
    answers = checking_status(Config.THREAD_ID, run_id)
    if answers:
        return jsonify({"answers": answers}), 200
    else:
        return jsonify({"error": "No answers found."}), 500


def init_routes(app):
    app.register_blueprint(main_routes)
