from models.EventModels import EventModels
from typing import List, Optional


class EventServices:

    @staticmethod
    def fetch_categories():
        categories = EventModels.fetch_categories()
        subcategories = EventModels.fetch_subcategories()
        result = [
            {
                "id": c["id"],
                "name": c["name"],
                "subcategories": [],
                "itemCount": EventModels.count_events_in_category(c["id"]),
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
        result = EventModels.create_category(name)
        category_id = result["inserted_id"]
        for i, sub_name in enumerate(subcategory_names):
            EventModels.create_subcategory(category_id, sub_name, i)
        return category_id

    @staticmethod
    def create_subcategory(category_id: int, name: str):
        return EventModels.create_subcategory(category_id, name)

    @staticmethod
    def update_category(id: int, name: str):
        return EventModels.update_category(id, name)

    @staticmethod
    def update_subcategory(id: int, name: str):
        return EventModels.update_subcategory(id, name)

    @staticmethod
    def delete_subcategory(id: int):
        return EventModels.delete_subcategory(id)

    @staticmethod
    def delete_category(id: int):
        count = EventModels.count_events_in_category(id)
        if count > 0:
            raise ValueError(f"Category has {count} event(s) and cannot be deleted")
        EventModels.delete_category(id)

    @staticmethod
    def fetch_events(category_id: Optional[int] = None, subcategory_id: Optional[int] = None, month: Optional[int] = None, year: Optional[int] = None):
        rows = EventModels.fetch_events(category_id, subcategory_id, month, year)
        return [
            {
                "id": r["id"],
                "title": r["title"],
                "description": r["description"],
                "date": str(r["date"]),
                "time": str(r["time"]) if r["time"] else None,
                "categoryId": r["categoryId"],
                "categoryName": r["categoryName"],
                "subcategoryId": r["subcategoryId"],
                "subcategoryName": r["subcategoryName"],
            }
            for r in rows
        ]

    @staticmethod
    def create_event(title: str, description: Optional[str], date: str, time: Optional[str], category_id: int, subcategory_id: Optional[int]):
        return EventModels.create_event(title, description, date, time, category_id, subcategory_id)

    @staticmethod
    def update_event(id: int, title: str, description: Optional[str], date: str, time: Optional[str], category_id: int, subcategory_id: Optional[int]):
        return EventModels.update_event(id, title, description, date, time, category_id, subcategory_id)

    @staticmethod
    def delete_event(id: int):
        return EventModels.delete_event(id)
