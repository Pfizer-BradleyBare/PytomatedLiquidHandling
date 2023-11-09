from abc import abstractmethod
from dataclasses import dataclass

from pydantic import PrivateAttr, field_validator

from PytomatedLiquidHandling.HAL import LayoutItem
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALDevice

from ...Tools.AbstractClasses import Interface


@dataclass
class AvailablePosition:
    LabwareID: str
    PositionID: str


class TipABC(Interface, HALDevice):
    TipRackLayoutItems: list[LayoutItem.TipRack]
    Volume: float
    _AvailablePositions: list[AvailablePosition] = PrivateAttr(default_factory=list)

    @field_validator("TipRacks", mode="before")
    def __TipRacksValidate(cls, v):
        SupportedObjects = list()

        Objects = LayoutItem.Devices

        for Identifier in v:
            if Identifier not in Objects:
                raise ValueError(
                    Identifier
                    + " is not found in "
                    + LayoutItem.Base.LayoutItemABC.__name__
                    + " objects."
                )

            SupportedObjects.append(Objects[Identifier])

        return SupportedObjects

    def _ParseAvailablePositions(self, AvailablePositions: list[dict[str, str]]):
        for Pos in AvailablePositions:
            self._AvailablePositions.append(
                AvailablePosition(Pos["LabwareID"], Pos["PositionID"])
            )

    def Initialize(self):
        Interface.Initialize(self)
        self.TipCounterEdit()

    def RemainingTips(self) -> int:
        """Total number of tips.
        NOTE: This is not guarenteed to be the number of accessible tips. Call RemainingTipsInTier for that info.
        """
        return len(self._AvailablePositions)

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
