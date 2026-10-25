import logging

from flask import Blueprint, request

from controllers.DeviceControllers import DeviceControllers
from lib.auth import check_auth
from routes.base import error_return, format_return

logger = logging.getLogger(__name__)

devices = Blueprint("devices", __name__)
devices.before_request(check_auth)


@devices.route("/", methods=["GET"], strict_slashes=False)
def fetch_devices():
    try:
        data = DeviceControllers.fetch_devices()
        return format_return(data)
    except Exception:
        logger.exception("Error fetching devices")
        return error_return({"error": "Failed to fetch devices"}, 500)


@devices.route("/battery/", methods=["POST"], strict_slashes=False)
def create_battery_log():
    try:
        data = request.get_json()
        DeviceControllers.create_battery_log(data)
        return format_return({"success": True})
    except Exception:
        logger.exception("Error creating battery log")
        return error_return({"error": "Failed to create battery log"}, 500)
