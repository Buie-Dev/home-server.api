from services.MeganServices import MeganServices
from typing import List, Optional


class MeganControllers:
    @staticmethod
    def fetch_categories():
        return MeganServices.fetch_categories()

    @staticmethod
    def create_category(name: str, subcategory_names: List[str]):
        return MeganServices.create_category(name, subcategory_names)

    @staticmethod
    def create_subcategory(category_id: int, name: str):
        return MeganServices.create_subcategory(category_id, name)

    @staticmethod
    def update_category(id: int, name: str):
        return MeganServices.update_category(id, name)

    @staticmethod
    def update_subcategory(id: int, name: str):
        return MeganServices.update_subcategory(id, name)

    @staticmethod
    def delete_subcategory(id: int):
        return MeganServices.delete_subcategory(id)

    @staticmethod
    def delete_category(id: int):
        MeganServices.delete_category(id)

    @staticmethod
    def fetch_ideas(category_id: Optional[int] = None, subcategory_id: Optional[int] = None):
        return MeganServices.fetch_ideas(category_id, subcategory_id)

    @staticmethod
    def create_idea(category_id: int, title: str, notes: Optional[str], subcategory_id: Optional[int]):
        return MeganServices.create_idea(category_id, title, notes, subcategory_id)

    @staticmethod
    def update_idea(id: int, title: str, notes: Optional[str], category_id: int, subcategory_id: Optional[int]):
        return MeganServices.update_idea(id, title, notes, category_id, subcategory_id)

    @staticmethod
    def toggle_idea(id: int, completed: bool):
        return MeganServices.toggle_idea(id, completed)

    @staticmethod
    def delete_idea(id: int):
        return MeganServices.delete_idea(id)
