from models.PeopleModels import PeopleModels
from typing import List, Optional


class PeopleServices:
    @staticmethod
    def fetch_people(user_id: int):
        return PeopleModels.fetch_people(user_id)

    @staticmethod
    def create_person(user_id: int, name: str):
        result = PeopleModels.create_person(user_id, name)
        return result["inserted_id"]

    @staticmethod
    def delete_person(person_id: int, user_id: int):
        return PeopleModels.delete_person(person_id, user_id)

    @staticmethod
    def fetch_categories(person_id: int):
        categories = PeopleModels.fetch_categories(person_id)
        subcategories = PeopleModels.fetch_subcategories(person_id)

        result = [
            {
                "id": c["id"],
                "name": c["name"],
                "subcategories": [],
                "ideaCount": PeopleModels.count_active_ideas(c["id"]),
            }
            for c in categories
        ]
        for sub in subcategories:
            cat = next((c for c in result if c["id"] == sub["category_id"]), None)
            if cat is not None:
                cat["subcategories"].append({"id": sub["id"], "name": sub["name"], "categoryId": sub["category_id"]})

        return result

    @staticmethod
    def create_category(person_id: int, name: str, subcategory_names: List[str]):
        result = PeopleModels.create_category(person_id, name)
        category_id = result["inserted_id"]
        for i, sub_name in enumerate(subcategory_names):
            PeopleModels.create_subcategory(person_id, category_id, sub_name, i)
        return category_id

    @staticmethod
    def create_subcategory(person_id: int, category_id: int, name: str):
        return PeopleModels.create_subcategory(person_id, category_id, name)

    @staticmethod
    def update_category(id: int, name: str):
        return PeopleModels.update_category(id, name)

    @staticmethod
    def update_subcategory(id: int, name: str):
        return PeopleModels.update_subcategory(id, name)

    @staticmethod
    def delete_subcategory(id: int):
        return PeopleModels.delete_subcategory(id)

    @staticmethod
    def delete_category(id: int):
        count = PeopleModels.count_active_ideas(id)
        if count > 0:
            raise ValueError(f"Category has {count} active idea(s) and cannot be deleted")
        PeopleModels.delete_category(id)

    @staticmethod
    def fetch_ideas(person_id: int, category_id: Optional[int] = None, subcategory_id: Optional[int] = None):
        return PeopleModels.fetch_ideas(person_id, category_id, subcategory_id)

    @staticmethod
    def create_idea(person_id: int, category_id: int, title: str, notes: Optional[str], subcategory_id: Optional[int]):
        return PeopleModels.create_idea(person_id, category_id, title, notes, subcategory_id)

    @staticmethod
    def update_idea(id: int, title: str, notes: Optional[str], category_id: int, subcategory_id: Optional[int]):
        return PeopleModels.update_idea(id, title, notes, category_id, subcategory_id)

    @staticmethod
    def delete_idea(id: int):
        return PeopleModels.delete_idea(id)
