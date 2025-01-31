from models.IrrigationModels import IrrigationModels


class IrrigationServices:

    @staticmethod
    def schedules():
        return IrrigationModels.schedules()
