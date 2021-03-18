
############################################
# this is a Flask-based backend
############################################

import os
from flask import Flask, request, abort, jsonify, send_from_directory

import torch
import torch.nn as nn

UPLOAD_DIRECTORY = "flask-temp-storage"
JS_DIRECTORY = "js"

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

api = Flask(__name__)

@api.route("/files")
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)

@api.route("/js")
def list_js():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(JS_DIRECTORY):
        path = os.path.join(JS_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)

@api.route("/files/<path:path>")
def get_file(path):
    """Download a file."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)



@api.route("/js/<path:path>")
def get_js_script(path):
    """Download a file."""
    return send_from_directory(JS_DIRECTORY, path, as_attachment=False)


@api.route("/files/<filename>", methods=["POST"])
def post_file(filename):
    """Upload a file."""

    if "/" in filename:
        # Return 400 BAD REQUEST
        abort(400, "no subdirectories allowed")

    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
        fp.write(request.data)

    # Return 201 CREATED
    return jsonify({'status': 'OK'})

if __name__ == "__main__":
    api.run(debug=True, port=5000)
