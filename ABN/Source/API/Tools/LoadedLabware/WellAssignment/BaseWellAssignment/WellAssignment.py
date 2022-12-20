from ......Tools.AbstractClasses import ObjectABC


class WellAssignment(ObjectABC):
    def __init__(self, PhysicalWellNumber: int, MethodName: str, LabwareName: str):
        self.PhysicalWellNumber: int = PhysicalWellNumber
        self.Assignment: str = MethodName + " - " + LabwareName
        self.MeasuredVolume: float = 0

    def GetName(self) -> int:
        return self.PhysicalWellNumber

    def GetAssignment(self) -> str:
        return self.Assignment

    def GetMeasuredVolume(self) -> float:
        return self.MeasuredVolume

    def UpdateMeasuredVolume(self, NewVolume: float):
        self.MeasuredVolume = NewVolume
