from models.Base import Base


class DeviceModels:
    @staticmethod
    def fetch_devices():
        return Base.custom_query(
            """
            SELECT
                id,
                name,
                identifier,
                type
            FROM devices
            """
        )

    @staticmethod
    def get_device_by_sensor(sensor: str):
        return Base.single_query("SELECT id FROM devices WHERE identifier = %s", (sensor,))

    @staticmethod
    def create_battery_log(device_id: int, voltage: float, current: float, power: float, state: str):
        return Base.custom_insert(
            """
            INSERT INTO battery_logs (device_id, voltage, current, power, state)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (device_id, voltage, current, power, state),
        )
