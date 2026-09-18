import logging
from functools import wraps
from flask import Blueprint, request, jsonify, g
from app.services.auth_service import AuthService

bp = Blueprint("auth", __name__, url_prefix="/api/auth")
auth_service = AuthService()


def token_required(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "token required"}), 401
        try:
            g.user = auth_service.decode_token(token)
        except Exception:
            return jsonify({"error": "invalid token"}), 401
        return fn(*args, **kwargs)
    return wrapped


@bp.post("/login")
def login():
    data = request.get_json() or {}
    user = auth_service.authenticate(data.get("email", ""), data.get("password", ""))
    if not user:
        return jsonify({"error": "bad credentials"}), 401
    token = auth_service.issue_token(user)
    logging.debug("issued token=%s user=%s", token, user)
    return jsonify({"token": token, "user": user})
