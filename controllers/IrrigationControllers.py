from services.IrrigationServices import IrrigationServices


class IrrigationControllers:

    @staticmethod
    def schedules():
        return IrrigationServices.schedules()
