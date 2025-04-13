from models.Base import Base
from typing import List, TypedDict
from ObjectTypes import ModelZone, Subzone


class IrrigationModels:

    # @staticmethod
    # def schedules():
    #     connection = Base.get_connection()
    #     sql = "SELECT id, TIME_FORMAT(start_time, '%H:%i') AS start_time, monday, tuesday, wednesday, thursday, friday, saturday, sunday FROM irrigation_schedules"
    #     print(sql)
    #     return Base.custom_query(sql, connection=connection)

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
