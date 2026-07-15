from models.Base import Base


class UserModels:

    @staticmethod
    def fetch_by_username(username: str):
        return Base.single_query(
            "SELECT id, username, password_hash FROM users WHERE username = %s AND deleted_at IS NULL",
            (username,),
        )

    @staticmethod
    def fetch_by_id(user_id: int):
        return Base.single_query(
            "SELECT id, username FROM users WHERE id = %s AND deleted_at IS NULL",
            (user_id,),
        )

    @staticmethod
    def fetch_by_username_or_id(user_id: int):
        return Base.single_query(
            "SELECT id, username FROM users WHERE id = %s AND deleted_at IS NULL",
            (user_id,),
        )

    @staticmethod
    def soft_delete_user(user_id: int):
        return Base.custom_update(
            "UPDATE users SET deleted_at = NOW(), username = CONCAT(username, '__deleted__', id) WHERE id = %s AND deleted_at IS NULL",
            (user_id,),
        )

    @staticmethod
    def create_user(username: str, password_hash: str) -> int:
        return Base.custom_insert(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, password_hash),
        )

    @staticmethod
    def update_password(username: str, new_hash: str):
        return Base.custom_update(
            "UPDATE users SET password_hash = %s WHERE username = %s",
            (new_hash, username),
        )
