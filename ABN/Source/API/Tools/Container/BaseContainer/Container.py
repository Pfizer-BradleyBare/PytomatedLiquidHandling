from abc import abstractmethod

from .....Tools.AbstractClasses import ObjectABC
from ..Plate.Well.WellSolution.WellSolutionTracker import WellSolutionTracker
from .LiquidClassCategory.LiquidClassCategory import LiquidClassCategory


class Container(ObjectABC):
    def __init__(self, Name: str, MethodName: str, Filter: str):
        self.Name: str = Name
        self.MethodName: str = MethodName
        self.Filter: list[str] = [Filter]

    def GetName(self) -> str:
        return self.Name

    def GetMethodName(self) -> str:
        return self.MethodName

    def GetFilter(self) -> list[str]:
        return self.Filter

    @abstractmethod
    def GetVolume(self) -> float:
        ...

    @abstractmethod
    def GetLiquidClassCategory(self) -> LiquidClassCategory:
        ...

    @abstractmethod
    def Aspirate(self, WellNumber: int, Volume: float) -> WellSolutionTracker:
        ...

    @abstractmethod
    def Dispense(
        self, WellNumber: int, WellSolutionTrackerInstance: WellSolutionTracker
    ):
        ...
