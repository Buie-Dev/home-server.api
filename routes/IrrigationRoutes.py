from typing import Any, Dict, List, Optional
from ObjectTypes import Zone

from flask import Blueprint, Flask, jsonify, request

from controllers.IrrigationControllers import IrrigationControllers
from routes.base import format_return, error_return

irrigation = Blueprint("irrigation", __name__)


# @irrigation.route("/schedules", methods=["GET"])
# def schedules() -> Any:
#     data = IrrigationControllers.schedules()
#     print(data)
#     return formatReturn(data)


@irrigation.route("/zones", methods=["GET"])
def fetch_zones() -> List[Zone]:
    print("Fetching Zones")
    try:
        print("Fetching Zones")
        data = IrrigationControllers.fetch_zones()
        print(data)
        return format_return(data)
    except Exception as e:
        print(f"Error fetching zones: {e}")
        return error_return({"error": "Failed to fetch all zones"}, 500)
