from models.IrrigationModels import IrrigationModels
from lib.irrigation import create_automation_command
from ObjectTypes import (
    Zone,
    CreateScheduleParams,
    AutomationCommand,
    ToggleScheduleParams,
    ZoneType,
)
from typing import List, Optional
import json


class IrrigationServices:

    @staticmethod
    def schedules():
        return IrrigationModels.schedules()

    @staticmethod
    def create_schedule(params: CreateScheduleParams):
        schedule_data = {
            "duration": params["duration"],
            "name": params["name"],
            "start_time": params["start_time"],
            "monday": params["monday"],
            "tuesday": params["tuesday"],
            "wednesday": params["wednesday"],
            "thursday": params["thursday"],
            "friday": params["friday"],
            "saturday": params["saturday"],
            "sunday": params["sunday"],
            "zone_id": params["zone_id"],
        }

        schedule_result = IrrigationModels.create_schedule(schedule_data)
        schedule_id = schedule_result["inserted_id"]

        if len(params["subzone_ids"]) > 0:
            IrrigationModels.create_subzone_schedules(
                schedule_id, params["subzone_ids"]
            )

        return schedule_id

    @staticmethod
    def delete_schedule(id: int):
        return IrrigationModels.delete_schedule(id)

    @staticmethod
    def fetch_zones(zone_type_id: Optional[int] = None) -> List[Zone]:
        try:

            zones_model = IrrigationModels.fetch_zones(zone_type_id)
            subzones = IrrigationModels.fetch_subzones()

            zones: List[Zone] = [
                {
                    "id": zm["id"],
                    "name": zm["name"],
                    "zone": zm["zone"],
                    "type": zm["type"],
                }
                for zm in zones_model
            ]
            for subzone in subzones:
                zone_id = subzone["zone_id"]
                zone = next((zone for zone in zones if zone["id"] == zone_id), None)
                if zone is None:
                    continue
                if "subzones" not in zone or zone["subzones"] is None:
                    zone["subzones"] = []

                zone["subzones"].append(subzone)

            return zones
        except Exception as e:
            print(e)
            print("Error Fetching Zones in Service", e)
            raise e

    @staticmethod
    def fetch_zone(id: int) -> Zone:
        try:

            zone_model = IrrigationModels.fetch_zone(id)
            subzones = IrrigationModels.fetch_subzones(id)

            zone: Zone = {
                "id": zone_model["id"],
                "name": zone_model["name"],
                "zone": zone_model["zone"],
                "subzones": subzones,
            }

            return zone
        except Exception as e:
            print(e)
            print("Error Fetching Zones in Service", e)
            raise e

    @staticmethod
    def fetch_automation_schedule(id: int) -> AutomationCommand:
        automation_schedule = IrrigationModels.fetch_automation_schedule(id)
        automation_schedule_formatted = {
            **automation_schedule,
            "subzone_ids": json.loads(automation_schedule["subzone_ids"]),
        }
        zone = IrrigationServices.fetch_zone(automation_schedule["zone_id"])
        return create_automation_command(zone, automation_schedule_formatted, id)

    @staticmethod
    def fetch_automation_schedules() -> List[AutomationCommand]:
        automation_schedules = IrrigationModels.fetch_automation_schedules()
        automation_schedules_formatted = [
            {
                **automation_schedule,
                "subzone_ids": json.loads(automation_schedule["subzone_ids"]),
            }
            for automation_schedule in automation_schedules
        ]

        return [
            create_automation_command(
                IrrigationServices.fetch_zone(automation_schedule["zone_id"]),
                automation_schedule,
                automation_schedule["id"],
            )
            for automation_schedule in automation_schedules_formatted
        ]

    @staticmethod
    def toggle_schedule(id: int, data: ToggleScheduleParams):
        return IrrigationModels.toggle_schedule(id, data)

    @staticmethod
    def fetch_zone_types() -> List[ZoneType]:
        return IrrigationModels.fetch_zone_types()
