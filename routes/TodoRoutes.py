import traceback
from flask import Blueprint, request
from controllers.TodoControllers import TodoControllers
from routes.base import format_return, error_return
from lib.auth import check_auth

todo = Blueprint("todo", __name__)
todo.before_request(check_auth)


@todo.route("/categories", methods=["GET"])
def fetch_categories():
    try:
        return format_return(TodoControllers.fetch_categories())
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to fetch categories"}, 500)


@todo.route("/categories", methods=["POST"])
def create_category():
    try:
        data = request.get_json()
        TodoControllers.create_category(data["name"], data.get("subcategoryNames", []))
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to create category"}, 500)


@todo.route("/categories/<int:id>", methods=["PUT"])
def update_category(id: int):
    try:
        data = request.get_json()
        TodoControllers.update_category(id, data["name"])
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to update category"}, 500)


@todo.route("/categories/<int:id>", methods=["DELETE"])
def delete_category(id: int):
    try:
        TodoControllers.delete_category(id)
        return format_return({"success": True})
    except ValueError as e:
        return error_return({"error": str(e)}, 409)
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to delete category"}, 500)


@todo.route("/categories/<int:id>/subcategories", methods=["POST"])
def add_subcategory(id: int):
    try:
        data = request.get_json()
        TodoControllers.create_subcategory(id, data["name"])
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to add subcategory"}, 500)


@todo.route("/subcategories/<int:id>", methods=["PUT"])
def update_subcategory(id: int):
    try:
        data = request.get_json()
        TodoControllers.update_subcategory(id, data["name"])
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to update subcategory"}, 500)


@todo.route("/subcategories/<int:id>", methods=["DELETE"])
def delete_subcategory(id: int):
    try:
        TodoControllers.delete_subcategory(id)
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to delete subcategory"}, 500)


@todo.route("/templates", methods=["GET"])
def fetch_templates():
    try:
        category_id = request.args.get("categoryId", type=int, default=None)
        subcategory_id = request.args.get("subcategoryId", type=int, default=None)
        return format_return(TodoControllers.fetch_templates(category_id, subcategory_id))
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to fetch templates"}, 500)


@todo.route("/templates", methods=["POST"])
def create_template():
    try:
        data = request.get_json()
        result = TodoControllers.create_template(
            title=data["title"],
            notes=data.get("notes"),
            category_id=data["categoryId"],
            subcategory_id=data.get("subcategoryId"),
            frequency=data["frequency"],
            checklist_items=data.get("checklistItems", []),
        )
        return format_return({"id": result["id"]})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to create template"}, 500)


@todo.route("/templates/<int:id>", methods=["PUT"])
def update_template(id: int):
    try:
        data = request.get_json()
        TodoControllers.update_template(
            id=id,
            title=data["title"],
            notes=data.get("notes"),
            category_id=data["categoryId"],
            subcategory_id=data.get("subcategoryId"),
            frequency=data["frequency"],
            checklist_items=data.get("checklistItems", []),
        )
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to update template"}, 500)


@todo.route("/templates/<int:id>", methods=["DELETE"])
def delete_template(id: int):
    try:
        TodoControllers.delete_template(id)
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to delete template"}, 500)


@todo.route("/history", methods=["GET"])
def fetch_history():
    try:
        category_id = request.args.get("categoryId", type=int, default=None)
        subcategory_id = request.args.get("subcategoryId", type=int, default=None)
        return format_return(TodoControllers.fetch_history(category_id, subcategory_id))
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to fetch history"}, 500)


@todo.route("/tasks", methods=["GET"])
def fetch_tasks():
    try:
        category_id = request.args.get("categoryId", type=int, default=None)
        subcategory_id = request.args.get("subcategoryId", type=int, default=None)
        return format_return(TodoControllers.fetch_tasks(category_id, subcategory_id))
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to fetch tasks"}, 500)


@todo.route("/tasks", methods=["POST"])
def add_task():
    try:
        data = request.get_json()
        TodoControllers.add_task(data["templateId"])
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to add task"}, 500)


@todo.route("/tasks/direct", methods=["POST"])
def add_direct_task():
    try:
        data = request.get_json()
        TodoControllers.add_direct_task(
            title=data["title"],
            notes=data.get("notes"),
            category_id=data["categoryId"],
            subcategory_id=data.get("subcategoryId"),
            frequency=data.get("frequency", "one_time"),
        )
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to add direct task"}, 500)


@todo.route("/tasks/<int:id>/complete", methods=["PUT"])
def complete_task(id: int):
    try:
        TodoControllers.complete_task(id)
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to complete task"}, 500)


@todo.route("/tasks/<int:id>", methods=["DELETE"])
def remove_task(id: int):
    try:
        TodoControllers.remove_task(id)
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to remove task"}, 500)


@todo.route("/tasks/<int:task_id>/checklist", methods=["POST"])
def add_checklist_item(task_id: int):
    try:
        data = request.get_json()
        item = TodoControllers.add_checklist_item(task_id, data["text"])
        return format_return(item)
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to add checklist item"}, 500)


@todo.route("/checklist/<int:item_id>", methods=["PUT"])
def update_checklist_item(item_id: int):
    try:
        data = request.get_json()
        TodoControllers.update_checklist_item(
            item_id,
            text=data.get("text"),
            checked=data.get("checked"),
        )
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to update checklist item"}, 500)


@todo.route("/checklist/<int:item_id>", methods=["DELETE"])
def delete_checklist_item(item_id: int):
    try:
        TodoControllers.delete_checklist_item(item_id)
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to delete checklist item"}, 500)
