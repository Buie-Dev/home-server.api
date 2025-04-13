import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Config:
    API_MYSQL_HOST = os.getenv("API_MYSQL_HOST")  # Default to "localhost" if not found
    API_MYSQL_USERNAME = os.getenv("API_MYSQL_USERNAME")
    API_MYSQL_PASSWORD = os.getenv("API_MYSQL_PASSWORD")
    API_MYSQL_DATABASE = os.getenv("API_MYSQL_DATABASE")
    API_PORT = os.getenv("API_PORT")

    @staticmethod
    def get_db_config():
        print(
            {
                "host": Config.API_MYSQL_HOST,
                "user": Config.API_MYSQL_USERNAME,
                "password": Config.API_MYSQL_PASSWORD,
                "database": Config.API_MYSQL_DATABASE,
            }
        )
        return {
            "host": Config.API_MYSQL_HOST,
            "user": Config.API_MYSQL_USERNAME,
            "password": Config.API_MYSQL_PASSWORD,
            "database": Config.API_MYSQL_DATABASE,
            "port": int(Config.API_PORT),
        }
