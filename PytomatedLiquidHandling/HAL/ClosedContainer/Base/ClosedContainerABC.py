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

    def ValidateOpenCloseOptions(self, OptionsList: list[OpenCloseOptions]):
        UnsupportedDeckLocations = list()
        UnsupportedLabwares = list()

        for Options in OptionsList:
            DeckLocationInstance = Options.LayoutItem.DeckLocation
            LabwareInstance = Options.LayoutItem.Labware

            if DeckLocationInstance not in self.SupportedDeckLocations:
                UnsupportedDeckLocations.append(DeckLocationInstance)

            if LabwareInstance not in self.SupportedLabwares:
                UnsupportedLabwares.append(LabwareInstance)

        if len(UnsupportedDeckLocations) > 0:
            raise DeckLocation.Base.DeckLocationNotSupportedError(
                UnsupportedDeckLocations
            )

        if len(UnsupportedLabwares) > 0:
            raise Labware.Base.LabwareNotSupportedError(UnsupportedLabwares)

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
