import logging
import traceback
from typing import Any

from flask import Blueprint, request

from controllers.IrrigationControllers import IrrigationControllers
from lib.auth import check_auth
from routes.base import error_return, format_return

logger = logging.getLogger(__name__)

irrigation = Blueprint("irrigation", __name__)
irrigation.before_request(check_auth)


@irrigation.route("/schedules", methods=["GET"])
def schedules() -> Any:
    try:
        zone_id = request.args.get("zoneId", type=int, default=None)
        subzone_id = request.args.get("subzoneId", type=int, default=None)
        data = IrrigationControllers.schedules(zone_id, subzone_id)
        return format_return(data)
    except Exception:
        logger.exception("Error fetching schedules")
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
    except Exception:
        logger.exception("Error creating schedule")
        return error_return({"error": "Failed to create schedule"}, 500)


@irrigation.route("/schedules/<int:id>", methods=["PUT"])
def update_schedule(id: int) -> Any:
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
        IrrigationControllers.update_schedule(id, params)
        return format_return({"Success": True})
    except Exception:
        logger.exception("Error updating schedule")
        return error_return({"error": "Failed to update schedule"}, 500)


@irrigation.route("/schedules/reorder", methods=["PUT"])
def reorder_schedules() -> Any:
    try:
        data = request.get_json()
        ids = data["ids"]
        IrrigationControllers.reorder_schedules(ids)
        return format_return({"Success": True})
    except Exception:
        logger.exception("Error reordering schedules")
        return error_return({"error": "Failed to reorder schedules"}, 500)


@irrigation.route("/schedules/<int:id>/toggle", methods=["POST"])
def toggle_schedule(id: int) -> Any:
    try:
        data = request.get_json()
        IrrigationControllers.toggle_schedule(id, data)
        return format_return({"Success": True})
    except Exception:
        logger.exception("Error toggling schedule")
        return error_return({"error": "Failed to update schedule"}, 500)


@irrigation.route("/schedules/<int:id>", methods=["DELETE"])
def delete_schedule(id: int) -> Any:
    try:
        IrrigationControllers.delete_schedule(id)
        return format_return({"Success": True})
    except Exception:
        logger.exception("Error deleting schedule")
        return error_return({"error": "Failed to delete schedule"}, 500)


@irrigation.route("/schedules/sync-status", methods=["GET"])
def check_sync() -> Any:
    try:
        data = IrrigationControllers.check_sync()
        return format_return(data)
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to check sync status"}, 500)


@irrigation.route("/schedules/sync", methods=["POST"])
def force_sync() -> Any:
    try:
        data = IrrigationControllers.force_sync()
        return format_return(data)
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to force sync"}, 500)


@irrigation.route("/schedules/automation", methods=["GET"])
def fetch_automation_schedules() -> Any:
    try:
        data = IrrigationControllers.fetch_automation_schedules(exclude_inactive=True)
        return format_return(data)
    except Exception:
        logger.exception("Error fetching automation schedules")
        return error_return({"error": "Failed to fetch automation schedules"}, 500)


@irrigation.route("/zones", methods=["GET"])
def fetch_zones() -> Any:
    try:
        zone_type_id = request.args.get("zoneTypeId", type=int, default=None)
        data = IrrigationControllers.fetch_zones(zone_type_id)
        return format_return(data)
    except Exception:
        logger.exception("Error fetching zones")
        return error_return({"error": "Failed to fetch all zones"}, 500)


@irrigation.route("/history/totals", methods=["GET"])
def fetch_history_totals() -> Any:
    try:
        zone_id = request.args.get("zoneId", default=None, type=int)
        subzone_id = request.args.get("subzoneId", default=None, type=int)
        data = IrrigationControllers.fetch_history_totals(zone_id=zone_id, subzone_id=subzone_id)
        return format_return(data)
    except Exception:
        logger.exception("Error fetching history totals")
        return error_return({"error": "Failed to fetch history totals"}, 500)


@irrigation.route("/history", methods=["GET"])
def fetch_history() -> Any:
    try:
        limit = request.args.get("limit", default=100, type=int)
        offset = request.args.get("offset", default=0, type=int)
        zone_id = request.args.get("zoneId", default=None, type=int)
        subzone_id = request.args.get("subzoneId", default=None, type=int)
        start_date = request.args.get("startDate", default=None, type=str)
        end_date = request.args.get("endDate", default=None, type=str)
        data = IrrigationControllers.fetch_history(
            limit=limit, offset=offset, zone_id=zone_id, subzone_id=subzone_id, start_date=start_date, end_date=end_date
        )
        return format_return(data)
    except Exception:
        logger.exception("Error fetching history")
        return error_return({"error": "Failed to fetch history"}, 500)


@irrigation.route("/history/<int:id>", methods=["DELETE"])
def delete_history(id: int) -> Any:
    try:
        IrrigationControllers.delete_history(id)
        return format_return({"Success": True})
    except Exception:
        logger.exception("Error deleting history")
        return error_return({"error": "Failed to delete history"}, 500)


@irrigation.route("/history", methods=["POST"])
def create_history() -> Any:
    try:
        data = request.get_json()
        IrrigationControllers.create_history(data)
        return format_return({"Success": True})
    except Exception:
        logger.exception("Error creating history")
        return error_return({"error": "Failed to create history"}, 500)


@irrigation.route("/zones/types", methods=["GET"])
def fetch_zone_types() -> Any:
    try:
        data = IrrigationControllers.fetch_zone_types()
        return format_return(data)
    except Exception:
        logger.exception("Error fetching zone types")
        return error_return({"error": "Failed to fetch zone types"}, 500)
