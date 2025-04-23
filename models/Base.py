import pymysql
from dbutils.pooled_db import PooledDB
from config.config import Config


class Base:
    pool = PooledDB(
        creator=pymysql,
        maxconnections=10,  # Max open connections
        mincached=2,  # Min idle connections in the pool
        maxcached=5,  # Max idle connections in the pool
        blocking=True,  # Wait if pool is full
        setsession=[],  # Session commands if needed
        ping=1,  # Check if connection is alive (0=never, 1=default)
        **Config.get_db_config(),
        cursorclass=pymysql.cursors.DictCursor,
    )

    @staticmethod
    def get_connection():
        return Base.pool.connection()

    @staticmethod
    def custom_insert(query, params=None, connection=None):
        if connection is not None:
            print("Has connection")
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                connection.commit()
                inserted_id = cursor.lastrowid
                print(f"Inserted ID: {inserted_id}")
                return {"inserted_id": inserted_id}
        else:
            conn = Base.get_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    conn.commit()
                    inserted_id = cursor.lastrowid
                    print(f"Inserted ID: {inserted_id}")
                    return {"inserted_id": inserted_id}
            finally:
                conn.close()

    @staticmethod
    def custom_query(query, params=None, connection=None):

        if connection is not None:
            print("Has connection")
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                data = cursor.fetchall()
                print(data)
                return data
        else:
            conn = Base.get_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    data = cursor.fetchall()

                    print(data)
                    return data
            finally:
                conn.close()

    @staticmethod
    def custom_delete(query, params=None, connection=None):
        if connection is not None:
            print("Has connection")
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                connection.commit()
                affected_rows = cursor.rowcount
                print(f"Deleted {affected_rows} row(s)")
                return {"deleted": affected_rows}
        else:
            conn = Base.get_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    conn.commit()
                    affected_rows = cursor.rowcount
                    print(f"Deleted {affected_rows} row(s)")
                    return {"deleted": affected_rows}
            finally:
                conn.close()
