from services.IrrigationServices import IrrigationServices
from typing import List, Optional
from ObjectTypes import (
    Zone,
    CreateScheduleParams,
    AutomationCommand,
    ToggleScheduleParams,
    ZoneType,
)
from mqtt import mqtt
from lib.irrigation import create_automation_command
import json

mqtt_client = mqtt.run_mqtt()


class IrrigationControllers:

    @staticmethod
    def schedules():
        return IrrigationServices.schedules()

    @staticmethod
    def create_schedule(data: CreateScheduleParams):

        schedule_id = IrrigationServices.create_schedule(data)
        zone = IrrigationServices.fetch_zone(data["zone_id"])
        automation_command = create_automation_command(zone, data, schedule_id)
        mqtt.publish_add_schedule(mqtt_client, automation_command)

    @staticmethod
    def delete_schedule(id: int):
        IrrigationServices.delete_schedule(id)
        mqtt.publish_delete_schedule(mqtt_client, id)

    @staticmethod
    def fetch_zones(zone_type_id: Optional[int] = None) -> List[Zone]:
        try:
            return IrrigationServices.fetch_zones(zone_type_id)
        except Exception as e:
            print("Error Fetching Zones in Controller", e)
            raise e

    @staticmethod
    def fetch_automation_schedules() -> List[AutomationCommand]:
        return IrrigationServices.fetch_automation_schedules()

    @staticmethod
    def toggle_schedule(id: int, data: ToggleScheduleParams):

        if data["active"]:
            IrrigationServices.toggle_schedule(id, data)
            automation_command = IrrigationServices.fetch_automation_schedule(id)
            mqtt.publish_add_schedule(mqtt_client, automation_command)
        else:
            IrrigationServices.toggle_schedule(id, data)
            mqtt.publish_delete_schedule(mqtt_client, id)

    @staticmethod
    def fetch_zone_types() -> List[ZoneType]:
        return IrrigationServices.fetch_zone_types()
