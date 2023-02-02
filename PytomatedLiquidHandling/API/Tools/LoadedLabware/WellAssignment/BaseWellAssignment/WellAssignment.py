from abc import abstractmethod

from ......Tools.AbstractClasses import ObjectABC
from .....Tools.Container import Container


class WellAssignment(ObjectABC):
    def __init__(self, PhysicalWellNumber: int, ContainerInstance: Container):
        self.PhysicalWellNumber: int = PhysicalWellNumber
        self.ContainerInstance: Container = ContainerInstance
        self.MeasuredVolume: float = 0

    def GetName(self) -> int:
        return self.PhysicalWellNumber

    @abstractmethod
    def TestAsignment(self, ContainerInstance: Container, WellNumber: int) -> bool:
        ...

    @abstractmethod
    def GetAssignment(self) -> str:
        ...

    def GetMeasuredVolume(self) -> float:
        return self.MeasuredVolume

    def UpdateMeasuredVolume(self, NewVolume: float):
        self.MeasuredVolume = NewVolume
