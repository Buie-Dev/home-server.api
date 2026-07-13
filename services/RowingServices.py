from models.RowingModels import RowingModels
from typing import List, Optional
import json

MAX_CREW = 9
MIN_CREW = 1


class RowingServices:

    # ── Crew Members ───────────────────────────────────────────────────────

    @staticmethod
    def fetch_crew_members():
        return RowingModels.fetch_crew_members()

    @staticmethod
    def create_crew_member(name: str):
        result = RowingModels.create_crew_member(name)
        return result["inserted_id"]

    @staticmethod
    def update_crew_member(id: int, name: str):
        RowingModels.update_crew_member(id, name)

    @staticmethod
    def delete_crew_member(id: int):
        count = RowingModels.count_boats_for_crew_member(id)
        if count > 0:
            raise ValueError(f"Crew member is assigned to {count} boat(s) and cannot be deleted")
        RowingModels.delete_crew_member(id)

    # ── Boats ──────────────────────────────────────────────────────────────

    @staticmethod
    def fetch_boats():
        boats = RowingModels.fetch_boats()
        result = []
        for boat in boats:
            crew = RowingModels.fetch_boat_crew(boat["id"])
            result.append({
                "id": boat["id"],
                "name": boat["name"],
                "createdAt": str(boat["createdAt"]),
                "crew": [
                    {
                        "id": c["id"],
                        "crewMemberId": c["crewMemberId"],
                        "crewMemberName": c["crewMemberName"],
                        "seatPosition": c["seatPosition"],
                    }
                    for c in crew
                ],
            })
        return result

    @staticmethod
    def create_boat(name: str, crew_member_ids: List[int]):
        if len(crew_member_ids) < MIN_CREW:
            raise ValueError(f"A boat must have at least {MIN_CREW} crew member")
        if len(crew_member_ids) > MAX_CREW:
            raise ValueError(f"A boat cannot have more than {MAX_CREW} crew members")

        result = RowingModels.create_boat(name)
        boat_id = result["inserted_id"]
        for i, crew_member_id in enumerate(crew_member_ids, start=1):
            RowingModels.add_crew_to_boat(boat_id, crew_member_id, i)
        return boat_id

    @staticmethod
    def update_boat(id: int, name: str, crew_member_ids: List[int]):
        if len(crew_member_ids) < MIN_CREW:
            raise ValueError(f"A boat must have at least {MIN_CREW} crew member")
        if len(crew_member_ids) > MAX_CREW:
            raise ValueError(f"A boat cannot have more than {MAX_CREW} crew members")

        RowingModels.update_boat_name(id, name)
        RowingModels.clear_boat_crew(id)
        for i, crew_member_id in enumerate(crew_member_ids, start=1):
            RowingModels.add_crew_to_boat(id, crew_member_id, i)

    @staticmethod
    def delete_boat(id: int):
        RowingModels.delete_boat(id)

    # ── Races ──────────────────────────────────────────────────────────────

    @staticmethod
    def fetch_races():
        races = RowingModels.fetch_races()
        result = []
        for race in races:
            entries = RowingModels.fetch_entries_for_race(race["id"])
            result.append({
                "id": race["id"],
                "distance": race["distance"],
                "raceType": race["raceType"],
                "windConditions": race["windConditions"],
                "notes": race["notes"],
                "status": race["status"],
                "createdAt": str(race["createdAt"]),
                "completedAt": str(race["completedAt"]) if race["completedAt"] else None,
                "entries": RowingServices._format_entries(entries),
            })
        return result

    @staticmethod
    def fetch_race(id: int):
        race = RowingModels.fetch_race(id)
        if not race:
            return None
        entries = RowingModels.fetch_entries_for_race(id)
        return {
            "id": race["id"],
            "distance": race["distance"],
            "raceType": race["raceType"],
            "windConditions": race["windConditions"],
            "notes": race["notes"],
            "status": race["status"],
            "createdAt": str(race["createdAt"]),
            "completedAt": str(race["completedAt"]) if race["completedAt"] else None,
            "entries": RowingServices._format_entries(entries),
        }

    @staticmethod
    def create_race(distance: str, race_type: str, boat_ids: List[int], wind_conditions: Optional[str], notes: Optional[str]):
        if race_type not in ("time_trial", "side_by_side"):
            raise ValueError("race_type must be 'time_trial' or 'side_by_side'")
        if not boat_ids:
            raise ValueError("At least one boat is required")

        result = RowingModels.create_race(distance, race_type, wind_conditions, notes)
        race_id = result["inserted_id"]
        for boat_id in boat_ids:
            RowingModels.create_entry(race_id, boat_id)
        return race_id

    @staticmethod
    def activate_race(id: int):
        RowingModels.update_race_status(id, "active")

    @staticmethod
    def complete_race(id: int):
        RowingModels.update_placements(id)
        RowingModels.update_race_status(id, "completed")

    @staticmethod
    def delete_race(id: int):
        RowingModels.delete_race(id)

    # ── Race Entries ───────────────────────────────────────────────────────

    @staticmethod
    def record_start(entry_id: int, start_time: int):
        RowingModels.record_entry_start(entry_id, start_time)

    @staticmethod
    def record_finish(entry_id: int, finish_time: int, elapsed_ms: int):
        RowingModels.record_entry_finish(entry_id, finish_time, elapsed_ms)

    @staticmethod
    def mark_dns(entry_id: int):
        RowingModels.mark_entry_dns(entry_id)

    @staticmethod
    def mark_dnf(entry_id: int):
        RowingModels.mark_entry_dnf(entry_id)

    @staticmethod
    def delete_entry(entry_id: int):
        RowingModels.delete_entry(entry_id)

    # ── Helpers ────────────────────────────────────────────────────────────

    @staticmethod
    def _format_entries(entries):
        return [
            {
                "id": e["id"],
                "raceId": e["raceId"],
                "boatId": e["boatId"],
                "boatName": e["boatName"],
                "startTime": e["startTime"],
                "finishTime": e["finishTime"],
                "elapsedMs": e["elapsedMs"],
                "dns": bool(e["dns"]),
                "dnf": bool(e["dnf"]),
                "placement": e["placement"],
            }
            for e in entries
        ]
