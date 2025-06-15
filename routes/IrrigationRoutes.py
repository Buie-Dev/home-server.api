from typing import Any, Dict, List, Optional
from ObjectTypes import Zone
import traceback
import json

from flask import Blueprint, Flask, jsonify, request
from controllers.IrrigationControllers import IrrigationControllers
from routes.base import format_return, error_return

irrigation = Blueprint("irrigation", __name__)


@irrigation.route("/schedules", methods=["GET"])
def schedules() -> Any:
    try:
        data = IrrigationControllers.schedules()
        return format_return(data)
    except Exception as e:
        traceback.print_exc()
        print(f"Error fetching schedules: {e}")
        return error_return({"error": "Failed to fetch schedules"}, 500)


@irrigation.route("/schedules", methods=["PUT"])
def create_schedule() -> Any:
    try:
        data = request.get_json()

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
            "zone_id": data["zoneId"],
            "subzone_ids": data.get("subzoneIds", []),
        }

        IrrigationControllers.create_schedule(params)

        return format_return({"Success": True})
    except Exception as e:
        traceback.print_exc()
        print(f"Error creating schedule: {e}")
        return error_return({"error": "Failed to create schedule"}, 500)


@irrigation.route("/schedules/<int:id>/toggle", methods=["POST"])
def toggle_schedule(id: int) -> Any:
    try:
        data = request.get_json()
        IrrigationControllers.toggle_schedule(id, data)
        return format_return({"Success": True})
    except Exception as e:
        traceback.print_exc()
        print(f"Error updating schedule: {e}")
        return error_return({"error": "Failed to update schedule"}, 500)


@irrigation.route("/schedules/<int:id>", methods=["DELETE"])
def delete_schedule(id: int) -> Any:
    try:
        IrrigationControllers.delete_schedule(id)
        return format_return({"Success": True})
    except Exception as e:
        traceback.print_exc()
        print(f"Error deleting schedule: {e}")
        return error_return({"error": "Failed to delete schedule"}, 500)


@irrigation.route("/schedules/automation", methods=["GET"])
def fetch_automation_schedules() -> Any:
    try:
        data = IrrigationControllers.fetch_automation_schedules()
        return format_return(data)
    except Exception as e:
        traceback.print_exc()
        print(f"Error fetching automation schedules: {e}")
        return error_return({"error": "Failed to fetch automation schedules"}, 500)


@irrigation.route("/zones", methods=["GET"])
def fetch_zones() -> Any:
    try:
        zone_type_id = request.args.get("zoneTypeId", type=int, default=None)
        data = IrrigationControllers.fetch_zones(zone_type_id)
        return format_return(data)
    except Exception as e:
        traceback.print_exc()
        print(f"Error fetching zones: {e}")
        return error_return({"error": "Failed to fetch all zones"}, 500)


@irrigation.route("/zones/types", methods=["GET"])
def fetch_zone_types() -> Any:
    try:
        data = IrrigationControllers.fetch_zone_types()
        return format_return(data)
    except Exception as e:
        traceback.print_exc()
        print(f"Error fetching zone types: {e}")
        return error_return({"error": "Failed to fetch zone types"}, 500)
