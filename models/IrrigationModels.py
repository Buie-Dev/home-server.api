from models.Base import Base


class IrrigationModels:

    @staticmethod
    def schedules():
        connection = Base.get_connection()
        sql = "SELECT id, TIME_FORMAT(start_time, '%H:%i') AS start_time, monday, tuesday, wednesday, thursday, friday, saturday, sunday FROM irrigation_schedules"
        print(sql)
        return Base.custom_query(sql, connection=connection)
