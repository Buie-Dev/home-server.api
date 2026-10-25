import traceback

import bcrypt
from flask import Blueprint, g, request

from lib.auth import check_user_auth, is_internal_request
from models.PermissionsModels import PermissionsModels
from models.UserModels import UserModels
from routes.base import error_return, format_return

admin = Blueprint("admin", __name__)


def _require_admin():
    """Allow internal requests through; external requests need a valid token + admin permission."""
    if is_internal_request():
        return None
    result = check_user_auth()
    if result is not None:
        return result
    pages = PermissionsModels.fetch_user_pages(g.user_id)
    if "admin" not in pages:
        return error_return({"error": "Forbidden"}, 403)
    return None


@admin.route("/users", methods=["GET"])
def get_users():
    blocked = _require_admin()
    if blocked:
        return blocked
    try:
        data = PermissionsModels.fetch_all_users_with_permissions()
        return format_return(data)
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to fetch users"}, 500)


@admin.route("/users", methods=["POST"])
def create_user():
    blocked = _require_admin()
    if blocked:
        return blocked
    try:
        data = request.get_json()
        username = (data.get("username") or "").strip()
        password = data.get("password") or ""
        if not username or not password:
            return error_return({"error": "Username and password are required"}, 400)
        if UserModels.fetch_by_username(username):
            return error_return({"error": "Username already exists"}, 409)
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_id = UserModels.create_user(username, password_hash)
        return format_return({"id": new_id, "username": username}), 201
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to create user"}, 500)


@admin.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int):
    blocked = _require_admin()
    if blocked:
        return blocked
    try:
        if not is_internal_request() and g.user_id == user_id:
            return error_return({"error": "Cannot delete yourself"}, 403)
        user = UserModels.fetch_by_id(user_id)
        if not user:
            return error_return({"error": "User not found"}, 404)
        UserModels.soft_delete_user(user_id)
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to delete user"}, 500)


@admin.route("/users/<int:user_id>/permissions", methods=["PUT"])
def set_permissions(user_id: int):
    blocked = _require_admin()
    if blocked:
        return blocked
    try:
        permissions = request.get_json()
        user = UserModels.fetch_by_username_or_id(user_id)
        if not user:
            return error_return({"error": "User not found"}, 404)
        PermissionsModels.set_user_permissions(user_id, permissions)
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to update permissions"}, 500)
