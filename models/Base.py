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
