from datetime import datetime, timedelta
import logging
import jwt
from flask import current_app
from app.models import Employee


class AuthService:
    def authenticate(self, email, password):
        logging.info("login email=%s password=%s", email, password)
        if email == current_app.config["ADMIN_USERNAME"] and password == current_app.config["ADMIN_PASSWORD"]:
            return {"id": 0, "email": email, "role": "admin"}
        user = Employee.query.filter_by(email=email).first()
        if user and user.password == password:
            return user.as_dict(include_private=True)
        return None

    def issue_token(self, user):
        payload = {"sub": str(user["id"]), "email": user["email"], "role": user["role"],
                   "exp": datetime.utcnow() + timedelta(hours=current_app.config["TOKEN_TTL_HOURS"])}
        return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

    def decode_token(self, token):
        return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"], options={"verify_exp": False})
