from abc import abstractmethod
from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC
from PytomatedLiquidHandling.HAL import DeckLocation, Labware, LayoutItem
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject

from ...Tools.AbstractClasses import InterfaceABC


@dataclass(kw_only=True)
class OpenCloseOptions(OptionsABC):
    LayoutItem: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
    Position: int


@dataclass
class ClosedContainerABC(InterfaceABC, HALObject):
    ToolSequence: str
    SupportedDeckLocations: list[DeckLocation.Base.DeckLocationABC]
    SupportedLabwares: list[Labware.Base.LabwareABC]

    def IsDeckLocationSupported(
        self, DeckLocation: DeckLocation.Base.DeckLocationABC
    ) -> bool:
        return DeckLocation in self.SupportedDeckLocations

    def IsLabwareSupported(self, Labware: Labware.PipettableLabware) -> bool:
        return Labware in self.SupportedLabwares

    @abstractmethod
    def Open(self, Options: list[OpenCloseOptions]):
        ...

    @abstractmethod
    def OpenTime(self, Options: list[OpenCloseOptions]) -> float:
        ...

    @abstractmethod
    def Close(self, Options: list[OpenCloseOptions]):
        ...

    @abstractmethod
    def CloseTime(self, Options: list[OpenCloseOptions]) -> float:
        ...
