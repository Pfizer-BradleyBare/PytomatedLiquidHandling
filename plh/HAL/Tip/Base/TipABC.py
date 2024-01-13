from abc import abstractmethod
from dataclasses import field

from pydantic import dataclasses, field_validator

from PytomatedLiquidHandling.HAL import LayoutItem
from PytomatedLiquidHandling.HAL.Tools.BaseClasses import HALDevice

from ...Tools.BaseClasses import Interface


@dataclasses.dataclass(kw_only=True)
class AvailablePosition:
    LabwareID: str
    PositionID: str


@dataclasses.dataclass(kw_only=True)
class TipABC(Interface, HALDevice):
    TipRacks: list[LayoutItem.TipRack]
    TipsPerRack: int
    Volume: float
    _AvailablePositions: list[AvailablePosition] = field(
        init=False, default_factory=list
    )

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
                AvailablePosition(
                    LabwareID=Pos["LabwareID"], PositionID=Pos["PositionID"]
                )
            )

    def Initialize(self):
        Interface.Initialize(self)

    def GetTips(self, Num: int) -> list[AvailablePosition]:
        if len(self._AvailablePositions) < Num:
            raise Exception("Not enough tips available")

        Tips = self._AvailablePositions[:Num]
        self._AvailablePositions = self._AvailablePositions[Num:]
        return Tips

    def RemainingTips(self) -> int:
        """Total number of tips.
        NOTE: This is not guarenteed to be the number of accessible tips. Call RemainingTipsInTier for that info.
        """
        return len(self._AvailablePositions)

    @abstractmethod
    def UpdateAvailablePositions(self):
        """This initiates a update of the available positions. This is not neccesarily the same as Initialize"""

    @abstractmethod
    def RemainingTipsInTier(self) -> int:
        """Total number of accessible tips."""
        ...

    @abstractmethod
    def DiscardLayerToWaste(self):
        """For stacked tips, discards the uppermost layer to make the next layer accessible.

        For non-stacked tips, should probably request a tip reload from the user.
        """
        ...
