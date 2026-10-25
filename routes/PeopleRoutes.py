import traceback

from flask import Blueprint, g, request

from controllers.PeopleControllers import PeopleControllers
from lib.auth import check_user_auth
from routes.base import error_return, format_return

people = Blueprint("people", __name__)
people.before_request(check_user_auth)


@people.route("/", methods=["GET"])
def fetch_people():
    try:
        data = PeopleControllers.fetch_people(g.user_id)
        return format_return(data)
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to fetch people"}, 500)


@people.route("/", methods=["POST"])
def create_person():
    try:
        data = request.get_json()
        person_id = PeopleControllers.create_person(g.user_id, data["name"])
        return format_return({"id": person_id})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to create person"}, 500)


@people.route("/<int:person_id>", methods=["DELETE"])
def delete_person(person_id: int):
    try:
        PeopleControllers.delete_person(person_id, g.user_id)
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to delete person"}, 500)


@people.route("/<int:person_id>/categories", methods=["GET"])
def fetch_categories(person_id: int):
    try:
        data = PeopleControllers.fetch_categories(person_id)
        return format_return(data)
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to fetch categories"}, 500)


@people.route("/<int:person_id>/categories", methods=["POST"])
def create_category(person_id: int):
    try:
        data = request.get_json()
        PeopleControllers.create_category(
            person_id,
            data["name"],
            data.get("subcategoryNames", []),
        )
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to create category"}, 500)


@people.route("/<int:person_id>/categories/<int:id>", methods=["PUT"])
def update_category(person_id: int, id: int):
    try:
        data = request.get_json()
        PeopleControllers.update_category(id, data["name"])
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to update category"}, 500)


@people.route("/<int:person_id>/categories/<int:id>", methods=["DELETE"])
def delete_category(person_id: int, id: int):
    try:
        PeopleControllers.delete_category(id)
        return format_return({"success": True})
    except ValueError as e:
        return error_return({"error": str(e)}, 409)
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to delete category"}, 500)


@people.route("/<int:person_id>/categories/<int:category_id>/subcategories", methods=["POST"])
def add_subcategory(person_id: int, category_id: int):
    try:
        data = request.get_json()
        PeopleControllers.create_subcategory(person_id, category_id, data["name"])
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to add subcategory"}, 500)


@people.route("/<int:person_id>/subcategories/<int:id>", methods=["PUT"])
def update_subcategory(person_id: int, id: int):
    try:
        data = request.get_json()
        PeopleControllers.update_subcategory(id, data["name"])
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to update subcategory"}, 500)


@people.route("/<int:person_id>/subcategories/<int:id>", methods=["DELETE"])
def delete_subcategory(person_id: int, id: int):
    try:
        PeopleControllers.delete_subcategory(id)
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to delete subcategory"}, 500)


@people.route("/<int:person_id>/ideas", methods=["GET"])
def fetch_ideas(person_id: int):
    try:
        category_id = request.args.get("categoryId", type=int, default=None)
        subcategory_id = request.args.get("subcategoryId", type=int, default=None)
        data = PeopleControllers.fetch_ideas(person_id, category_id, subcategory_id)
        return format_return(data)
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to fetch ideas"}, 500)


@people.route("/<int:person_id>/ideas", methods=["POST"])
def create_idea(person_id: int):
    try:
        data = request.get_json()
        PeopleControllers.create_idea(
            person_id,
            category_id=data["categoryId"],
            title=data["title"],
            notes=data.get("notes"),
            subcategory_id=data.get("subcategoryId"),
        )
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to create idea"}, 500)


@people.route("/<int:person_id>/ideas/<int:id>", methods=["PUT"])
def update_idea(person_id: int, id: int):
    try:
        data = request.get_json()
        PeopleControllers.update_idea(
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


@people.route("/<int:person_id>/ideas/<int:id>", methods=["DELETE"])
def delete_idea(person_id: int, id: int):
    try:
        PeopleControllers.delete_idea(id)
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to delete idea"}, 500)
