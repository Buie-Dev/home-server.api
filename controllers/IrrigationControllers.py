from services.IrrigationServices import IrrigationServices
from typing import List
from ObjectTypes import Zone


class IrrigationControllers:

    # @staticmethod
    # def schedules():
    #     return IrrigationServices.schedules()

    @staticmethod
    def fetch_zones() -> List[Zone]:
        try:
            return IrrigationServices.fetch_zones()
        except Exception as e:
            print("Error Fetching Zones in Controller", e)
            raise e
