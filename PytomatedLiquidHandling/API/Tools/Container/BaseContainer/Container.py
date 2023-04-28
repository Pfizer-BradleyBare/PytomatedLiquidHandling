from abc import abstractmethod

from .....Tools.AbstractClasses import UniqueObjectABC
from ....Tools.LoadedLabware import LoadedLabware
from ..Plate.Well.WellSolution.WellSolutionTracker import WellSolutionTracker
from .LiquidClassCategory.LiquidClassCategory import LiquidClassCategory


class Container(UniqueObjectABC):
    def __init__(self, Name: str, Filter: str):
        self.Name: str = Name
        self.Filter: list[str] = [Filter]
        self.LoadedLabwareInstance: LoadedLabware | None = None

    def GetName(self) -> str:
        return self.Name

    def GetFilter(self) -> list[str]:
        return self.Filter

    @abstractmethod
    def GetVolume(self) -> float:
        ...

    @abstractmethod
    def GetLiquidClassCategory(self, WellNumber: int) -> LiquidClassCategory:
        ...

    @abstractmethod
    def Aspirate(self, WellNumber: int, Volume: float) -> WellSolutionTracker:
        ...

    @abstractmethod
    def Dispense(
        self, WellNumber: int, WellSolutionTrackerInstance: WellSolutionTracker
    ):
        ...
