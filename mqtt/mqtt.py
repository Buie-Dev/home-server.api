import json
import logging
import time
import paho.mqtt.client as mqtt

from config.config import Config

logger = logging.getLogger(__name__)

TOPIC_SUB_HEALTH_CHECK_REQUEST = "healthcheck/request"

TOPIC_PUB_HEALTH_CHECK_RESPONSE = "healthcheck/response"
TOBIC_PUB_ADD_SCHEDULE = "irrigation/schedule/create"
TOBIC_PUB_DELETE_SCHEDULE = "irrigation/schedule/delete"

sub_topics = [TOPIC_SUB_HEALTH_CHECK_REQUEST]

logger.info("Config.MQTT %s %s %s %s", Config.MQTT_BROKER, Config.MQTT_PASSWORD, Config.MQTT_PORT, Config.MQTT_USERNAME)


# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected successfully to broker!")
        for topic in sub_topics:
            client.subscribe(topic)
    else:
        logger.error("Connection failed with code %s", rc)


def on_disconnect(client, userdata, rc):
    if rc != 0:
        logger.warning("Unexpected disconnection from broker (rc=%s)", rc)


def health_check_response(client):
    payload = {"device": Config.DEVICE_NAME}
    publish_message(client, TOPIC_PUB_HEALTH_CHECK_RESPONSE, payload)


def publish_message(client, topic, payload, retain=False):
    try:
        message = json.dumps(payload)
        result = client.publish(topic, message, retain=retain)
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            logger.error("Failed to publish to %s: rc=%s (client may be disconnected)", topic, result.rc)
        else:
            logger.info("Published to %s: Retain: %s: %s", topic, retain, message)
    except Exception as e:
        logger.error("Error publishing message: %s", e)


def publish_add_schedule(client, data):
    publish_message(client, TOBIC_PUB_ADD_SCHEDULE, data, False)


def publish_delete_schedule(client, id):
    publish_message(client, TOBIC_PUB_DELETE_SCHEDULE, {"id": id}, False)


# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    try:
        if msg.topic == TOPIC_SUB_HEALTH_CHECK_REQUEST:
            health_check_response(client)

    except json.JSONDecodeError:
        logger.warning("Received non-JSON message: %s on topic %s", msg.payload.decode(), msg.topic)


def create_mqtt_client():
    client = mqtt.Client()
    client.username_pw_set(Config.MQTT_USERNAME, Config.MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.reconnect_delay_set(min_delay=1, max_delay=30)
    return client


def run_mqtt():
    client = create_mqtt_client()
    delay = 1
    while True:
        try:
            logger.info("Connecting to broker %s on port %s", Config.MQTT_BROKER, Config.MQTT_PORT)
            client.connect(Config.MQTT_BROKER, Config.MQTT_PORT, 60)
            client.loop_start()
            return client
        except Exception as e:
            logger.error("Failed to connect to broker: %s. Retrying in %ss...", e, delay)
            time.sleep(delay)
            delay = min(delay * 2, 30)
