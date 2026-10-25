import json
from unittest.mock import MagicMock, patch

from mqtt.mqtt import (
    TOBIC_PUB_ADD_SCHEDULE,
    TOBIC_PUB_DELETE_SCHEDULE,
    TOPIC_PUB_HEALTH_CHECK_RESPONSE,
    TOPIC_PUB_SCHEDULE_STATUS_REQUEST,
    TOPIC_SUB_HEALTH_CHECK_REQUEST,
    TOPIC_SUB_SCHEDULE_STATUS_RESPONSE,
    health_check_response,
    on_connect,
    on_message,
    publish_add_schedule,
    publish_delete_schedule,
    publish_message,
    request_schedule_status,
)


class TestOnConnect:
    def test_subscribes_to_topics_on_success(self):
        client = MagicMock()
        on_connect(client, None, None, 0)

        subscribed = [call[0][0] for call in client.subscribe.call_args_list]
        assert TOPIC_SUB_HEALTH_CHECK_REQUEST in subscribed
        assert TOPIC_SUB_SCHEDULE_STATUS_RESPONSE in subscribed

    def test_does_not_subscribe_on_failure(self):
        client = MagicMock()
        on_connect(client, None, None, 1)

        client.subscribe.assert_not_called()


class TestOnMessage:
    def _make_msg(self, topic, payload):
        msg = MagicMock()
        msg.topic = topic
        msg.payload = json.dumps(payload).encode() if isinstance(payload, dict) else payload.encode()
        return msg

    @patch("mqtt.mqtt.health_check_response")
    def test_healthcheck_request_triggers_response(self, mock_hc):
        client = MagicMock()
        msg = self._make_msg(TOPIC_SUB_HEALTH_CHECK_REQUEST, "ping")

        on_message(client, None, msg)

        mock_hc.assert_called_once_with(client)

    @patch("mqtt.mqtt._status_event")
    def test_schedule_status_response_stores_schedules(self, mock_event):
        import mqtt.mqtt as mqtt_mod

        client = MagicMock()
        schedules = [{"id": 1}, {"id": 2}]
        msg = self._make_msg(TOPIC_SUB_SCHEDULE_STATUS_RESPONSE, {"schedules": schedules})

        on_message(client, None, msg)

        assert mqtt_mod._latest_status_schedules == schedules
        mock_event.set.assert_called_once()


class TestPublishMessage:
    def test_publishes_json_payload(self):
        client = MagicMock()
        result = MagicMock()
        result.rc = 0
        client.publish.return_value = result

        publish_message(client, "test/topic", {"key": "value"})

        client.publish.assert_called_once_with("test/topic", '{"key": "value"}', retain=False)

    def test_publishes_with_retain(self):
        client = MagicMock()
        result = MagicMock()
        result.rc = 0
        client.publish.return_value = result

        publish_message(client, "test/topic", {"key": "value"}, retain=True)

        client.publish.assert_called_once_with("test/topic", '{"key": "value"}', retain=True)


class TestHealthCheckResponse:
    def test_publishes_device_name(self):
        client = MagicMock()
        result = MagicMock()
        result.rc = 0
        client.publish.return_value = result

        health_check_response(client)

        call_args = client.publish.call_args
        assert call_args[0][0] == TOPIC_PUB_HEALTH_CHECK_RESPONSE
        payload = json.loads(call_args[0][1])
        assert payload["device"] == "test-device"


class TestPublishHelpers:
    def test_publish_add_schedule(self):
        client = MagicMock()
        result = MagicMock()
        result.rc = 0
        client.publish.return_value = result

        publish_add_schedule(client, {"id": 1, "name": "Test"})

        assert client.publish.call_args[0][0] == TOBIC_PUB_ADD_SCHEDULE

    def test_publish_delete_schedule(self):
        client = MagicMock()
        result = MagicMock()
        result.rc = 0
        client.publish.return_value = result

        publish_delete_schedule(client, 42)

        assert client.publish.call_args[0][0] == TOBIC_PUB_DELETE_SCHEDULE
        payload = json.loads(client.publish.call_args[0][1])
        assert payload["id"] == 42


class TestRequestScheduleStatus:
    def test_clears_state_and_publishes(self):
        import mqtt.mqtt as mqtt_mod

        client = MagicMock()
        result = MagicMock()
        result.rc = 0
        client.publish.return_value = result

        mqtt_mod._latest_status_schedules = [{"old": "data"}]

        with patch.object(mqtt_mod._status_event, "clear") as mock_clear:
            request_schedule_status(client)

        assert mqtt_mod._latest_status_schedules is None
        mock_clear.assert_called_once()
        assert client.publish.call_args[0][0] == TOPIC_PUB_SCHEDULE_STATUS_REQUEST
