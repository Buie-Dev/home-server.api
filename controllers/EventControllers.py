from services.EventServices import EventServices
from typing import List, Optional


class EventControllers:
    @staticmethod
    def fetch_categories():
        return EventServices.fetch_categories()

    @staticmethod
    def create_category(name: str, subcategory_names: List[str]):
        return EventServices.create_category(name, subcategory_names)

    @staticmethod
    def create_subcategory(category_id: int, name: str):
        return EventServices.create_subcategory(category_id, name)

    @staticmethod
    def update_category(id: int, name: str):
        return EventServices.update_category(id, name)

    @staticmethod
    def update_subcategory(id: int, name: str):
        return EventServices.update_subcategory(id, name)

    @staticmethod
    def delete_subcategory(id: int):
        return EventServices.delete_subcategory(id)

    @staticmethod
    def delete_category(id: int):
        EventServices.delete_category(id)

    @staticmethod
    def fetch_events(
        category_id: Optional[int] = None,
        subcategory_id: Optional[int] = None,
        month: Optional[int] = None,
        year: Optional[int] = None,
    ):
        return EventServices.fetch_events(category_id, subcategory_id, month, year)

    @staticmethod
    def create_event(
        title: str,
        description: Optional[str],
        date: str,
        time: Optional[str],
        category_id: int,
        subcategory_id: Optional[int],
    ):
        return EventServices.create_event(title, description, date, time, category_id, subcategory_id)

    @staticmethod
    def update_event(
        id: int,
        title: str,
        description: Optional[str],
        date: str,
        time: Optional[str],
        category_id: int,
        subcategory_id: Optional[int],
    ):
        return EventServices.update_event(id, title, description, date, time, category_id, subcategory_id)

    @staticmethod
    def delete_event(id: int):
        return EventServices.delete_event(id)
