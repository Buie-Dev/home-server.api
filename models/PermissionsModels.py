from models.Base import Base

PAGES = ['irrigation', 'rowing', 'people', 'todo', 'events', 'devices', 'admin']


class PermissionsModels:

    @staticmethod
    def fetch_user_pages(user_id: int) -> list:
        row = Base.single_query(
            "SELECT irrigation, rowing, people, todo, events, devices, admin FROM user_permissions WHERE user_id = %s",
            (user_id,),
        )
        if not row:
            return []
        return [page for page in PAGES if row.get(page)]

    @staticmethod
    def fetch_all_users_with_permissions() -> list:
        users = Base.custom_query("SELECT id, username FROM users ORDER BY username ASC")
        result = []
        for user in users:
            row = Base.single_query(
                "SELECT irrigation, rowing, people, todo, events, devices, admin FROM user_permissions WHERE user_id = %s",
                (user["id"],),
            )
            perms = {page: bool(row.get(page, False)) for page in PAGES} if row else {page: False for page in PAGES}
            result.append({"id": user["id"], "username": user["username"], "permissions": perms})
        return result

    @staticmethod
    def set_user_permissions(user_id: int, permissions: dict):
        vals = tuple(bool(permissions.get(page, False)) for page in PAGES)
        existing = Base.single_query(
            "SELECT user_id FROM user_permissions WHERE user_id = %s", (user_id,)
        )
        if existing:
            Base.custom_update(
                """UPDATE user_permissions
                   SET irrigation=%s, rowing=%s, people=%s, todo=%s, events=%s, devices=%s, admin=%s
                   WHERE user_id=%s""",
                (*vals, user_id),
            )
        else:
            Base.custom_insert(
                """INSERT INTO user_permissions (user_id, irrigation, rowing, people, todo, events, devices, admin)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (user_id, *vals),
            )
