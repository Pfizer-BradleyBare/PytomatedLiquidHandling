from abc import abstractmethod
from dataclasses import dataclass, field

from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject

from ...Tools.AbstractClasses import InterfaceABC


@dataclass
class TipABC(InterfaceABC, HALObject):
    PickupSequence: str
    MaxVolume: float

    def Initialize(self):
        InterfaceABC.Initialize(self)
        self.TipCounterEdit()

    def IsVolumeSupported(self, Volume: float):
        return Volume <= self.MaxVolume

    @abstractmethod
    def TipCounterEdit(self):
        ...

    @abstractmethod
    def GetTipPositions(self, Num: int) -> list[int]:
        ...

    @abstractmethod
    def GetRemainingTips(self) -> int:
        ...
