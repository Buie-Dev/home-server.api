from models.Base import Base
from typing import List, TypedDict, Optional
from ObjectTypes import (
    ModelZone,
    Subzone,
    CreateScheduleParams,
    AutomationSchedule,
    ToggleScheduleParams,
)


class IrrigationModels:

    @staticmethod
    def schedules():
        connection = Base.get_connection()
        sql = """
            SELECT 
                s.id, 
                s.name,
                TIME_FORMAT(s.start_time, '%H:%i') AS startTime, 
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
                s.active
            FROM schedules AS s
            LEFT JOIN subzone_schedules AS ss ON s.id = ss.schedule_id
            LEFT JOIN subzones AS sz ON ss.subzone_id = sz.id
            JOIN zones AS z ON s.zone_id = z.id
            WHERE deleted_at IS NULL
            GROUP BY s.id, s.zone_id
        """

        return Base.custom_query(sql, connection=connection)

    @staticmethod
    def create_schedule(params: CreateScheduleParams):
        connection = Base.get_connection()
        sql = """
            INSERT INTO schedules (start_time, name, duration, monday, tuesday, wednesday, thursday, friday, saturday, sunday, zone_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

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
        params = [
            param for subzone_id in subzone_ids for param in (schedule_id, subzone_id)
        ]
        return Base.custom_insert(sql, params=params, connection=connection)

    @staticmethod
    def delete_schedule(id: int):
        sql = """
            UPDATE schedules SET deleted_at = NOW() WHERE id = %s
        """
        return Base.custom_delete(sql, params=(id))

    @staticmethod
    def fetch_zones() -> List[ModelZone]:
        connection = Base.get_connection()
        sql = "SELECT id, name, zone FROM zones WHERE active = 1"
        return Base.custom_query(sql, connection=connection)

    @staticmethod
    def fetch_zone(id: int) -> ModelZone:
        connection = Base.get_connection()
        sql = "SELECT id, name, zone FROM zones WHERE id = %s"
        return Base.single_query(sql, params=(id), connection=connection)

    @staticmethod
    def fetch_subzones(zone_id: Optional[int] = None) -> List[Subzone]:
        connection = Base.get_connection()
        params = []
        sql = "SELECT id, name, zone_id, subzone FROM subzones WHERE active = 1"
        if zone_id:
            sql += " AND zone_id = %s"
            params.append(zone_id)
        return Base.custom_query(sql, params=params, connection=connection)

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
                JSON_ARRAYAGG(ss.subzone_id) AS subzone_ids
            FROM schedules AS s
            LEFT JOIN subzone_schedules AS ss ON s.id = ss.schedule_id
            WHERE s.id = %s
            GROUP BY s.id, s.zone_id
            """
        return Base.single_query(sql, params=params, connection=connection)

    @staticmethod
    def fetch_automation_schedules() -> List[AutomationSchedule]:
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
                JSON_ARRAYAGG(ss.subzone_id) AS subzone_ids
            FROM schedules AS s
            LEFT JOIN subzone_schedules AS ss ON s.id = ss.schedule_id
            WHERE deleted_at IS NULL
            GROUP BY s.id, s.zone_id
            """
        return Base.custom_query(sql, connection=connection)

    @staticmethod
    def toggle_schedule(id: int, data: ToggleScheduleParams):
        connection = Base.get_connection()
        sql = """
            UPDATE schedules SET active = %s WHERE id = %s
        """
        params = (data["active"], id)
        return Base.custom_update(sql, params=params, connection=connection)
