from models.DeviceModels import DeviceModels


class DeviceServices:
    @staticmethod
    def fetch_devices():
        rows = DeviceModels.fetch_devices()
        return [
            {
                "id": row["identifier"],
                "name": row["name"],
                "description": row.get("description", ""),
                "type": row["type"],
                "healthCheckResponse": row["identifier"],
            }
            for row in rows
        ]

    @staticmethod
    def create_battery_log(data: dict):
        device = DeviceModels.get_device_by_sensor(data["sensor"])
        if not device:
            raise ValueError(f"No device found with sensor name: {data['sensor']}")
        return DeviceModels.create_battery_log(
            device_id=device["id"],
            voltage=data["voltage"],
            current=data["current"],
            power=data["power"],
            state=data["state"],
        )
