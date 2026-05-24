from models.MeganModels import MeganModels
from typing import List, Optional


class MeganServices:

    @staticmethod
    def fetch_categories():
        categories = MeganModels.fetch_categories()
        subcategories = MeganModels.fetch_subcategories()

        result = [
            {
                "id": c["id"],
                "name": c["name"],
                "subcategories": [],
                "ideaCount": MeganModels.count_active_ideas(c["id"]),
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
        result = MeganModels.create_category(name)
        category_id = result["inserted_id"]
        for i, sub_name in enumerate(subcategory_names):
            MeganModels.create_subcategory(category_id, sub_name, i)
        return category_id

    @staticmethod
    def create_subcategory(category_id: int, name: str):
        return MeganModels.create_subcategory(category_id, name)

    @staticmethod
    def update_category(id: int, name: str):
        return MeganModels.update_category(id, name)

    @staticmethod
    def update_subcategory(id: int, name: str):
        return MeganModels.update_subcategory(id, name)

    @staticmethod
    def delete_subcategory(id: int):
        return MeganModels.delete_subcategory(id)

    @staticmethod
    def delete_category(id: int):
        count = MeganModels.count_active_ideas(id)
        if count > 0:
            raise ValueError(f"Category has {count} active idea(s) and cannot be deleted")
        MeganModels.delete_category(id)

    @staticmethod
    def fetch_ideas(category_id: Optional[int] = None, subcategory_id: Optional[int] = None):
        return MeganModels.fetch_ideas(category_id, subcategory_id)

    @staticmethod
    def create_idea(category_id: int, title: str, notes: Optional[str], subcategory_id: Optional[int]):
        return MeganModels.create_idea(category_id, title, notes, subcategory_id)

    @staticmethod
    def update_idea(id: int, title: str, notes: Optional[str], category_id: int, subcategory_id: Optional[int]):
        return MeganModels.update_idea(id, title, notes, category_id, subcategory_id)

    @staticmethod
    def toggle_idea(id: int, completed: bool):
        return MeganModels.toggle_idea(id, completed)

    @staticmethod
    def delete_idea(id: int):
        return MeganModels.delete_idea(id)
