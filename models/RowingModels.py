from models.Base import Base
from typing import Optional


class RowingModels:

    # ── Boat Classes ───────────────────────────────────────────────────────

    @staticmethod
    def fetch_boat_classes():
        return Base.custom_query(
            "SELECT id, symbol, name, crew_count AS crewCount, has_cox AS hasCox FROM rowing_boat_classes ORDER BY crew_count ASC, has_cox ASC"
        )

    # ── Crew Members ───────────────────────────────────────────────────────

    @staticmethod
    def fetch_crew_members():
        return Base.custom_query(
            "SELECT id, name, gender, created_at AS createdAt FROM rowing_crew_members WHERE deleted_at IS NULL ORDER BY name ASC"
        )

    @staticmethod
    def create_crew_member(name: str, gender: str):
        return Base.custom_insert(
            "INSERT INTO rowing_crew_members (name, gender) VALUES (%s, %s)",
            (name, gender),
        )

    @staticmethod
    def update_crew_member(id: int, name: str, gender: str):
        return Base.custom_update(
            "UPDATE rowing_crew_members SET name = %s, gender = %s WHERE id = %s",
            (name, gender, id),
        )

    @staticmethod
    def delete_crew_member(id: int):
        return Base.custom_update(
            "UPDATE rowing_crew_members SET deleted_at = NOW() WHERE id = %s",
            (id,),
        )

    @staticmethod
    def count_boats_for_crew_member(crew_member_id: int):
        row = Base.single_query(
            "SELECT COUNT(*) AS count FROM rowing_boat_crew WHERE crew_member_id = %s",
            (crew_member_id,),
        )
        return row["count"] if row else 0

    # ── Boats ──────────────────────────────────────────────────────────────

    @staticmethod
    def fetch_boats():
        return Base.custom_query(
            """
            SELECT
                b.id,
                b.name,
                b.boat_class_id AS boatClassId,
                bc.symbol AS boatClassSymbol,
                bc.name AS boatClassName,
                b.created_at AS createdAt
            FROM rowing_boats b
            LEFT JOIN rowing_boat_classes bc ON b.boat_class_id = bc.id
            WHERE b.deleted_at IS NULL
            ORDER BY b.name ASC
            """
        )

    @staticmethod
    def fetch_boat_crew(boat_id: int):
        return Base.custom_query(
            """
            SELECT bc.id, bc.crew_member_id AS crewMemberId, cm.name AS crewMemberName,
                   cm.gender AS crewMemberGender, bc.seat_position AS seatPosition
            FROM rowing_boat_crew bc
            JOIN rowing_crew_members cm ON bc.crew_member_id = cm.id
            WHERE bc.boat_id = %s AND cm.deleted_at IS NULL
            ORDER BY bc.seat_position ASC
            """,
            (boat_id,),
        )

    @staticmethod
    def count_crew_in_boat(boat_id: int):
        row = Base.single_query(
            "SELECT COUNT(*) AS count FROM rowing_boat_crew WHERE boat_id = %s",
            (boat_id,),
        )
        return row["count"] if row else 0

    @staticmethod
    def create_boat(name: str, boat_class_id: Optional[int]):
        return Base.custom_insert(
            "INSERT INTO rowing_boats (name, boat_class_id) VALUES (%s, %s)",
            (name, boat_class_id),
        )

    @staticmethod
    def update_boat_name(id: int, name: str, boat_class_id: Optional[int]):
        return Base.custom_update(
            "UPDATE rowing_boats SET name = %s, boat_class_id = %s WHERE id = %s",
            (name, boat_class_id, id),
        )

    @staticmethod
    def add_crew_to_boat(boat_id: int, crew_member_id: int, seat_position: int):
        return Base.custom_insert(
            "INSERT INTO rowing_boat_crew (boat_id, crew_member_id, seat_position) VALUES (%s, %s, %s)",
            (boat_id, crew_member_id, seat_position),
        )

    @staticmethod
    def remove_crew_from_boat(boat_id: int, crew_member_id: int):
        return Base.custom_delete(
            "DELETE FROM rowing_boat_crew WHERE boat_id = %s AND crew_member_id = %s",
            (boat_id, crew_member_id),
        )

    @staticmethod
    def clear_boat_crew(boat_id: int):
        return Base.custom_delete(
            "DELETE FROM rowing_boat_crew WHERE boat_id = %s",
            (boat_id,),
        )

    @staticmethod
    def delete_boat(id: int):
        return Base.custom_update(
            "UPDATE rowing_boats SET deleted_at = NOW() WHERE id = %s",
            (id,),
        )

    # ── Races ──────────────────────────────────────────────────────────────

    @staticmethod
    def fetch_races():
        return Base.custom_query(
            """
            SELECT
                id,
                distance,
                race_type AS raceType,
                event_type AS eventType,
                wind_conditions AS windConditions,
                notes,
                status,
                created_at AS createdAt,
                completed_at AS completedAt
            FROM rowing_races
            WHERE deleted_at IS NULL
            ORDER BY created_at DESC
            """
        )

    @staticmethod
    def fetch_race(id: int):
        return Base.single_query(
            """
            SELECT
                id,
                distance,
                race_type AS raceType,
                event_type AS eventType,
                wind_conditions AS windConditions,
                notes,
                status,
                created_at AS createdAt,
                completed_at AS completedAt
            FROM rowing_races
            WHERE id = %s AND deleted_at IS NULL
            """,
            (id,),
        )

    @staticmethod
    def create_race(distance: str, race_type: str, event_type: str, wind_conditions: Optional[str], notes: Optional[str]):
        return Base.custom_insert(
            "INSERT INTO rowing_races (distance, race_type, event_type, wind_conditions, notes) VALUES (%s, %s, %s, %s, %s)",
            (distance, race_type, event_type, wind_conditions, notes),
        )

    @staticmethod
    def update_race_status(id: int, status: str):
        if status == "completed":
            return Base.custom_update(
                "UPDATE rowing_races SET status = %s, completed_at = NOW() WHERE id = %s",
                (status, id),
            )
        return Base.custom_update(
            "UPDATE rowing_races SET status = %s WHERE id = %s",
            (status, id),
        )

    @staticmethod
    def delete_race(id: int):
        return Base.custom_update(
            "UPDATE rowing_races SET deleted_at = NOW() WHERE id = %s",
            (id,),
        )

    # ── Race Entries ───────────────────────────────────────────────────────

    @staticmethod
    def fetch_entries_for_race(race_id: int):
        return Base.custom_query(
            """
            SELECT
                e.id,
                e.race_id AS raceId,
                e.boat_id AS boatId,
                b.name AS boatName,
                e.start_time AS startTime,
                e.finish_time AS finishTime,
                e.elapsed_ms AS elapsedMs,
                e.dns,
                e.dnf,
                e.placement
            FROM rowing_race_entries e
            JOIN rowing_boats b ON e.boat_id = b.id
            WHERE e.race_id = %s AND e.deleted_at IS NULL
            ORDER BY e.placement ASC, e.elapsed_ms ASC
            """,
            (race_id,),
        )

    @staticmethod
    def create_entry(race_id: int, boat_id: int):
        return Base.custom_insert(
            "INSERT INTO rowing_race_entries (race_id, boat_id) VALUES (%s, %s)",
            (race_id, boat_id),
        )

    @staticmethod
    def record_entry_start(entry_id: int, start_time: int):
        return Base.custom_update(
            "UPDATE rowing_race_entries SET start_time = %s WHERE id = %s",
            (start_time, entry_id),
        )

    @staticmethod
    def record_entry_finish(entry_id: int, finish_time: int, elapsed_ms: int):
        return Base.custom_update(
            "UPDATE rowing_race_entries SET finish_time = %s, elapsed_ms = %s WHERE id = %s",
            (finish_time, elapsed_ms, entry_id),
        )

    @staticmethod
    def mark_entry_dns(entry_id: int):
        return Base.custom_update(
            "UPDATE rowing_race_entries SET dns = 1 WHERE id = %s",
            (entry_id,),
        )

    @staticmethod
    def mark_entry_dnf(entry_id: int):
        return Base.custom_update(
            "UPDATE rowing_race_entries SET dnf = 1 WHERE id = %s",
            (entry_id,),
        )

    @staticmethod
    def update_placements(race_id: int):
        finished = Base.custom_query(
            "SELECT id FROM rowing_race_entries WHERE race_id = %s AND elapsed_ms IS NOT NULL AND dns = 0 AND dnf = 0 ORDER BY elapsed_ms ASC",
            (race_id,),
        )
        for i, row in enumerate(finished, start=1):
            Base.custom_update(
                "UPDATE rowing_race_entries SET placement = %s WHERE id = %s",
                (i, row["id"]),
            )

    @staticmethod
    def delete_entry(entry_id: int):
        return Base.custom_update(
            "UPDATE rowing_race_entries SET deleted_at = NOW() WHERE id = %s",
            (entry_id,),
        )
