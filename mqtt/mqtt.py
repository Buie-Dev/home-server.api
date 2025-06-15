import json
import paho.mqtt.client as mqtt

from config.config import Config


TOPIC_SUB_HEALTH_CHECK_REQUEST = "healthcheck/request"

TOPIC_PUB_HEALTH_CHECK_RESPONSE = "healthcheck/response"  # Topic to publish to
TOBIC_PUB_ADD_SCHEDULE = "irrigation/schedule/create"
TOBIC_PUB_DELETE_SCHEDULE = "irrigation/schedule/delete"

sub_topics = [TOPIC_SUB_HEALTH_CHECK_REQUEST]
print("--------------------------------")
print(Config)
print(
    "Config.MQTT",
    Config.MQTT_BROKER,
    Config.MQTT_PASSWORD,
    Config.MQTT_PORT,
    Config.MQTT_USERNAME,
)


# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to broker!")
        for topic in sub_topics:
            client.subscribe(topic)  # Subscribe to a topic after connecting
    else:
        print(f"Connection failed with code {rc}")


def health_check_response(client):
    payload = {"device": Config.DEVICE_NAME}
    publish_message(client, TOPIC_PUB_HEALTH_CHECK_RESPONSE, payload)


def publish_message(client, topic, payload, retain=False):
    try:
        message = json.dumps(payload)
        client.publish(topic, message, retain=retain)
        print(f"Published to {topic}: Retain: {retain}: {message}")
    except Exception as e:
        print(f"Error publishing message: {e}")


def publish_add_schedule(client, data):
    publish_message(client, TOBIC_PUB_ADD_SCHEDULE, data, False)


def publish_delete_schedule(client, id):
    publish_message(client, TOBIC_PUB_DELETE_SCHEDULE, {"id": id}, False)


# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    # print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")
    try:
        if msg.topic == TOPIC_SUB_HEALTH_CHECK_REQUEST:
            health_check_response(client)

    except json.JSONDecodeError:
        print(f"Received non-JSON message: {msg.payload.decode()} on topic {msg.topic}")


def create_mqtt_client():
    client = mqtt.Client()
    client.username_pw_set(Config.MQTT_USERNAME, Config.MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    return client


def run_mqtt():
    try:
        client = create_mqtt_client()
        print(f"Connecting to broker {Config.MQTT_BROKER} on port {Config.MQTT_PORT}")
        client.connect(Config.MQTT_BROKER, Config.MQTT_PORT, 60)
        client.loop_start()
        return client

    finally:
        pass
