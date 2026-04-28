import traceback
import bcrypt
from flask import Blueprint, request, jsonify
from config.config import Config
from lib.auth import create_token
from routes.base import error_return

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data.get("username", "")
        password = data.get("password", "")

        password_matches = bcrypt.checkpw(
            password.encode("utf-8"),
            Config.APP_PASSWORD_HASH.encode("utf-8")
        )
        if username != Config.APP_USERNAME or not password_matches:
            return error_return({"error": "Invalid credentials"}, 401)

        token = create_token(username)
        return jsonify({"token": token})
    except Exception as e:
        traceback.print_exc()
        return error_return({"error": "Login failed"}, 500)
