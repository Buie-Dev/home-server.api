from services.DeviceServices import DeviceServices


class DeviceControllers:

    @staticmethod
    def fetch_devices():
        return DeviceServices.fetch_devices()

    @staticmethod
    def create_battery_log(data: dict):
        return DeviceServices.create_battery_log(data)
