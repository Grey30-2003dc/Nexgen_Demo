from flask import jsonify


def api_error(message, status=400):
    return jsonify({"error": message}), status
