from typing import List, Optional

from lib.dates import get_vancouver_date_context
from models.Base import Base
from ObjectTypes import (
    AutomationSchedule,
    CreateScheduleParams,
    ModelZone,
    Subzone,
    ToggleScheduleParams,
    ZoneType,
)


class IrrigationModels:
    @staticmethod
    def schedules(zone_id: Optional[int] = None, subzone_id: Optional[int] = None):
        connection = Base.get_connection()
        sql = """
            SELECT
                s.id,
                s.name,
                TIME_FORMAT(s.start_time, '%%H:%%i') AS startTime,
                s.duration,
                s.monday,
                s.tuesday,
                s.wednesday,
                s.thursday,
                s.friday,
                s.saturday,
                s.sunday,
                s.zone_id,
                z.name AS zoneName,
                GROUP_CONCAT(sz.name) AS subzoneNames,
                JSON_ARRAYAGG(ss.subzone_id) AS subzoneIds,
                s.active,
                s.sort_order
            FROM schedules AS s
            LEFT JOIN subzone_schedules AS ss ON s.id = ss.schedule_id
            LEFT JOIN subzones AS sz ON ss.subzone_id = sz.id
            JOIN zones AS z ON s.zone_id = z.id
            WHERE s.deleted_at IS NULL
        """
        params = []
        if zone_id is not None:
            sql += " AND s.zone_id = %s"
            params.append(zone_id)
        if subzone_id is not None:
            sql += (
                " AND EXISTS (SELECT 1 FROM subzone_schedules ss2 WHERE ss2.schedule_id = s.id AND ss2.subzone_id = %s)"
            )
            params.append(subzone_id)
        sql += " GROUP BY s.id, s.zone_id ORDER BY s.sort_order ASC"

        return Base.custom_query(sql, params, connection=connection)

    @staticmethod
    def create_schedule(params: CreateScheduleParams):
        connection = Base.get_connection()
        sql = """
            INSERT INTO schedules (start_time, name, duration, monday, tuesday, wednesday, thursday, friday, saturday, sunday, zone_id, sort_order)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    (SELECT COALESCE(MAX(s2.sort_order), 0) + 1 FROM schedules s2 WHERE s2.deleted_at IS NULL))"""

        data = (
            params["start_time"],
            params["name"],
            params["duration"],
            params["monday"],
            params["tuesday"],
            params["wednesday"],
            params["thursday"],
            params["friday"],
            params["saturday"],
            params["sunday"],
            params["zone_id"],
        )
        return Base.custom_insert(sql, connection=connection, params=data)

    @staticmethod
    def create_subzone_schedules(schedule_id: int, subzone_ids: List[int]):
        connection = Base.get_connection()
        # Create placeholders for each subzone_id
        placeholders = ",".join(["(%s,%s)"] * len(subzone_ids))
        sql = f"""
            INSERT INTO subzone_schedules (schedule_id, subzone_id)
            VALUES {placeholders}
        """
        # Create a flat list of parameters (schedule_id, subzone_id) for each subzone
        params = [param for subzone_id in subzone_ids for param in (schedule_id, subzone_id)]
        return Base.custom_insert(sql, params=params, connection=connection)

    @staticmethod
    def update_schedule(id: int, params):
        connection = Base.get_connection()
        sql = """
            UPDATE schedules
            SET name=%s, start_time=%s, duration=%s,
                monday=%s, tuesday=%s, wednesday=%s, thursday=%s, friday=%s, saturday=%s, sunday=%s,
                zone_id=%s
            WHERE id=%s
        """
        data = (
            params["name"],
            params["start_time"],
            params["duration"],
            params["monday"],
            params["tuesday"],
            params["wednesday"],
            params["thursday"],
            params["friday"],
            params["saturday"],
            params["sunday"],
            params["zone_id"],
            id,
        )
        return Base.custom_delete(sql, params=data, connection=connection)

    @staticmethod
    def delete_subzone_schedules(schedule_id: int):
        connection = Base.get_connection()
        sql = "DELETE FROM subzone_schedules WHERE schedule_id = %s"
        return Base.custom_delete(sql, params=(schedule_id,), connection=connection)

    @staticmethod
    def delete_schedule(id: int):
        sql = """
            UPDATE schedules SET deleted_at = NOW() WHERE id = %s
        """
        return Base.custom_delete(sql, params=(id))

    @staticmethod
    def fetch_zones(zone_type_id: Optional[int] = None) -> List[ModelZone]:
        connection = Base.get_connection()
        params = []
        sql = """
            SELECT
                z.id,
                z.name,
                z.zone,
                zt.type
            FROM zones AS z
            JOIN zone_types AS zt ON z.zone_type_id = zt.id
            WHERE active = 1
        """
        if zone_type_id:
            sql += " AND zone_type_id = %s"
            params.append(zone_type_id)
        sql += " ORDER BY sort_order ASC"
        return Base.custom_query(sql, params=params, connection=connection)

    @staticmethod
    def fetch_zone(id: int) -> ModelZone:
        connection = Base.get_connection()
        sql = "SELECT id, name, zone FROM zones WHERE id = %s"
        return Base.single_query(sql, params=(id), connection=connection)

    @staticmethod
    def fetch_subzones(zone_id: Optional[int] = None) -> List[Subzone]:
        connection = Base.get_connection()
        params = []
        sql = "SELECT id, name, zone_id, subzone, heads FROM subzones WHERE active = 1"
        if zone_id:
            sql += " AND zone_id = %s"
            params.append(zone_id)
        return Base.custom_query(sql, params=params, connection=connection)

    @staticmethod
    def fetch_subzones_by_ids(ids: List[int]) -> List[Subzone]:
        connection = Base.get_connection()
        placeholders = ",".join(["%s"] * len(ids))
        sql = f"SELECT id, name, zone_id, subzone, heads FROM subzones WHERE active = 1 AND id IN ({placeholders})"
        return Base.custom_query(sql, params=ids, connection=connection)

    @staticmethod
    def fetch_automation_schedule(id: int) -> AutomationSchedule:
        connection = Base.get_connection()
        params = [id]
        sql = """
            SELECT
                s.id,
                zone_id,
                monday,
                tuesday,
                wednesday,
                thursday,
                friday,
                saturday,
                sunday,
                TIME_FORMAT(start_time, '%%H:%%i') AS start_time,
                duration,
                sort_order,
                JSON_ARRAYAGG(ss.subzone_id) AS subzone_ids
            FROM schedules AS s
            LEFT JOIN subzone_schedules AS ss ON s.id = ss.schedule_id
            WHERE s.id = %s
            GROUP BY s.id, s.zone_id
            """
        return Base.single_query(sql, params=params, connection=connection)

    @staticmethod
    def fetch_automation_schedules(exclude_inactive=False, include_deleted=False) -> List[AutomationSchedule]:
        connection = Base.get_connection()
        conditions = []
        if not include_deleted:
            conditions.append("deleted_at IS NULL")
        if exclude_inactive:
            conditions.append("active = 1")
        where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""
        sql = f"""
            SELECT
                s.id,
                zone_id,
                monday,
                tuesday,
                wednesday,
                thursday,
                friday,
                saturday,
                sunday,
                TIME_FORMAT(start_time, '%H:%i') AS start_time,
                duration,
                sort_order,
                JSON_ARRAYAGG(ss.subzone_id) AS subzone_ids
            FROM schedules AS s
            LEFT JOIN subzone_schedules AS ss ON s.id = ss.schedule_id
            {where_clause}
            GROUP BY s.id, s.zone_id
            ORDER BY s.sort_order ASC
            """
        return Base.custom_query(sql, connection=connection)

    @staticmethod
    def fetch_active_automation_schedules() -> List[AutomationSchedule]:
        connection = Base.get_connection()
        sql = """
            SELECT
                s.id,
                zone_id,
                monday,
                tuesday,
                wednesday,
                thursday,
                friday,
                saturday,
                sunday,
                TIME_FORMAT(start_time, '%H:%i') AS start_time,
                duration,
                sort_order,
                JSON_ARRAYAGG(ss.subzone_id) AS subzone_ids
            FROM schedules AS s
            LEFT JOIN subzone_schedules AS ss ON s.id = ss.schedule_id
            WHERE deleted_at IS NULL AND active = 1
            GROUP BY s.id, s.zone_id
            ORDER BY s.sort_order ASC
            """
        return Base.custom_query(sql, connection=connection)

    @staticmethod
    def reorder_schedules(ids: List[int]):
        connection = Base.get_connection()
        when_clauses = " ".join(["WHEN %s THEN %s"] * len(ids))
        id_placeholders = ", ".join(["%s"] * len(ids))
        sql = f"""
            UPDATE schedules
            SET sort_order = CASE id {when_clauses} END
            WHERE id IN ({id_placeholders})
        """
        params = []
        for i, schedule_id in enumerate(ids):
            params.extend([schedule_id, i + 1])
        params.extend(ids)
        return Base.custom_update(sql, params=params, connection=connection)

    @staticmethod
    def is_schedule_active(id: int) -> bool:
        connection = Base.get_connection()
        sql = "SELECT active FROM schedules WHERE id = %s AND deleted_at IS NULL"
        row = Base.single_query(sql, params=[id], connection=connection)
        return bool(row and row.get("active"))

    @staticmethod
    def toggle_schedule(id: int, data: ToggleScheduleParams):
        connection = Base.get_connection()
        sql = """
            UPDATE schedules SET active = %s WHERE id = %s
        """
        params = (data["active"], id)
        return Base.custom_update(sql, params=params, connection=connection)

    @staticmethod
    def fetch_zone_types() -> List[ZoneType]:
        connection = Base.get_connection()
        sql = "SELECT id, type FROM zone_types"
        return Base.custom_query(sql, connection=connection)

    @staticmethod
    def fetch_history(
        limit: int = 100,
        offset: int = 0,
        zone_id: int = None,
        subzone_id: int = None,
        start_date: str = None,
        end_date: str = None,
    ):
        connection = Base.get_connection()
        params = []
        sql = """
            SELECT
                h.id,
                z.name AS zone_name,
                zt.type AS zone_type,
                sz.name AS subzone_name,
                h.litres,
                h.date,
                h.start_time,
                h.end_time
            FROM irrigation_history AS h
            LEFT JOIN zones AS z ON h.zone_id = z.zone
            LEFT JOIN zone_types AS zt ON z.zone_type_id = zt.id
            LEFT JOIN subzones AS sz ON h.subzone_id = sz.id
            WHERE h.deleted_at IS NULL
        """
        if zone_id is not None:
            sql += " AND z.id = %s"
            params.append(zone_id)
        if subzone_id is not None:
            sql += " AND sz.id = %s"
            params.append(subzone_id)
        if start_date is not None:
            sql += " AND h.date >= %s"
            params.append(start_date)
        if end_date is not None:
            sql += " AND h.date <= %s"
            params.append(end_date)
        sql += " ORDER BY h.date DESC, h.start_time DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        return Base.custom_query(sql, params=params, connection=connection)

    @staticmethod
    def fetch_history_totals(zone_id: int = None, subzone_id: int = None):
        dc = get_vancouver_date_context()
        connection = Base.get_connection()
        params = [
            dc["today"],
            dc["today"],
            dc["today"],
            dc["week_ago"],
            dc["week_ago"],
            dc["week_ago"],
            dc["year"],
            dc["month"],
            dc["year"],
            dc["month"],
            dc["year"],
            dc["month"],
        ]
        sql = """
            SELECT
                COALESCE(SUM(CASE WHEN h.date = %s THEN h.litres ELSE 0 END), 0) AS today_litres,
                COALESCE(SUM(CASE WHEN h.date = %s THEN TIME_TO_SEC(h.end_time) - TIME_TO_SEC(h.start_time) ELSE 0 END), 0) AS today_seconds,
                COALESCE(COUNT(CASE WHEN h.date = %s THEN 1 END), 0) AS today_runs,
                COALESCE(SUM(CASE WHEN h.date >= %s THEN h.litres ELSE 0 END), 0) AS week_litres,
                COALESCE(SUM(CASE WHEN h.date >= %s THEN TIME_TO_SEC(h.end_time) - TIME_TO_SEC(h.start_time) ELSE 0 END), 0) AS week_seconds,
                COALESCE(COUNT(CASE WHEN h.date >= %s THEN 1 END), 0) AS week_runs,
                COALESCE(SUM(CASE WHEN YEAR(h.date) = %s AND MONTH(h.date) = %s THEN h.litres ELSE 0 END), 0) AS month_litres,
                COALESCE(SUM(CASE WHEN YEAR(h.date) = %s AND MONTH(h.date) = %s THEN TIME_TO_SEC(h.end_time) - TIME_TO_SEC(h.start_time) ELSE 0 END), 0) AS month_seconds,
                COALESCE(COUNT(CASE WHEN YEAR(h.date) = %s AND MONTH(h.date) = %s THEN 1 END), 0) AS month_runs
            FROM irrigation_history AS h
            LEFT JOIN zones AS z ON h.zone_id = z.zone
            LEFT JOIN subzones AS sz ON h.subzone_id = sz.id
            WHERE h.deleted_at IS NULL
        """
        if zone_id is not None:
            sql += " AND z.id = %s"
            params.append(zone_id)
        if subzone_id is not None:
            sql += " AND sz.id = %s"
            params.append(subzone_id)
        return Base.single_query(sql, params=params, connection=connection)

    @staticmethod
    def delete_history(id: int):
        connection = Base.get_connection()
        sql = "UPDATE irrigation_history SET deleted_at = NOW() WHERE id = %s"
        return Base.custom_delete(sql, params=(id,), connection=connection)

    @staticmethod
    def create_history(params):
        connection = Base.get_connection()
        sql = """
            INSERT INTO irrigation_history (zone_id, subzone_id, litres, date, start_time, end_time)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        data = (
            params.get("zone_id"),
            params.get("subzone_id"),
            params["litres"],
            params["date"],
            params["start_time"],
            params["end_time"],
        )
        return Base.custom_insert(sql, connection=connection, params=data)
