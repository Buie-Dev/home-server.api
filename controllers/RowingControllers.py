from services.RowingServices import RowingServices
from typing import List, Optional


class RowingControllers:
    # ── Boat Classes ───────────────────────────────────────────────────────

    @staticmethod
    def fetch_boat_classes():
        return RowingServices.fetch_boat_classes()

    # ── Crew Members ───────────────────────────────────────────────────────

    @staticmethod
    def fetch_crew_members():
        return RowingServices.fetch_crew_members()

    @staticmethod
    def create_crew_member(name: str, gender: str):
        return RowingServices.create_crew_member(name, gender)

    @staticmethod
    def update_crew_member(id: int, name: str, gender: str):
        return RowingServices.update_crew_member(id, name, gender)

    @staticmethod
    def delete_crew_member(id: int):
        return RowingServices.delete_crew_member(id)

    # ── Boats ──────────────────────────────────────────────────────────────

    @staticmethod
    def fetch_boats():
        return RowingServices.fetch_boats()

    @staticmethod
    def create_boat(name: str, boat_class_id: Optional[int]):
        return RowingServices.create_boat(name, boat_class_id)

    @staticmethod
    def update_boat(id: int, name: str, boat_class_id: Optional[int]):
        return RowingServices.update_boat(id, name, boat_class_id)

    @staticmethod
    def delete_boat(id: int):
        return RowingServices.delete_boat(id)

    # ── Crews ──────────────────────────────────────────────────────────────

    @staticmethod
    def fetch_crews():
        return RowingServices.fetch_crews()

    @staticmethod
    def create_crew(
        boat_id: int,
        gender: str,
        age_category: str,
        cox: Optional[int],
        seat_1: Optional[int],
        seat_2: Optional[int],
        seat_3: Optional[int],
        seat_4: Optional[int],
        seat_5: Optional[int],
        seat_6: Optional[int],
        seat_7: Optional[int],
        seat_8: Optional[int],
    ):
        return RowingServices.create_crew(
            boat_id, gender, age_category, cox, seat_1, seat_2, seat_3, seat_4, seat_5, seat_6, seat_7, seat_8
        )

    @staticmethod
    def update_crew(
        crew_id: int,
        boat_id: int,
        gender: str,
        age_category: str,
        cox: Optional[int],
        seat_1: Optional[int],
        seat_2: Optional[int],
        seat_3: Optional[int],
        seat_4: Optional[int],
        seat_5: Optional[int],
        seat_6: Optional[int],
        seat_7: Optional[int],
        seat_8: Optional[int],
    ):
        return RowingServices.update_crew(
            crew_id, boat_id, gender, age_category, cox, seat_1, seat_2, seat_3, seat_4, seat_5, seat_6, seat_7, seat_8
        )

    @staticmethod
    def update_crew_lineup(
        crew_id: int,
        boat_id: int,
        gender: str,
        age_category: str,
        cox: Optional[int],
        seat_1: Optional[int],
        seat_2: Optional[int],
        seat_3: Optional[int],
        seat_4: Optional[int],
        seat_5: Optional[int],
        seat_6: Optional[int],
        seat_7: Optional[int],
        seat_8: Optional[int],
    ):
        return RowingServices.update_crew_lineup(
            crew_id, boat_id, gender, age_category, cox, seat_1, seat_2, seat_3, seat_4, seat_5, seat_6, seat_7, seat_8
        )

    @staticmethod
    def delete_crew(crew_id: int):
        return RowingServices.delete_crew(crew_id)

    # ── Races ──────────────────────────────────────────────────────────────

    @staticmethod
    def fetch_races(date: str):
        return RowingServices.fetch_races(date)

    @staticmethod
    def fetch_race(id: int):
        return RowingServices.fetch_race(id)

    @staticmethod
    def create_race(
        distance: str,
        race_type: str,
        crew_ids: List[int],
        event_type: Optional[str],
        wind_conditions: Optional[str],
        notes: Optional[str],
    ):
        return RowingServices.create_race(distance, race_type, crew_ids, event_type, wind_conditions, notes)

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
    def reassign_entry_crew(entry_id: int, crew_id: int):
        return RowingServices.reassign_entry_crew(entry_id, crew_id)

    @staticmethod
    def delete_entry(entry_id: int):
        return RowingServices.delete_entry(entry_id)

    # ── World Best Times ───────────────────────────────────────────────────

    @staticmethod
    def fetch_world_best_times():
        return RowingServices.fetch_world_best_times()
