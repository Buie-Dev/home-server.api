import traceback

import bcrypt
from flask import Blueprint, g, jsonify, request

from lib.auth import check_user_auth, create_token, is_internal_request
from models.PermissionsModels import PermissionsModels
from models.UserModels import UserModels
from routes.base import error_return, format_return

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data.get("username", "")
        password = data.get("password", "")

        user = UserModels.fetch_by_username(username)
        if not user:
            return error_return({"error": "Invalid credentials"}, 401)

        password_matches = bcrypt.checkpw(
            password.encode("utf-8"),
            user["password_hash"].encode("utf-8"),
        )
        if not password_matches:
            return error_return({"error": "Invalid credentials"}, 401)

        token = create_token(user["id"], user["username"])
        return jsonify({"token": token})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Login failed"}, 500)


@auth.route("/me/permissions", methods=["GET"])
def get_my_permissions():
    blocked = check_user_auth()
    if blocked:
        return blocked
    try:
        pages = PermissionsModels.fetch_user_pages(g.user_id)
        return format_return({"user_id": g.user_id, "pages": pages})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to fetch permissions"}, 500)


@auth.route("/users/<username>/password", methods=["PUT"])
def update_password(username: str):
    if not is_internal_request():
        return error_return({"error": "Forbidden"}, 403)

    try:
        data = request.get_json()
        new_password = data.get("new_password", "")
        if not new_password:
            return error_return({"error": "new_password is required"}, 400)

        user = UserModels.fetch_by_username(username)
        if not user:
            return error_return({"error": "User not found"}, 404)

        new_hash = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        UserModels.update_password(username, new_hash)
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to update password"}, 500)
