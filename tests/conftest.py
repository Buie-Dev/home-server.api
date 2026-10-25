import sys
from unittest.mock import MagicMock, patch

# Mock Config before any app code imports it
mock_config = MagicMock()
mock_config.API_MYSQL_HOST = "localhost"
mock_config.API_MYSQL_USERNAME = "testuser"
mock_config.API_MYSQL_PASSWORD = "testpass"
mock_config.API_MYSQL_DATABASE = "testdb"
mock_config.API_PORT = "3306"
mock_config.MQTT_BROKER = "localhost"
mock_config.MQTT_PORT = 1883
mock_config.MQTT_USERNAME = "mqttuser"
mock_config.MQTT_PASSWORD = "mqttpass"
mock_config.DEVICE_NAME = "test-device"
mock_config.JWT_SECRET = "test-secret"
mock_config.APP_USERNAME = "admin"
mock_config.APP_PASSWORD_HASH = "$2b$12$fakehash"
mock_config.get_db_config.return_value = {
    "host": "localhost",
    "user": "testuser",
    "password": "testpass",
    "database": "testdb",
    "port": 3306,
}

# Patch config module before anything imports it
config_module = MagicMock()
config_module.Config = mock_config
sys.modules["config.config"] = config_module

# Mock the database pool so Base doesn't try to connect
mock_pool = MagicMock()
mock_pooled_db = MagicMock(return_value=mock_pool)
patch("dbutils.pooled_db.PooledDB", mock_pooled_db).start()

# Mock run_mqtt so IrrigationControllers doesn't try to connect at import time
mock_mqtt_module = MagicMock()
mock_mqtt_client = MagicMock()
mock_mqtt_module.run_mqtt.return_value = mock_mqtt_client
sys.modules["mqtt.mqtt"] = mock_mqtt_module

# Re-export the real functions we need for mqtt tests
import importlib

_real_mqtt_path = "/".join(__file__.split("/")[:-2]) + "/mqtt/mqtt.py"

import pytest

from index import app as flask_app

# Now that the app is imported, restore the real mqtt module for direct mqtt tests
del sys.modules["mqtt.mqtt"]


@pytest.fixture
def app():
    flask_app.config["TESTING"] = True
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_token():
    from lib.auth import create_token

    return create_token(1, "testuser")
