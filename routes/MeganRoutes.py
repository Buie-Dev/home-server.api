import traceback

from flask import Blueprint, request

from controllers.MeganControllers import MeganControllers
from lib.auth import check_auth
from routes.base import error_return, format_return

megan = Blueprint("megan", __name__)
megan.before_request(check_auth)


@megan.route("/categories", methods=["GET"])
def fetch_categories():
    try:
        data = MeganControllers.fetch_categories()
        return format_return(data)
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to fetch categories"}, 500)


@megan.route("/categories", methods=["POST"])
def create_category():
    try:
        data = request.get_json()
        MeganControllers.create_category(
            name=data["name"],
            subcategory_names=data.get("subcategoryNames", []),
        )
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to create category"}, 500)


@megan.route("/categories/<int:id>", methods=["PUT"])
def update_category(id: int):
    try:
        data = request.get_json()
        MeganControllers.update_category(id, data["name"])
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to update category"}, 500)


@megan.route("/categories/<int:id>/subcategories", methods=["POST"])
def add_subcategory(id: int):
    try:
        data = request.get_json()
        MeganControllers.create_subcategory(id, data["name"])
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to add subcategory"}, 500)


@megan.route("/subcategories/<int:id>", methods=["PUT"])
def update_subcategory(id: int):
    try:
        data = request.get_json()
        MeganControllers.update_subcategory(id, data["name"])
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to update subcategory"}, 500)


@megan.route("/subcategories/<int:id>", methods=["DELETE"])
def delete_subcategory(id: int):
    try:
        MeganControllers.delete_subcategory(id)
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to delete subcategory"}, 500)


@megan.route("/categories/<int:id>", methods=["DELETE"])
def delete_category(id: int):
    try:
        MeganControllers.delete_category(id)
        return format_return({"success": True})
    except ValueError as e:
        return error_return({"error": str(e)}, 409)
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to delete category"}, 500)


@megan.route("/ideas", methods=["GET"])
def fetch_ideas():
    try:
        category_id = request.args.get("categoryId", type=int, default=None)
        subcategory_id = request.args.get("subcategoryId", type=int, default=None)
        data = MeganControllers.fetch_ideas(category_id, subcategory_id)
        return format_return(data)
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to fetch ideas"}, 500)


@megan.route("/ideas", methods=["POST"])
def create_idea():
    try:
        data = request.get_json()
        MeganControllers.create_idea(
            category_id=data["categoryId"],
            title=data["title"],
            notes=data.get("notes"),
            subcategory_id=data.get("subcategoryId"),
        )
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to create idea"}, 500)


@megan.route("/ideas/<int:id>", methods=["PUT"])
def update_idea(id: int):
    try:
        data = request.get_json()
        MeganControllers.update_idea(
            id=id,
            title=data["title"],
            notes=data.get("notes"),
            category_id=data["categoryId"],
            subcategory_id=data.get("subcategoryId"),
        )
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to update idea"}, 500)


@megan.route("/ideas/<int:id>/toggle", methods=["PUT"])
def toggle_idea(id: int):
    try:
        data = request.get_json()
        MeganControllers.toggle_idea(id, data["completed"])
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to toggle idea"}, 500)


@megan.route("/ideas/<int:id>", methods=["DELETE"])
def delete_idea(id: int):
    try:
        MeganControllers.delete_idea(id)
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to delete idea"}, 500)
