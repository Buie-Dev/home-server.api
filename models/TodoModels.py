from models.Base import Base
from typing import Optional


class TodoModels:
    @staticmethod
    def fetch_categories():
        return Base.custom_query(
            "SELECT id, name FROM todo_categories WHERE deleted_at IS NULL ORDER BY sort_order ASC, name ASC"
        )

    @staticmethod
    def fetch_subcategories():
        return Base.custom_query(
            "SELECT id, category_id, name FROM todo_subcategories WHERE deleted_at IS NULL ORDER BY sort_order ASC, name ASC"
        )

    @staticmethod
    def create_category(name: str, sort_order: int = 0):
        return Base.custom_insert(
            "INSERT INTO todo_categories (name, sort_order) VALUES (%s, %s)",
            (name, sort_order),
        )

    @staticmethod
    def create_subcategory(category_id: int, name: str, sort_order: int = 0):
        return Base.custom_insert(
            "INSERT INTO todo_subcategories (category_id, name, sort_order) VALUES (%s, %s, %s)",
            (category_id, name, sort_order),
        )

    @staticmethod
    def update_category(id: int, name: str):
        return Base.custom_update(
            "UPDATE todo_categories SET name = %s WHERE id = %s",
            (name, id),
        )

    @staticmethod
    def update_subcategory(id: int, name: str):
        return Base.custom_update(
            "UPDATE todo_subcategories SET name = %s WHERE id = %s",
            (name, id),
        )

    @staticmethod
    def delete_subcategory(id: int):
        return Base.custom_update(
            "UPDATE todo_subcategories SET deleted_at = NOW() WHERE id = %s",
            (id,),
        )

    @staticmethod
    def count_active_templates(category_id: int):
        row = Base.single_query(
            "SELECT COUNT(*) AS count FROM todo_templates WHERE category_id = %s AND deleted_at IS NULL",
            (category_id,),
        )
        return row["count"] if row else 0

    @staticmethod
    def delete_category(id: int):
        Base.custom_update(
            "UPDATE todo_subcategories SET deleted_at = NOW() WHERE category_id = %s AND deleted_at IS NULL",
            (id,),
        )
        return Base.custom_update(
            "UPDATE todo_categories SET deleted_at = NOW() WHERE id = %s",
            (id,),
        )

    @staticmethod
    def fetch_templates(category_id: Optional[int] = None, subcategory_id: Optional[int] = None):
        params = []
        sql = """
            SELECT
                t.id,
                t.title,
                t.notes,
                t.frequency,
                t.month,
                t.created_at AS createdAt,
                t.category_id AS categoryId,
                c.name AS categoryName,
                t.subcategory_id AS subcategoryId,
                s.name AS subcategoryName
            FROM todo_templates AS t
            JOIN todo_categories AS c ON t.category_id = c.id
            LEFT JOIN todo_subcategories AS s ON t.subcategory_id = s.id
            WHERE t.deleted_at IS NULL
        """
        if category_id is not None:
            sql += " AND t.category_id = %s"
            params.append(category_id)
        if subcategory_id is not None:
            sql += " AND t.subcategory_id = %s"
            params.append(subcategory_id)
        sql += " ORDER BY t.title ASC"
        return Base.custom_query(sql, params or None)

    @staticmethod
    def fetch_template_checklist(template_ids: list):
        if not template_ids:
            return []
        placeholders = ",".join(["%s"] * len(template_ids))
        return Base.custom_query(
            f"SELECT id, template_id AS templateId, text FROM todo_template_checklist WHERE template_id IN ({placeholders}) AND deleted_at IS NULL ORDER BY sort_order ASC, created_at ASC",
            template_ids,
        )

    @staticmethod
    def create_template_checklist_item(template_id: int, text: str, sort_order: int = 0):
        return Base.custom_insert(
            "INSERT INTO todo_template_checklist (template_id, text, sort_order) VALUES (%s, %s, %s)",
            (template_id, text, sort_order),
        )

    @staticmethod
    def delete_template_checklist(template_id: int):
        return Base.custom_update(
            "UPDATE todo_template_checklist SET deleted_at = NOW() WHERE template_id = %s AND deleted_at IS NULL",
            (template_id,),
        )

    @staticmethod
    def create_template(
        title: str,
        notes: Optional[str],
        category_id: int,
        subcategory_id: Optional[int],
        frequency: str,
        month: Optional[int] = None,
    ):
        result = Base.custom_insert(
            "INSERT INTO todo_templates (title, notes, category_id, subcategory_id, frequency, month) VALUES (%s, %s, %s, %s, %s, %s)",
            (title, notes, category_id, subcategory_id, frequency, month),
        )
        return {"id": result["inserted_id"]}

    @staticmethod
    def add_direct_task(
        title: str, notes: Optional[str], category_id: int, subcategory_id: Optional[int], frequency: str
    ):
        return Base.custom_insert(
            "INSERT INTO todo_tasks (title, notes, frequency, category_id, subcategory_id) VALUES (%s, %s, %s, %s, %s)",
            (title, notes, frequency, category_id, subcategory_id),
        )

    @staticmethod
    def update_template(
        id: int,
        title: str,
        notes: Optional[str],
        category_id: int,
        subcategory_id: Optional[int],
        frequency: str,
        month: Optional[int] = None,
    ):
        return Base.custom_update(
            "UPDATE todo_templates SET title = %s, notes = %s, category_id = %s, subcategory_id = %s, frequency = %s, month = %s WHERE id = %s",
            (title, notes, category_id, subcategory_id, frequency, month, id),
        )

    @staticmethod
    def delete_template(id: int):
        return Base.custom_update(
            "UPDATE todo_templates SET deleted_at = NOW() WHERE id = %s",
            (id,),
        )

    @staticmethod
    def fetch_tasks(category_id: Optional[int] = None, subcategory_id: Optional[int] = None):
        params = []
        sql = """
            SELECT
                ta.id,
                ta.template_id AS templateId,
                ta.completed,
                ta.added_at AS addedAt,
                ta.completed_at AS completedAt,
                ta.title,
                ta.notes,
                ta.frequency,
                ta.category_id AS categoryId,
                c.name AS categoryName,
                ta.subcategory_id AS subcategoryId,
                s.name AS subcategoryName
            FROM todo_tasks AS ta
            JOIN todo_categories AS c ON ta.category_id = c.id
            LEFT JOIN todo_subcategories AS s ON ta.subcategory_id = s.id
            WHERE ta.deleted_at IS NULL AND ta.archived_at IS NULL
        """
        if category_id is not None:
            sql += " AND ta.category_id = %s"
            params.append(category_id)
        if subcategory_id is not None:
            sql += " AND ta.subcategory_id = %s"
            params.append(subcategory_id)
        sql += " ORDER BY ta.completed ASC, ta.added_at DESC"
        return Base.custom_query(sql, params or None)

    @staticmethod
    def fetch_history(category_id: Optional[int] = None, subcategory_id: Optional[int] = None):
        params = []
        sql = """
            SELECT
                ta.id,
                ta.completed_at AS completedAt,
                ta.title,
                ta.frequency,
                ta.category_id AS categoryId,
                c.name AS categoryName,
                ta.subcategory_id AS subcategoryId,
                s.name AS subcategoryName
            FROM todo_tasks AS ta
            JOIN todo_categories AS c ON ta.category_id = c.id
            LEFT JOIN todo_subcategories AS s ON ta.subcategory_id = s.id
            WHERE ta.deleted_at IS NULL AND ta.archived_at IS NOT NULL
        """
        if category_id is not None:
            sql += " AND ta.category_id = %s"
            params.append(category_id)
        if subcategory_id is not None:
            sql += " AND ta.subcategory_id = %s"
            params.append(subcategory_id)
        sql += " ORDER BY ta.completed_at DESC LIMIT 200"
        return Base.custom_query(sql, params or None)

    @staticmethod
    def add_task(template_id: int):
        template = Base.single_query(
            "SELECT title, notes, frequency, category_id, subcategory_id FROM todo_templates WHERE id = %s",
            (template_id,),
        )
        result = Base.custom_insert(
            "INSERT INTO todo_tasks (template_id, title, notes, frequency, category_id, subcategory_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                template_id,
                template["title"],
                template.get("notes"),
                template["frequency"],
                template["category_id"],
                template.get("subcategory_id"),
            ),
        )
        task_id = result["inserted_id"]
        template_checklist = TodoModels.fetch_template_checklist([template_id])
        for item in template_checklist:
            Base.custom_insert(
                "INSERT INTO todo_checklist (task_id, text) VALUES (%s, %s)",
                (task_id, item["text"]),
            )
        return result

    @staticmethod
    def fetch_templates_for_automation():
        return Base.custom_query(
            "SELECT id, frequency, month FROM todo_templates WHERE frequency != 'one_time' AND deleted_at IS NULL"
        )

    @staticmethod
    def task_added_today(template_id: int) -> bool:
        row = Base.single_query(
            "SELECT id FROM todo_tasks WHERE template_id = %s AND deleted_at IS NULL AND completed = 0",
            (template_id,),
        )
        return row is not None

    @staticmethod
    def update_task(id: int, title: str, notes: Optional[str], category_id: int, subcategory_id: Optional[int]):
        return Base.custom_update(
            "UPDATE todo_tasks SET title = %s, notes = %s, category_id = %s, subcategory_id = %s WHERE id = %s",
            (title, notes, category_id, subcategory_id, id),
        )

    @staticmethod
    def complete_task(id: int):
        return Base.custom_update(
            "UPDATE todo_tasks SET completed = 1, completed_at = NOW() WHERE id = %s",
            (id,),
        )

    @staticmethod
    def archive_task(id: int):
        return Base.custom_update(
            "UPDATE todo_tasks SET archived_at = NOW() WHERE id = %s",
            (id,),
        )

    @staticmethod
    def archive_all_completed():
        return Base.custom_update(
            "UPDATE todo_tasks SET archived_at = NOW() WHERE completed = 1 AND archived_at IS NULL AND deleted_at IS NULL",
            None,
        )

    @staticmethod
    def remove_task(id: int):
        return Base.custom_update(
            "UPDATE todo_tasks SET deleted_at = NOW() WHERE id = %s",
            (id,),
        )

    @staticmethod
    def fetch_checklist_for_tasks(task_ids: list):
        if not task_ids:
            return []
        placeholders = ",".join(["%s"] * len(task_ids))
        return Base.custom_query(
            f"SELECT id, task_id AS taskId, text, checked FROM todo_checklist WHERE task_id IN ({placeholders}) AND deleted_at IS NULL ORDER BY created_at ASC",
            task_ids,
        )

    @staticmethod
    def add_checklist_item(task_id: int, text: str):
        result = Base.custom_insert(
            "INSERT INTO todo_checklist (task_id, text) VALUES (%s, %s)",
            (task_id, text),
        )
        return {"id": result["inserted_id"], "taskId": task_id, "text": text, "checked": False}

    @staticmethod
    def update_checklist_item(item_id: int, text: Optional[str], checked: Optional[bool]):
        if text is not None and checked is not None:
            return Base.custom_update(
                "UPDATE todo_checklist SET text = %s, checked = %s WHERE id = %s",
                (text, int(checked), item_id),
            )
        elif text is not None:
            return Base.custom_update(
                "UPDATE todo_checklist SET text = %s WHERE id = %s",
                (text, item_id),
            )
        else:
            return Base.custom_update(
                "UPDATE todo_checklist SET checked = %s WHERE id = %s",
                (int(checked), item_id),
            )

    @staticmethod
    def delete_checklist_item(item_id: int):
        return Base.custom_update(
            "UPDATE todo_checklist SET deleted_at = NOW() WHERE id = %s",
            (item_id,),
        )
