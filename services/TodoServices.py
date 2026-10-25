from datetime import datetime
from models.TodoModels import TodoModels
from typing import List, Optional


class TodoServices:
    @staticmethod
    def fetch_categories():
        categories = TodoModels.fetch_categories()
        subcategories = TodoModels.fetch_subcategories()
        result = [
            {
                "id": c["id"],
                "name": c["name"],
                "subcategories": [],
                "itemCount": TodoModels.count_active_templates(c["id"]),
            }
            for c in categories
        ]
        for sub in subcategories:
            cat = next((c for c in result if c["id"] == sub["category_id"]), None)
            if cat is not None:
                cat["subcategories"].append({"id": sub["id"], "name": sub["name"], "categoryId": sub["category_id"]})
        return result

    @staticmethod
    def create_category(name: str, subcategory_names: List[str]):
        result = TodoModels.create_category(name)
        category_id = result["inserted_id"]
        for i, sub_name in enumerate(subcategory_names):
            TodoModels.create_subcategory(category_id, sub_name, i)
        return category_id

    @staticmethod
    def create_subcategory(category_id: int, name: str):
        return TodoModels.create_subcategory(category_id, name)

    @staticmethod
    def update_category(id: int, name: str):
        return TodoModels.update_category(id, name)

    @staticmethod
    def update_subcategory(id: int, name: str):
        return TodoModels.update_subcategory(id, name)

    @staticmethod
    def delete_subcategory(id: int):
        return TodoModels.delete_subcategory(id)

    @staticmethod
    def delete_category(id: int):
        count = TodoModels.count_active_templates(id)
        if count > 0:
            raise ValueError(f"Category has {count} active template(s) and cannot be deleted")
        TodoModels.delete_category(id)

    @staticmethod
    def fetch_templates(category_id: Optional[int] = None, subcategory_id: Optional[int] = None):
        templates = TodoModels.fetch_templates(category_id, subcategory_id)
        if templates:
            template_ids = [t["id"] for t in templates]
            checklist_items = TodoModels.fetch_template_checklist(template_ids)
            checklist_map: dict = {}
            for item in checklist_items:
                tid = item["templateId"]
                if tid not in checklist_map:
                    checklist_map[tid] = []
                checklist_map[tid].append({"id": item["id"], "text": item["text"]})
            for template in templates:
                template["checklistItems"] = checklist_map.get(template["id"], [])
        return templates

    @staticmethod
    def create_template(
        title: str,
        notes: Optional[str],
        category_id: int,
        subcategory_id: Optional[int],
        frequency: str,
        checklist_items: List[str] = [],
        month: Optional[int] = None,
    ):
        result = TodoModels.create_template(title, notes, category_id, subcategory_id, frequency, month)
        template_id = result["id"]
        for i, text in enumerate(checklist_items):
            if text.strip():
                TodoModels.create_template_checklist_item(template_id, text.strip(), i)
        return result

    @staticmethod
    def add_direct_task(
        title: str, notes: Optional[str], category_id: int, subcategory_id: Optional[int], frequency: str
    ):
        return TodoModels.add_direct_task(title, notes, category_id, subcategory_id, frequency)

    @staticmethod
    def update_template(
        id: int,
        title: str,
        notes: Optional[str],
        category_id: int,
        subcategory_id: Optional[int],
        frequency: str,
        checklist_items: List[str] = [],
        month: Optional[int] = None,
    ):
        TodoModels.update_template(id, title, notes, category_id, subcategory_id, frequency, month)
        TodoModels.delete_template_checklist(id)
        for i, text in enumerate(checklist_items):
            if text.strip():
                TodoModels.create_template_checklist_item(id, text.strip(), i)
        return {"success": True}

    @staticmethod
    def delete_template(id: int):
        return TodoModels.delete_template(id)

    @staticmethod
    def fetch_tasks(category_id: Optional[int] = None, subcategory_id: Optional[int] = None):
        tasks = TodoModels.fetch_tasks(category_id, subcategory_id)
        if tasks:
            task_ids = [t["id"] for t in tasks]
            checklist_items = TodoModels.fetch_checklist_for_tasks(task_ids)
            checklist_map: dict = {}
            for item in checklist_items:
                tid = item["taskId"]
                if tid not in checklist_map:
                    checklist_map[tid] = []
                checklist_map[tid].append({"id": item["id"], "text": item["text"], "checked": bool(item["checked"])})
            for task in tasks:
                task["checklistItems"] = checklist_map.get(task["id"], [])
        return tasks

    @staticmethod
    def add_checklist_item(task_id: int, text: str):
        return TodoModels.add_checklist_item(task_id, text)

    @staticmethod
    def update_checklist_item(item_id: int, text: Optional[str], checked: Optional[bool]):
        return TodoModels.update_checklist_item(item_id, text, checked)

    @staticmethod
    def delete_checklist_item(item_id: int):
        return TodoModels.delete_checklist_item(item_id)

    @staticmethod
    def fetch_history(category_id: Optional[int] = None, subcategory_id: Optional[int] = None):
        return TodoModels.fetch_history(category_id, subcategory_id)

    @staticmethod
    def add_task(template_id: int):
        return TodoModels.add_task(template_id)

    @staticmethod
    def complete_task(id: int):
        return TodoModels.complete_task(id)

    @staticmethod
    def archive_task(id: int):
        return TodoModels.archive_task(id)

    @staticmethod
    def archive_all_completed():
        return TodoModels.archive_all_completed()

    @staticmethod
    def run_automation():
        now = datetime.now()
        day = now.day
        weekday = now.weekday()  # 0 = Monday
        month = now.month

        templates = TodoModels.fetch_templates_for_automation()
        added = 0
        for t in templates:
            freq = t["frequency"]
            if freq == "daily":
                should_trigger = True
            elif freq == "weekly":
                should_trigger = weekday == 0
            elif freq == "monthly":
                should_trigger = day == 1
            elif freq == "quarterly":
                should_trigger = day == 1 and month in (1, 4, 7, 10)
            elif freq == "yearly":
                should_trigger = day == 1 and month == t.get("month")
            else:
                should_trigger = False

            if should_trigger and not TodoModels.task_added_today(t["id"]):
                TodoModels.add_task(t["id"])
                added += 1

        return added

    @staticmethod
    def update_task(id: int, title: str, notes: Optional[str], category_id: int, subcategory_id: Optional[int]):
        return TodoModels.update_task(id, title, notes, category_id, subcategory_id)

    @staticmethod
    def remove_task(id: int):
        return TodoModels.remove_task(id)
