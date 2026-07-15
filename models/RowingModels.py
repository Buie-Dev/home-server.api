from models.Base import Base
from typing import Optional

_CREW_BASE_SQL = """
    SELECT
        cr.id,
        cr.boat_id AS boatId,
        b.name AS boatName,
        b.boat_class_id AS boatClassId,
        bc.symbol AS boatClassSymbol,
        bc.crew_count AS boatClassCrewCount,
        bc.has_cox AS boatClassHasCox,
        cr.gender,
        cr.age_category AS ageCategory,
        cr.cox, cox_m.name AS coxName, cox_m.gender AS coxGender,
        cr.seat_1, s1.name AS seat1Name, s1.gender AS seat1Gender,
        cr.seat_2, s2.name AS seat2Name, s2.gender AS seat2Gender,
        cr.seat_3, s3.name AS seat3Name, s3.gender AS seat3Gender,
        cr.seat_4, s4.name AS seat4Name, s4.gender AS seat4Gender,
        cr.seat_5, s5.name AS seat5Name, s5.gender AS seat5Gender,
        cr.seat_6, s6.name AS seat6Name, s6.gender AS seat6Gender,
        cr.seat_7, s7.name AS seat7Name, s7.gender AS seat7Gender,
        cr.seat_8, s8.name AS seat8Name, s8.gender AS seat8Gender,
        cr.created_at AS createdAt
    FROM rowing_crews cr
    JOIN rowing_boats b ON cr.boat_id = b.id
    LEFT JOIN rowing_boat_classes bc ON b.boat_class_id = bc.id
    LEFT JOIN rowing_crew_members cox_m ON cr.cox = cox_m.id
    LEFT JOIN rowing_crew_members s1 ON cr.seat_1 = s1.id
    LEFT JOIN rowing_crew_members s2 ON cr.seat_2 = s2.id
    LEFT JOIN rowing_crew_members s3 ON cr.seat_3 = s3.id
    LEFT JOIN rowing_crew_members s4 ON cr.seat_4 = s4.id
    LEFT JOIN rowing_crew_members s5 ON cr.seat_5 = s5.id
    LEFT JOIN rowing_crew_members s6 ON cr.seat_6 = s6.id
    LEFT JOIN rowing_crew_members s7 ON cr.seat_7 = s7.id
    LEFT JOIN rowing_crew_members s8 ON cr.seat_8 = s8.id
"""


