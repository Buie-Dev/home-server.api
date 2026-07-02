from models.Base import Base
from typing import Optional


class EventModels:

    @staticmethod
    def fetch_categories():
        return Base.custom_query(
            "SELECT id, name FROM event_categories WHERE deleted_at IS NULL ORDER BY sort_order ASC, name ASC"
        )

    @staticmethod
    def fetch_subcategories():
        return Base.custom_query(
            "SELECT id, category_id, name FROM event_subcategories WHERE deleted_at IS NULL ORDER BY sort_order ASC, name ASC"
        )

    @staticmethod
    def count_events_in_category(category_id: int):
        row = Base.single_query(
            "SELECT COUNT(*) AS count FROM events WHERE category_id = %s AND deleted_at IS NULL",
            (category_id,),
        )
        return row["count"] if row else 0

    @staticmethod
    def create_category(name: str, sort_order: int = 0):
        return Base.custom_insert(
            "INSERT INTO event_categories (name, sort_order) VALUES (%s, %s)",
            (name, sort_order),
        )

    @staticmethod
    def create_subcategory(category_id: int, name: str, sort_order: int = 0):
        return Base.custom_insert(
            "INSERT INTO event_subcategories (category_id, name, sort_order) VALUES (%s, %s, %s)",
            (category_id, name, sort_order),
        )

    @staticmethod
    def update_category(id: int, name: str):
        return Base.custom_update(
            "UPDATE event_categories SET name = %s WHERE id = %s",
            (name, id),
        )

    @staticmethod
    def update_subcategory(id: int, name: str):
        return Base.custom_update(
            "UPDATE event_subcategories SET name = %s WHERE id = %s",
            (name, id),
        )

    @staticmethod
    def delete_subcategory(id: int):
        return Base.custom_update(
            "UPDATE event_subcategories SET deleted_at = NOW() WHERE id = %s",
            (id,),
        )

    @staticmethod
    def delete_category(id: int):
        Base.custom_update(
            "UPDATE event_subcategories SET deleted_at = NOW() WHERE category_id = %s AND deleted_at IS NULL",
            (id,),
        )
        return Base.custom_update(
            "UPDATE event_categories SET deleted_at = NOW() WHERE id = %s",
            (id,),
        )

    @staticmethod
    def fetch_events(category_id: Optional[int] = None, subcategory_id: Optional[int] = None, month: Optional[int] = None, year: Optional[int] = None):
        params = []
        sql = """
            SELECT
                e.id,
                e.title,
                e.description,
                e.date,
                e.time,
                e.category_id AS categoryId,
                c.name AS categoryName,
                e.subcategory_id AS subcategoryId,
                s.name AS subcategoryName
            FROM events AS e
            JOIN event_categories AS c ON e.category_id = c.id
            LEFT JOIN event_subcategories AS s ON e.subcategory_id = s.id
            WHERE e.deleted_at IS NULL
        """
        if category_id is not None:
            sql += " AND e.category_id = %s"
            params.append(category_id)
        if subcategory_id is not None:
            sql += " AND e.subcategory_id = %s"
            params.append(subcategory_id)
        if month is not None:
            sql += " AND MONTH(e.date) = %s"
            params.append(month)
        if year is not None:
            sql += " AND YEAR(e.date) = %s"
            params.append(year)
        sql += " ORDER BY e.date ASC, e.time ASC"
        return Base.custom_query(sql, params or None)

    @staticmethod
    def create_event(title: str, description: Optional[str], date: str, time: Optional[str], category_id: int, subcategory_id: Optional[int]):
        return Base.custom_insert(
            "INSERT INTO events (title, description, date, time, category_id, subcategory_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (title, description, date, time, category_id, subcategory_id),
        )

    @staticmethod
    def update_event(id: int, title: str, description: Optional[str], date: str, time: Optional[str], category_id: int, subcategory_id: Optional[int]):
        return Base.custom_update(
            "UPDATE events SET title = %s, description = %s, date = %s, time = %s, category_id = %s, subcategory_id = %s WHERE id = %s",
            (title, description, date, time, category_id, subcategory_id, id),
        )

    @staticmethod
    def delete_event(id: int):
        return Base.custom_update(
            "UPDATE events SET deleted_at = NOW() WHERE id = %s",
            (id,),
        )
