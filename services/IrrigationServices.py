from models.IrrigationModels import IrrigationModels
from ObjectTypes import Zone, CreateScheduleParams
from typing import List


class IrrigationServices:

    @staticmethod
    def schedules():
        return IrrigationModels.schedules()

    @staticmethod
    def create_schedule(params: CreateScheduleParams):
        return IrrigationModels.create_schedule(params)

    @staticmethod
    def delete_schedule(id: int):
        return IrrigationModels.delete_schedule(id)

    @staticmethod
    def fetch_zones() -> List[Zone]:
        try:

            zones_model = IrrigationModels.fetch_zones()
            subzones = IrrigationModels.fetch_subzones()

            zones: List[Zone] = [
                {"id": zm["id"], "name": zm["name"], "zone": zm["zone"]}
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
