from models.Base import Base
from typing import Optional


class MeganModels:
    @staticmethod
    def fetch_categories():
        return Base.custom_query(
            "SELECT id, name FROM megan_categories WHERE deleted_at IS NULL ORDER BY sort_order ASC, name ASC"
        )

    @staticmethod
    def fetch_subcategories():
        return Base.custom_query(
            "SELECT id, category_id, name FROM megan_subcategories WHERE deleted_at IS NULL ORDER BY sort_order ASC, name ASC"
        )

    @staticmethod
    def create_category(name: str, sort_order: int = 0):
        return Base.custom_insert(
            "INSERT INTO megan_categories (name, sort_order) VALUES (%s, %s)",
            (name, sort_order),
        )

    @staticmethod
    def create_subcategory(category_id: int, name: str, sort_order: int = 0):
        return Base.custom_insert(
            "INSERT INTO megan_subcategories (category_id, name, sort_order) VALUES (%s, %s, %s)",
            (category_id, name, sort_order),
        )

    @staticmethod
    def count_active_ideas(category_id: int):
        row = Base.single_query(
            "SELECT COUNT(*) AS count FROM megan_ideas WHERE category_id = %s AND deleted_at IS NULL",
            (category_id,),
        )
        return row["count"] if row else 0

    @staticmethod
    def update_category(id: int, name: str):
        return Base.custom_update(
            "UPDATE megan_categories SET name = %s WHERE id = %s",
            (name, id),
        )

    @staticmethod
    def update_subcategory(id: int, name: str):
        return Base.custom_update(
            "UPDATE megan_subcategories SET name = %s WHERE id = %s",
            (name, id),
        )

    @staticmethod
    def delete_subcategory(id: int):
        return Base.custom_update(
            "UPDATE megan_subcategories SET deleted_at = NOW() WHERE id = %s",
            (id,),
        )

    @staticmethod
    def delete_category(id: int):
        Base.custom_update(
            "UPDATE megan_subcategories SET deleted_at = NOW() WHERE category_id = %s AND deleted_at IS NULL",
            (id,),
        )
        return Base.custom_update(
            "UPDATE megan_categories SET deleted_at = NOW() WHERE id = %s",
            (id,),
        )

    @staticmethod
    def fetch_ideas(category_id: Optional[int] = None, subcategory_id: Optional[int] = None):
        params = []
        sql = """
            SELECT
                i.id,
                i.title,
                i.notes,
                i.completed,
                i.created_at AS createdAt,
                i.category_id AS categoryId,
                c.name AS categoryName,
                i.subcategory_id AS subcategoryId,
                s.name AS subcategoryName
            FROM megan_ideas AS i
            JOIN megan_categories AS c ON i.category_id = c.id
            LEFT JOIN megan_subcategories AS s ON i.subcategory_id = s.id
            WHERE i.deleted_at IS NULL
        """
        if category_id is not None:
            sql += " AND i.category_id = %s"
            params.append(category_id)
        if subcategory_id is not None:
            sql += " AND i.subcategory_id = %s"
            params.append(subcategory_id)
        sql += " ORDER BY c.sort_order ASC, i.created_at DESC"
        return Base.custom_query(sql, params or None)

    @staticmethod
    def create_idea(category_id: int, title: str, notes: Optional[str], subcategory_id: Optional[int]):
        return Base.custom_insert(
            "INSERT INTO megan_ideas (category_id, subcategory_id, title, notes) VALUES (%s, %s, %s, %s)",
            (category_id, subcategory_id, title, notes),
        )

    @staticmethod
    def update_idea(id: int, title: str, notes: Optional[str], category_id: int, subcategory_id: Optional[int]):
        return Base.custom_update(
            "UPDATE megan_ideas SET title = %s, notes = %s, category_id = %s, subcategory_id = %s WHERE id = %s",
            (title, notes, category_id, subcategory_id, id),
        )

    @staticmethod
    def toggle_idea(id: int, completed: bool):
        return Base.custom_update(
            "UPDATE megan_ideas SET completed = %s WHERE id = %s",
            (1 if completed else 0, id),
        )

    @staticmethod
    def delete_idea(id: int):
        return Base.custom_update(
            "UPDATE megan_ideas SET deleted_at = NOW() WHERE id = %s",
            (id,),
        )
