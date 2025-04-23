from models.Base import Base
from typing import List, TypedDict
from ObjectTypes import ModelZone, Subzone, CreateScheduleParams


class IrrigationModels:

    @staticmethod
    def schedules():
        connection = Base.get_connection()
        sql = """
            SELECT 
                id, 
                name,
                TIME_FORMAT(start_time, '%H:%i') AS startTime, 
                duration,
                monday,
                tuesday,
                wednesday,
                thursday,
                friday,
                saturday,
                sunday 
            FROM schedules 
            WHERE deleted_at IS NULL
        """

        print(sql)
        return Base.custom_query(sql, connection=connection)

    @staticmethod
    def create_schedule(params: CreateScheduleParams):
        connection = Base.get_connection()
        sql = """
            INSERT INTO schedules (start_time, name, duration, monday, tuesday, wednesday, thursday, friday, saturday, sunday) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        print(sql)

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
        )
        print(data)
        return Base.custom_insert(sql, connection=connection, params=data)

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
    def fetch_subzones() -> List[Subzone]:
        connection = Base.get_connection()
        sql = "SELECT id, name, zone_id, subzone FROM garden_zones WHERE active = 1"
        return Base.custom_query(sql, connection=connection)
