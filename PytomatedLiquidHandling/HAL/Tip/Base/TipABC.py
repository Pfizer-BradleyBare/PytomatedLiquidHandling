from abc import abstractmethod
from dataclasses import dataclass, field

from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject

from ...Tools.AbstractClasses import InterfaceABC


@dataclass
class AvailablePosition:
    LabwareID: str
    PositionID: str


@dataclass
class TipABC(InterfaceABC, HALObject):
    RackLabwareIDs: list[str]
    MaxVolume: float
    AvailablePositions: list[AvailablePosition] = field(
        init=False, default_factory=list
    )

    def _ParseAvailablePositions(self, AvailablePositions: list[dict[str, str]]):
        for Pos in AvailablePositions:
            self.AvailablePositions.append(
                AvailablePosition(Pos["LabwareID"], Pos["PositionID"])
            )

    def Initialize(self):
        InterfaceABC.Initialize(self)
        self.TipCounterEdit()

    def RemainingTips(self) -> int:
        """Total number of tips.
        NOTE: This is not guarenteed to be the number of accessible tips. Call RemainingTipsInTier for that info.
        """
        return len(self.AvailablePositions)

    @abstractmethod
    def RemainingTipsInTier(self) -> int:
        """Total number of accessible tips."""
        ...

    @abstractmethod
    def DiscardTierLayerToWaste(self):
        """For stacked tips, discards the uppermost layer to make the next layer accessible.

        For non-stacked tips, should probably request a tip reload from the user.
        """
        ...

    @abstractmethod
    def TipCounterEdit(self):
        """Creates an interface for the user to physically edit the number of tips currently available."""
        ...
