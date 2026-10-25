from models.RowingModels import RowingModels
from typing import List, Optional


class RowingServices:
    # ── Boat Classes ───────────────────────────────────────────────────────

    @staticmethod
    def fetch_boat_classes():
        return [
            {
                "id": c["id"],
                "symbol": c["symbol"],
                "crewCount": c["crewCount"],
                "hasCox": bool(c["hasCox"]),
            }
            for c in RowingModels.fetch_boat_classes()
        ]

    # ── Crew Members ───────────────────────────────────────────────────────

    @staticmethod
    def fetch_crew_members():
        return RowingModels.fetch_crew_members()

    @staticmethod
    def create_crew_member(name: str, gender: str):
        return RowingModels.create_crew_member(name, gender)["inserted_id"]

    @staticmethod
    def update_crew_member(id: int, name: str, gender: str):
        RowingModels.update_crew_member(id, name, gender)

    @staticmethod
    def delete_crew_member(id: int):
        count = RowingModels.count_crews_for_crew_member(id)
        if count > 0:
            raise ValueError(f"This rower is assigned to {count} crew(s) — remove them from crews first")
        RowingModels.delete_crew_member(id)

    # ── Boats ──────────────────────────────────────────────────────────────

    @staticmethod
    def fetch_boats():
        return [RowingServices._format_boat(b) for b in RowingModels.fetch_boats()]

    @staticmethod
    def create_boat(name: str, boat_class_id: Optional[int]):
        if not name.strip():
            raise ValueError("Boat name is required")
        return RowingModels.create_boat(name, boat_class_id)["inserted_id"]

    @staticmethod
    def update_boat(id: int, name: str, boat_class_id: Optional[int]):
        if not name.strip():
            raise ValueError("Boat name is required")
        RowingModels.update_boat(id, name, boat_class_id)

    @staticmethod
    def delete_boat(id: int):
        RowingModels.delete_boat(id)

    # ── Crews ──────────────────────────────────────────────────────────────

    @staticmethod
    def fetch_crews():
        return [
            {
                **RowingServices._format_crew(r),
                "hasResults": RowingModels.crew_has_results(r["id"]),
            }
            for r in RowingModels.fetch_crews()
        ]

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
        RowingServices._validate_crew_seats(cox, seat_1, seat_2, seat_3, seat_4, seat_5, seat_6, seat_7, seat_8)
        return RowingModels.create_crew(
            boat_id, gender, age_category, cox, seat_1, seat_2, seat_3, seat_4, seat_5, seat_6, seat_7, seat_8
        )["inserted_id"]

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
        RowingServices._validate_crew_seats(cox, seat_1, seat_2, seat_3, seat_4, seat_5, seat_6, seat_7, seat_8)
        if not RowingModels.fetch_crew(crew_id):
            raise ValueError("Crew not found")
        RowingModels.update_crew(
            crew_id, boat_id, gender, age_category, cox, seat_1, seat_2, seat_3, seat_4, seat_5, seat_6, seat_7, seat_8
        )
        return {"id": crew_id, "copied": False}

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
        """Always edits in place — used from the race results screen to correct who raced."""
        RowingServices._validate_crew_seats(cox, seat_1, seat_2, seat_3, seat_4, seat_5, seat_6, seat_7, seat_8)
        if not RowingModels.fetch_crew(crew_id):
            raise ValueError("Crew not found")
        RowingModels.update_crew(
            crew_id, boat_id, gender, age_category, cox, seat_1, seat_2, seat_3, seat_4, seat_5, seat_6, seat_7, seat_8
        )

    @staticmethod
    def delete_crew(crew_id: int):
        RowingModels.delete_crew(crew_id)

    # ── Races ──────────────────────────────────────────────────────────────

    @staticmethod
    def fetch_races(date: str):
        return [
            {
                **RowingServices._format_race(race),
                "entries": RowingServices._format_entries(
                    RowingModels.fetch_entries_for_race(race["id"]), race["distance"]
                ),
            }
            for race in RowingModels.fetch_races(date)
        ]

    @staticmethod
    def fetch_race(id: int):
        race = RowingModels.fetch_race(id)
        if not race:
            return None
        return {
            **RowingServices._format_race(race),
            "entries": RowingServices._format_entries(RowingModels.fetch_entries_for_race(id), race["distance"]),
        }

    @staticmethod
    def create_race(
        distance: str,
        race_type: str,
        crew_ids: List[int],
        event_type: Optional[str],
        wind_conditions: Optional[str],
        notes: Optional[str],
    ):
        if race_type not in ("time_trial", "side_by_side"):
            raise ValueError("race_type must be 'time_trial' or 'side_by_side'")
        if not crew_ids:
            raise ValueError("At least one crew is required")
        race_id = RowingModels.create_race(distance, race_type, event_type, wind_conditions, notes)["inserted_id"]
        for crew_id in crew_ids:
            RowingModels.create_entry(race_id, crew_id)
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
    def reassign_entry_crew(entry_id: int, crew_id: int):
        RowingModels.update_entry_crew(entry_id, crew_id)

    @staticmethod
    def delete_entry(entry_id: int):
        RowingModels.delete_entry(entry_id)

    # ── Helpers ────────────────────────────────────────────────────────────

    @staticmethod
    def _validate_crew_seats(*member_ids):
        filled = [mid for mid in member_ids if mid is not None]
        if len(filled) != len(set(filled)):
            raise ValueError("Each rower can only occupy one seat")

    @staticmethod
    def _crew_class_name(gender: str, age_category: str, symbol: str) -> str:
        if gender == "Mixed":
            return f"Mixed {age_category} {symbol}"
        return f"{gender}'s {age_category} {symbol}"

    @staticmethod
    def _format_boat(b: dict) -> dict:
        has_cox = b.get("boatClassHasCox")
        return {
            "id": b["id"],
            "name": b["name"],
            "boatClassId": b.get("boatClassId"),
            "boatClassSymbol": b.get("boatClassSymbol"),
            "boatClassCrewCount": b.get("boatClassCrewCount"),
            "boatClassHasCox": bool(has_cox) if has_cox is not None else False,
            "createdAt": str(b["createdAt"]),
        }

    @staticmethod
    def _format_crew(r: dict) -> dict:
        def slot(mid, name, gender):
            if mid is None:
                return None
            return {"crewMemberId": mid, "name": name or "", "gender": gender or ""}

        symbol = r.get("boatClassSymbol")
        gender = r.get("gender")
        age_cat = r.get("ageCategory")
        has_cox = r.get("boatClassHasCox")
        crew_class_name = (
            RowingServices._crew_class_name(gender, age_cat, symbol) if symbol and gender and age_cat else symbol
        )

        return {
            "id": r["id"],
            "boatId": r["boatId"],
            "boatName": r["boatName"],
            "boatClassId": r.get("boatClassId"),
            "boatClassSymbol": symbol,
            "boatClassCrewCount": r.get("boatClassCrewCount"),
            "boatClassHasCox": bool(has_cox) if has_cox is not None else False,
            "gender": gender,
            "ageCategory": age_cat,
            "crewClassName": crew_class_name,
            "cox": slot(r.get("cox"), r.get("coxName"), r.get("coxGender")),
            "seat1": slot(r.get("seat_1"), r.get("seat1Name"), r.get("seat1Gender")),
            "seat2": slot(r.get("seat_2"), r.get("seat2Name"), r.get("seat2Gender")),
            "seat3": slot(r.get("seat_3"), r.get("seat3Name"), r.get("seat3Gender")),
            "seat4": slot(r.get("seat_4"), r.get("seat4Name"), r.get("seat4Gender")),
            "seat5": slot(r.get("seat_5"), r.get("seat5Name"), r.get("seat5Gender")),
            "seat6": slot(r.get("seat_6"), r.get("seat6Name"), r.get("seat6Gender")),
            "seat7": slot(r.get("seat_7"), r.get("seat7Name"), r.get("seat7Gender")),
            "seat8": slot(r.get("seat_8"), r.get("seat8Name"), r.get("seat8Gender")),
            "createdAt": str(r["createdAt"]),
        }

    @staticmethod
    def _format_race(race: dict) -> dict:
        return {
            "id": race["id"],
            "distance": race["distance"],
            "raceType": race["raceType"],
            "eventType": race["eventType"],
            "windConditions": race["windConditions"],
            "notes": race["notes"],
            "status": race["status"],
            "createdAt": str(race["createdAt"]),
            "completedAt": str(race["completedAt"]) if race["completedAt"] else None,
        }

    @staticmethod
    def _format_entries(entries: list, race_distance: str) -> list:
        dist = int(race_distance)
        result = []
        for e in entries:
            has_cox = bool(e.get("boatHasCox"))
            cox_name = e.get("coxName")
            stroke_name = e.get("strokeName")
            # coxie shown if the boat has a cox; stroke shown otherwise
            key_person = cox_name if has_cox else stroke_name
            elapsed_ms = e["elapsedMs"]
            wbt_time_ms = e.get("wbtTimeMs")
            if elapsed_ms is not None and wbt_time_ms is not None:
                wbt_pct = round((dist * wbt_time_ms) / (elapsed_ms * 2000) * 100, 2)
                wbt_is_estimated = bool(e.get("wbtIsEstimated"))
            else:
                wbt_pct = None
                wbt_is_estimated = False
            result.append(
                {
                    "id": e["id"],
                    "raceId": e["raceId"],
                    "crewId": e.get("crewId"),
                    "boatName": e.get("boatName") or "Unknown",
                    "coxName": cox_name,
                    "strokeName": stroke_name,
                    "keyPerson": key_person,
                    "startTime": e["startTime"],
                    "finishTime": e["finishTime"],
                    "elapsedMs": elapsed_ms,
                    "dns": bool(e["dns"]),
                    "dnf": bool(e["dnf"]),
                    "placement": e["placement"],
                    "gender": e.get("gender"),
                    "ageCategory": e.get("ageCategory"),
                    "boatClassSymbol": e.get("boatClassSymbol"),
                    "wbtPct": wbt_pct,
                    "wbtIsEstimated": wbt_is_estimated,
                }
            )
        return result

    # ── World Best Times ────────────────────────────────────────────────────

    @staticmethod
    def fetch_world_best_times():
        return [
            {
                "id": r["id"],
                "gender": r["gender"],
                "ageCategory": r["ageCategory"],
                "boatSymbol": r["boatSymbol"],
                "timeMs": r["timeMs"],
                "isEstimated": bool(r["isEstimated"]),
            }
            for r in RowingModels.fetch_world_best_times()
        ]