class RowingModels:

    # ── Boat Classes ───────────────────────────────────────────────────────

    @staticmethod
    def fetch_boat_classes():
        return Base.custom_query(
            """
            SELECT id, symbol, crew_count AS crewCount, has_cox AS hasCox
            FROM rowing_boat_classes
            ORDER BY crew_count ASC, has_cox ASC
            """
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
    def count_crews_for_crew_member(crew_member_id: int):
        row = Base.single_query(
            """
            SELECT COUNT(*) AS count FROM rowing_crews
            WHERE deleted_at IS NULL AND (
                cox = %s OR seat_1 = %s OR seat_2 = %s OR seat_3 = %s OR seat_4 = %s
                OR seat_5 = %s OR seat_6 = %s OR seat_7 = %s OR seat_8 = %s
            )
            """,
            tuple([crew_member_id] * 9),
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
                bc.crew_count AS boatClassCrewCount,
                bc.has_cox AS boatClassHasCox,
                b.created_at AS createdAt
            FROM rowing_boats b
            LEFT JOIN rowing_boat_classes bc ON b.boat_class_id = bc.id
            WHERE b.deleted_at IS NULL
            ORDER BY b.name ASC
            """
        )

    @staticmethod
    def create_boat(name: str, boat_class_id: Optional[int]):
        return Base.custom_insert(
            "INSERT INTO rowing_boats (name, boat_class_id) VALUES (%s, %s)",
            (name, boat_class_id),
        )

    @staticmethod
    def update_boat(id: int, name: str, boat_class_id: Optional[int]):
        return Base.custom_update(
            "UPDATE rowing_boats SET name = %s, boat_class_id = %s WHERE id = %s",
            (name, boat_class_id, id),
        )

    @staticmethod
    def delete_boat(id: int):
        return Base.custom_update(
            "UPDATE rowing_boats SET deleted_at = NOW() WHERE id = %s",
            (id,),
        )

    # ── Crews ──────────────────────────────────────────────────────────────

    @staticmethod
    def fetch_crews():
        return Base.custom_query(
            f"{_CREW_BASE_SQL} WHERE cr.deleted_at IS NULL ORDER BY b.name ASC, cr.created_at DESC"
        )

    @staticmethod
    def fetch_crew(crew_id: int):
        return Base.single_query(
            f"{_CREW_BASE_SQL} WHERE cr.id = %s AND cr.deleted_at IS NULL",
            (crew_id,),
        )

    @staticmethod
    def create_crew(boat_id: int, gender: str, age_category: str,
                    cox: Optional[int], seat_1: Optional[int], seat_2: Optional[int],
                    seat_3: Optional[int], seat_4: Optional[int], seat_5: Optional[int],
                    seat_6: Optional[int], seat_7: Optional[int], seat_8: Optional[int]):
        return Base.custom_insert(
            """
            INSERT INTO rowing_crews
                (boat_id, gender, age_category, cox, seat_1, seat_2, seat_3, seat_4, seat_5, seat_6, seat_7, seat_8)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (boat_id, gender, age_category, cox, seat_1, seat_2, seat_3, seat_4, seat_5, seat_6, seat_7, seat_8),
        )

    @staticmethod
    def update_crew(crew_id: int, boat_id: int, gender: str, age_category: str,
                    cox: Optional[int], seat_1: Optional[int], seat_2: Optional[int],
                    seat_3: Optional[int], seat_4: Optional[int], seat_5: Optional[int],
                    seat_6: Optional[int], seat_7: Optional[int], seat_8: Optional[int]):
        return Base.custom_update(
            """
            UPDATE rowing_crews SET
                boat_id = %s, gender = %s, age_category = %s,
                cox = %s, seat_1 = %s, seat_2 = %s, seat_3 = %s, seat_4 = %s,
                seat_5 = %s, seat_6 = %s, seat_7 = %s, seat_8 = %s
            WHERE id = %s
            """,
            (boat_id, gender, age_category, cox, seat_1, seat_2, seat_3, seat_4, seat_5, seat_6, seat_7, seat_8, crew_id),
        )

    @staticmethod
    def crew_has_results(crew_id: int) -> bool:
        row = Base.single_query(
            """
            SELECT COUNT(*) AS count FROM rowing_race_entries e
            JOIN rowing_races r ON e.race_id = r.id
            WHERE e.crew_id = %s
            AND (e.elapsed_ms IS NOT NULL OR e.dns = 1 OR e.dnf = 1)
            AND r.deleted_at IS NULL AND e.deleted_at IS NULL
            """,
            (crew_id,),
        )
        return (row["count"] if row else 0) > 0

    @staticmethod
    def delete_crew(crew_id: int):
        return Base.custom_update(
            "UPDATE rowing_crews SET deleted_at = NOW() WHERE id = %s",
            (crew_id,),
        )

    # ── Races ──────────────────────────────────────────────────────────────

    @staticmethod
    def fetch_races(date: str):
        return Base.custom_query(
            """
            SELECT id, distance, race_type AS raceType, event_type AS eventType,
                   wind_conditions AS windConditions, notes, status,
                   created_at AS createdAt, completed_at AS completedAt
            FROM rowing_races
            WHERE deleted_at IS NULL AND DATE(created_at) = %s
            ORDER BY created_at DESC
            """,
            (date,),
        )

    @staticmethod
    def fetch_race(id: int):
        return Base.single_query(
            """
            SELECT id, distance, race_type AS raceType, event_type AS eventType,
                   wind_conditions AS windConditions, notes, status,
                   created_at AS createdAt, completed_at AS completedAt
            FROM rowing_races
            WHERE id = %s AND deleted_at IS NULL
            """,
            (id,),
        )

    @staticmethod
    def create_race(distance: str, race_type: str, event_type: Optional[str],
                    wind_conditions: Optional[str], notes: Optional[str]):
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
                e.id, e.race_id AS raceId, e.crew_id AS crewId,
                b.name AS boatName,
                e.start_time AS startTime, e.finish_time AS finishTime,
                e.elapsed_ms AS elapsedMs, e.dns, e.dnf, e.placement,
                cox_m.name AS coxName,
                s1.name AS strokeName,
                bc.has_cox AS boatHasCox
            FROM rowing_race_entries e
            LEFT JOIN rowing_crews cr ON e.crew_id = cr.id
            LEFT JOIN rowing_boats b ON cr.boat_id = b.id
            LEFT JOIN rowing_boat_classes bc ON b.boat_class_id = bc.id
            LEFT JOIN rowing_crew_members cox_m ON cr.cox = cox_m.id
            LEFT JOIN rowing_crew_members s1 ON cr.seat_1 = s1.id
            WHERE e.race_id = %s AND e.deleted_at IS NULL
            ORDER BY e.placement ASC, e.elapsed_ms ASC
            """,
            (race_id,),
        )

    @staticmethod
    def create_entry(race_id: int, crew_id: int):
        return Base.custom_insert(
            "INSERT INTO rowing_race_entries (race_id, crew_id) VALUES (%s, %s)",
            (race_id, crew_id),
        )

    @staticmethod
    def update_entry_crew(entry_id: int, crew_id: int):
        return Base.custom_update(
            "UPDATE rowing_race_entries SET crew_id = %s WHERE id = %s",
            (crew_id, entry_id),
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
