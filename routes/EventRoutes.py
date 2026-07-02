import traceback
from flask import Blueprint, request
from controllers.EventControllers import EventControllers
from routes.base import format_return, error_return
from lib.auth import check_auth

events = Blueprint("events", __name__)
events.before_request(check_auth)


@events.route("/categories", methods=["GET"])
def fetch_categories():
    try:
        return format_return(EventControllers.fetch_categories())
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to fetch categories"}, 500)


@events.route("/categories", methods=["POST"])
def create_category():
    try:
        data = request.get_json()
        EventControllers.create_category(data["name"], data.get("subcategoryNames", []))
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to create category"}, 500)


@events.route("/categories/<int:id>", methods=["PUT"])
def update_category(id: int):
    try:
        data = request.get_json()
        EventControllers.update_category(id, data["name"])
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to update category"}, 500)


@events.route("/categories/<int:id>", methods=["DELETE"])
def delete_category(id: int):
    try:
        EventControllers.delete_category(id)
        return format_return({"success": True})
    except ValueError as e:
        return error_return({"error": str(e)}, 409)
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to delete category"}, 500)


@events.route("/categories/<int:id>/subcategories", methods=["POST"])
def add_subcategory(id: int):
    try:
        data = request.get_json()
        EventControllers.create_subcategory(id, data["name"])
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to add subcategory"}, 500)


@events.route("/subcategories/<int:id>", methods=["PUT"])
def update_subcategory(id: int):
    try:
        data = request.get_json()
        EventControllers.update_subcategory(id, data["name"])
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to update subcategory"}, 500)


@events.route("/subcategories/<int:id>", methods=["DELETE"])
def delete_subcategory(id: int):
    try:
        EventControllers.delete_subcategory(id)
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to delete subcategory"}, 500)


@events.route("", methods=["GET"])
def fetch_events():
    try:
        category_id = request.args.get("categoryId", type=int, default=None)
        subcategory_id = request.args.get("subcategoryId", type=int, default=None)
        month = request.args.get("month", type=int, default=None)
        year = request.args.get("year", type=int, default=None)
        return format_return(EventControllers.fetch_events(category_id, subcategory_id, month, year))
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to fetch events"}, 500)


@events.route("", methods=["POST"])
def create_event():
    try:
        data = request.get_json()
        EventControllers.create_event(
            title=data["title"],
            description=data.get("description"),
            date=data["date"],
            time=data.get("time"),
            category_id=data["categoryId"],
            subcategory_id=data.get("subcategoryId"),
        )
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to create event"}, 500)


@events.route("/<int:id>", methods=["PUT"])
def update_event(id: int):
    try:
        data = request.get_json()
        EventControllers.update_event(
            id=id,
            title=data["title"],
            description=data.get("description"),
            date=data["date"],
            time=data.get("time"),
            category_id=data["categoryId"],
            subcategory_id=data.get("subcategoryId"),
        )
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to update event"}, 500)


@events.route("/<int:id>", methods=["DELETE"])
def delete_event(id: int):
    try:
        EventControllers.delete_event(id)
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to delete event"}, 500)
