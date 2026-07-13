import traceback
from flask import Blueprint, request
from controllers.RowingControllers import RowingControllers
from routes.base import format_return, error_return
from lib.auth import check_auth

rowing = Blueprint("rowing", __name__)
rowing.before_request(check_auth)


# ── Crew Members ───────────────────────────────────────────────────────────────

@rowing.route("/crew", methods=["GET"])
def fetch_crew_members():
    try:
        return format_return(RowingControllers.fetch_crew_members())
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to fetch crew members"}, 500)


@rowing.route("/crew", methods=["POST"])
def create_crew_member():
    try:
        data = request.get_json()
        crew_id = RowingControllers.create_crew_member(data["name"])
        return format_return({"id": crew_id})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to create crew member"}, 500)


@rowing.route("/crew/<int:id>", methods=["PUT"])
def update_crew_member(id: int):
    try:
        data = request.get_json()
        RowingControllers.update_crew_member(id, data["name"])
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to update crew member"}, 500)


@rowing.route("/crew/<int:id>", methods=["DELETE"])
def delete_crew_member(id: int):
    try:
        RowingControllers.delete_crew_member(id)
        return format_return({"success": True})
    except ValueError as e:
        return error_return({"error": str(e)}, 409)
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to delete crew member"}, 500)


# ── Boats ──────────────────────────────────────────────────────────────────────

@rowing.route("/boats", methods=["GET"])
def fetch_boats():
    try:
        return format_return(RowingControllers.fetch_boats())
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to fetch boats"}, 500)


@rowing.route("/boats", methods=["POST"])
def create_boat():
    try:
        data = request.get_json()
        boat_id = RowingControllers.create_boat(data["name"], data["crewMemberIds"])
        return format_return({"id": boat_id})
    except ValueError as e:
        return error_return({"error": str(e)}, 400)
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to create boat"}, 500)


@rowing.route("/boats/<int:id>", methods=["PUT"])
def update_boat(id: int):
    try:
        data = request.get_json()
        RowingControllers.update_boat(id, data["name"], data["crewMemberIds"])
        return format_return({"success": True})
    except ValueError as e:
        return error_return({"error": str(e)}, 400)
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to update boat"}, 500)


@rowing.route("/boats/<int:id>", methods=["DELETE"])
def delete_boat(id: int):
    try:
        RowingControllers.delete_boat(id)
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to delete boat"}, 500)


# ── Races ──────────────────────────────────────────────────────────────────────

@rowing.route("/races", methods=["GET"])
def fetch_races():
    try:
        return format_return(RowingControllers.fetch_races())
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to fetch races"}, 500)


@rowing.route("/races/<int:id>", methods=["GET"])
def fetch_race(id: int):
    try:
        race = RowingControllers.fetch_race(id)
        if not race:
            return error_return({"error": "Race not found"}, 404)
        return format_return(race)
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to fetch race"}, 500)


@rowing.route("/races", methods=["POST"])
def create_race():
    try:
        data = request.get_json()
        race_id = RowingControllers.create_race(
            distance=data["distance"],
            race_type=data["raceType"],
            boat_ids=data["boatIds"],
            wind_conditions=data.get("windConditions"),
            notes=data.get("notes"),
        )
        return format_return({"id": race_id})
    except ValueError as e:
        return error_return({"error": str(e)}, 400)
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to create race"}, 500)


@rowing.route("/races/<int:id>/activate", methods=["POST"])
def activate_race(id: int):
    try:
        RowingControllers.activate_race(id)
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to activate race"}, 500)


@rowing.route("/races/<int:id>/complete", methods=["POST"])
def complete_race(id: int):
    try:
        RowingControllers.complete_race(id)
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to complete race"}, 500)


@rowing.route("/races/<int:id>", methods=["DELETE"])
def delete_race(id: int):
    try:
        RowingControllers.delete_race(id)
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to delete race"}, 500)


# ── Race Entries ───────────────────────────────────────────────────────────────

@rowing.route("/entries/<int:entry_id>/start", methods=["POST"])
def record_start(entry_id: int):
    try:
        data = request.get_json()
        RowingControllers.record_start(entry_id, data["startTime"])
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to record start"}, 500)


@rowing.route("/entries/<int:entry_id>/finish", methods=["POST"])
def record_finish(entry_id: int):
    try:
        data = request.get_json()
        RowingControllers.record_finish(entry_id, data["finishTime"], data["elapsedMs"])
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to record finish"}, 500)


@rowing.route("/entries/<int:entry_id>/dns", methods=["POST"])
def mark_dns(entry_id: int):
    try:
        RowingControllers.mark_dns(entry_id)
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to mark DNS"}, 500)


@rowing.route("/entries/<int:entry_id>/dnf", methods=["POST"])
def mark_dnf(entry_id: int):
    try:
        RowingControllers.mark_dnf(entry_id)
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to mark DNF"}, 500)


@rowing.route("/entries/<int:entry_id>", methods=["DELETE"])
def delete_entry(entry_id: int):
    try:
        RowingControllers.delete_entry(entry_id)
        return format_return({"success": True})
    except Exception:
        traceback.print_exc()
        return error_return({"error": "Failed to delete entry"}, 500)
