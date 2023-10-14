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
        """Creates an interface for the user to physically edit the number of tips currently available."""
        ...

    @abstractmethod
    def GetTotalRemainingTips(self) -> int:
        """Returns number of remaining tips in total."""
        ...

    @abstractmethod
    def GetRemainingSequencePositions(self) -> list[int]:
        """Returns number of remaining positions in the currently accessible layer.
        If len(GetRemainingSequencePositions) and GetTotalRemainingTips are equal. This this tip type is not stacked.
        NOTE: This is not guarenteed to be consecutive.
        """
        ...

    @abstractmethod
    def GetNextTipLayer(self):
        """Discards the currently accessible layer and makes the following layer accessible."""
        ...
