from services.TodoServices import TodoServices
from typing import List, Optional


class TodoControllers:

    @staticmethod
    def fetch_categories():
        return TodoServices.fetch_categories()

    @staticmethod
    def create_category(name: str, subcategory_names: List[str]):
        return TodoServices.create_category(name, subcategory_names)

    @staticmethod
    def create_subcategory(category_id: int, name: str):
        return TodoServices.create_subcategory(category_id, name)

    @staticmethod
    def update_category(id: int, name: str):
        return TodoServices.update_category(id, name)

    @staticmethod
    def update_subcategory(id: int, name: str):
        return TodoServices.update_subcategory(id, name)

    @staticmethod
    def delete_subcategory(id: int):
        return TodoServices.delete_subcategory(id)

    @staticmethod
    def delete_category(id: int):
        TodoServices.delete_category(id)

    @staticmethod
    def fetch_templates(category_id: Optional[int] = None, subcategory_id: Optional[int] = None):
        return TodoServices.fetch_templates(category_id, subcategory_id)

    @staticmethod
    def create_template(title: str, notes: Optional[str], category_id: int, subcategory_id: Optional[int], frequency: str, checklist_items: list = []):
        return TodoServices.create_template(title, notes, category_id, subcategory_id, frequency, checklist_items)

    @staticmethod
    def add_direct_task(title: str, notes: Optional[str], category_id: int, subcategory_id: Optional[int], frequency: str):
        return TodoServices.add_direct_task(title, notes, category_id, subcategory_id, frequency)

    @staticmethod
    def update_template(id: int, title: str, notes: Optional[str], category_id: int, subcategory_id: Optional[int], frequency: str, checklist_items: list = []):
        return TodoServices.update_template(id, title, notes, category_id, subcategory_id, frequency, checklist_items)

    @staticmethod
    def delete_template(id: int):
        return TodoServices.delete_template(id)

    @staticmethod
    def fetch_tasks(category_id: Optional[int] = None, subcategory_id: Optional[int] = None):
        return TodoServices.fetch_tasks(category_id, subcategory_id)

    @staticmethod
    def fetch_history(category_id: Optional[int] = None, subcategory_id: Optional[int] = None):
        return TodoServices.fetch_history(category_id, subcategory_id)

    @staticmethod
    def add_task(template_id: int):
        return TodoServices.add_task(template_id)

    @staticmethod
    def complete_task(id: int):
        return TodoServices.complete_task(id)

    @staticmethod
    def remove_task(id: int):
        return TodoServices.remove_task(id)

    @staticmethod
    def add_checklist_item(task_id: int, text: str):
        return TodoServices.add_checklist_item(task_id, text)

    @staticmethod
    def update_checklist_item(item_id: int, text: Optional[str], checked: Optional[bool]):
        return TodoServices.update_checklist_item(item_id, text, checked)

    @staticmethod
    def delete_checklist_item(item_id: int):
        return TodoServices.delete_checklist_item(item_id)
