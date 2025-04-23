from services.IrrigationServices import IrrigationServices
from typing import List
from ObjectTypes import Zone, CreateScheduleParams


class IrrigationControllers:

    @staticmethod
    def schedules():
        return IrrigationServices.schedules()

    @staticmethod
    def create_schedule(data: CreateScheduleParams):
        return IrrigationServices.create_schedule(data)

    @staticmethod
    def delete_schedule(id: int):
        return IrrigationServices.delete_schedule(id)

    @staticmethod
    def fetch_zones() -> List[Zone]:
        try:
            return IrrigationServices.fetch_zones()
        except Exception as e:
            print("Error Fetching Zones in Controller", e)
            raise e
