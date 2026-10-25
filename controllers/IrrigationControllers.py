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

mqtt_client = mqtt.run_mqtt()


class IrrigationControllers:
    @staticmethod
    def schedules(zone_id: Optional[int] = None, subzone_id: Optional[int] = None):
        return IrrigationServices.schedules(zone_id, subzone_id)

    @staticmethod
    def create_schedule(data: CreateScheduleParams):

        schedule_id = IrrigationServices.create_schedule(data)
        zone = IrrigationServices.fetch_zone(data["zone_id"])
        automation_command = create_automation_command(zone, data, schedule_id)
        mqtt.publish_add_schedule(mqtt_client, automation_command)

    @staticmethod
    def update_schedule(id: int, data: CreateScheduleParams):
        IrrigationServices.update_schedule(id, data)
        mqtt.publish_delete_schedule(mqtt_client, id)
        if IrrigationServices.is_schedule_active(id):
            automation_command = IrrigationServices.fetch_automation_schedule(id)
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
    def fetch_automation_schedules(exclude_inactive=False) -> List[AutomationCommand]:
        return IrrigationServices.fetch_automation_schedules(exclude_inactive=exclude_inactive)

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
    def check_sync():
        mqtt.request_schedule_status(mqtt_client)
        automation_schedules = mqtt.wait_for_schedule_status(timeout=5)
        if automation_schedules is None:
            return {"error": "No response from automation service", "timeout": True}
        return IrrigationServices.compare_sync(automation_schedules)

    @staticmethod
    def force_sync():
        all_schedules = IrrigationServices.fetch_automation_schedules(include_deleted=True)
        for s in all_schedules:
            mqtt.publish_delete_schedule(mqtt_client, s["id"])
        active_schedules = IrrigationServices.fetch_active_automation_schedules()
        for s in active_schedules:
            mqtt.publish_add_schedule(mqtt_client, s)
        return {"synced": len(active_schedules)}

    @staticmethod
    def reorder_schedules(ids: List[int]):
        IrrigationServices.reorder_schedules(ids)
        for schedule_id in ids:
            try:
                automation_command = IrrigationServices.fetch_automation_schedule(schedule_id)
                mqtt.publish_add_schedule(mqtt_client, automation_command)
            except Exception as e:
                print(f"Failed to republish schedule {schedule_id} after reorder: {e}")

    @staticmethod
    def fetch_zone_types() -> List[ZoneType]:
        return IrrigationServices.fetch_zone_types()

    @staticmethod
    def fetch_history(
        limit: int = 100,
        offset: int = 0,
        zone_id: int = None,
        subzone_id: int = None,
        start_date: str = None,
        end_date: str = None,
    ):
        return IrrigationServices.fetch_history(
            limit=limit, offset=offset, zone_id=zone_id, subzone_id=subzone_id, start_date=start_date, end_date=end_date
        )

    @staticmethod
    def fetch_history_totals(zone_id: int = None, subzone_id: int = None):
        return IrrigationServices.fetch_history_totals(zone_id=zone_id, subzone_id=subzone_id)

    @staticmethod
    def delete_history(id: int):
        return IrrigationServices.delete_history(id)

    @staticmethod
    def create_history(data):
        return IrrigationServices.create_history(data)
