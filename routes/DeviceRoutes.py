import traceback

from flask import Blueprint, request
from controllers.DeviceControllers import DeviceControllers
from routes.base import format_return, error_return
from lib.auth import check_auth

devices = Blueprint("devices", __name__)
devices.before_request(check_auth)


@devices.route("/", methods=["GET"], strict_slashes=False)
def fetch_devices():
    try:
        data = DeviceControllers.fetch_devices()
        return format_return(data)
    except Exception as e:
        traceback.print_exc()
        print(f"Error fetching devices: {e}")
        return error_return({"error": "Failed to fetch devices"}, 500)


@devices.route("/battery/", methods=["POST"], strict_slashes=False)
def create_battery_log():
    try:
        data = request.get_json()
        DeviceControllers.create_battery_log(data)
        return format_return({"success": True})
    except Exception as e:
        traceback.print_exc()
        print(f"Error creating battery log: {e}")
        return error_return({"error": "Failed to create battery log"}, 500)
