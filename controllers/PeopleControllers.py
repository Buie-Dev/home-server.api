from services.PeopleServices import PeopleServices
from typing import List, Optional


class PeopleControllers:

    @staticmethod
    def fetch_people(user_id: int):
        return PeopleServices.fetch_people(user_id)

    @staticmethod
    def create_person(user_id: int, name: str):
        return PeopleServices.create_person(user_id, name)

    @staticmethod
    def delete_person(person_id: int, user_id: int):
        return PeopleServices.delete_person(person_id, user_id)

    @staticmethod
    def fetch_categories(person_id: int):
        return PeopleServices.fetch_categories(person_id)

    @staticmethod
    def create_category(person_id: int, name: str, subcategory_names: List[str]):
        return PeopleServices.create_category(person_id, name, subcategory_names)

    @staticmethod
    def create_subcategory(person_id: int, category_id: int, name: str):
        return PeopleServices.create_subcategory(person_id, category_id, name)

    @staticmethod
    def update_category(id: int, name: str):
        return PeopleServices.update_category(id, name)

    @staticmethod
    def update_subcategory(id: int, name: str):
        return PeopleServices.update_subcategory(id, name)

    @staticmethod
    def delete_subcategory(id: int):
        return PeopleServices.delete_subcategory(id)

    @staticmethod
    def delete_category(id: int):
        PeopleServices.delete_category(id)

    @staticmethod
    def fetch_ideas(person_id: int, category_id: Optional[int] = None, subcategory_id: Optional[int] = None):
        return PeopleServices.fetch_ideas(person_id, category_id, subcategory_id)

    @staticmethod
    def create_idea(person_id: int, category_id: int, title: str, notes: Optional[str], subcategory_id: Optional[int]):
        return PeopleServices.create_idea(person_id, category_id, title, notes, subcategory_id)

    @staticmethod
    def update_idea(id: int, title: str, notes: Optional[str], category_id: int, subcategory_id: Optional[int]):
        return PeopleServices.update_idea(id, title, notes, category_id, subcategory_id)

    @staticmethod
    def delete_idea(id: int):
        return PeopleServices.delete_idea(id)
