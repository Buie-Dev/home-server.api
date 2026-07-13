from services.RowingServices import RowingServices
from typing import List, Optional


class RowingControllers:

    # ── Crew Members ───────────────────────────────────────────────────────

    @staticmethod
    def fetch_crew_members():
        return RowingServices.fetch_crew_members()

    @staticmethod
    def create_crew_member(name: str):
        return RowingServices.create_crew_member(name)

    @staticmethod
    def update_crew_member(id: int, name: str):
        return RowingServices.update_crew_member(id, name)

    @staticmethod
    def delete_crew_member(id: int):
        return RowingServices.delete_crew_member(id)

    # ── Boats ──────────────────────────────────────────────────────────────

    @staticmethod
    def fetch_boats():
        return RowingServices.fetch_boats()

    @staticmethod
    def create_boat(name: str, crew_member_ids: List[int]):
        return RowingServices.create_boat(name, crew_member_ids)

    @staticmethod
    def update_boat(id: int, name: str, crew_member_ids: List[int]):
        return RowingServices.update_boat(id, name, crew_member_ids)

    @staticmethod
    def delete_boat(id: int):
        return RowingServices.delete_boat(id)

    # ── Races ──────────────────────────────────────────────────────────────

    @staticmethod
    def fetch_races():
        return RowingServices.fetch_races()

    @staticmethod
    def fetch_race(id: int):
        return RowingServices.fetch_race(id)

    @staticmethod
    def create_race(distance: str, race_type: str, boat_ids: List[int], wind_conditions: Optional[str], notes: Optional[str]):
        return RowingServices.create_race(distance, race_type, boat_ids, wind_conditions, notes)

    @staticmethod
    def activate_race(id: int):
        return RowingServices.activate_race(id)

    @staticmethod
    def complete_race(id: int):
        return RowingServices.complete_race(id)

    @staticmethod
    def delete_race(id: int):
        return RowingServices.delete_race(id)

    # ── Race Entries ───────────────────────────────────────────────────────

    @staticmethod
    def record_start(entry_id: int, start_time: int):
        return RowingServices.record_start(entry_id, start_time)

    @staticmethod
    def record_finish(entry_id: int, finish_time: int, elapsed_ms: int):
        return RowingServices.record_finish(entry_id, finish_time, elapsed_ms)

    @staticmethod
    def mark_dns(entry_id: int):
        return RowingServices.mark_dns(entry_id)

    @staticmethod
    def mark_dnf(entry_id: int):
        return RowingServices.mark_dnf(entry_id)

    @staticmethod
    def delete_entry(entry_id: int):
        return RowingServices.delete_entry(entry_id)
