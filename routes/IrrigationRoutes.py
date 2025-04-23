from typing import Any, Dict, List, Optional
from ObjectTypes import Zone
import traceback

from flask import Blueprint, Flask, jsonify, request

from controllers.IrrigationControllers import IrrigationControllers
from routes.base import format_return, error_return

irrigation = Blueprint("irrigation", __name__)


@irrigation.route("/schedules", methods=["GET"])
def schedules() -> Any:
    data = IrrigationControllers.schedules()
    print(data)
    return format_return(data)


@irrigation.route("/schedules", methods=["PUT"])
def create_schedule() -> Any:
    data = request.get_json()
    print(data)
    print("0-0-0-0-0-0------")
    params = {
        "duration": data["duration"],
        "name": data["name"],
        "start_time": data["startTime"],
        "monday": data["monday"],
        "tuesday": data["tuesday"],
        "wednesday": data["wednesday"],
        "thursday": data["thursday"],
        "friday": data["friday"],
        "saturday": data["saturday"],
        "sunday": data["sunday"],
    }
    IrrigationControllers.create_schedule(params)

    return format_return({"Success": True})


@irrigation.route("/schedules/<int:id>", methods=["DELETE"])
def delete_schedule(id: int) -> Any:
    IrrigationControllers.delete_schedule(id)
    return format_return({"Success": True})


@irrigation.route("/zones", methods=["GET"])
def fetch_zones() -> List[Zone]:
    print("Fetching Zones")
    try:
        print("Fetching Zones")
        data = IrrigationControllers.fetch_zones()
        print(data)
        return format_return(data)
    except Exception as e:
        traceback.print_exc()
        print(f"Error fetching zones: {e}")
        return error_return({"error": "Failed to fetch all zones"}, 500)
