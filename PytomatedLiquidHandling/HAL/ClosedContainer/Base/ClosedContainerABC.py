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
        """Must be called before calling Open, OpenTime, Close, or CloseTime.

        If LabwareNotSupportedError is thrown then you are trying to use the wrong ClosedContainerDevice.

        If DeckLocationNotSupportedError is thrown then you need to move the LayoutItem to a compatible location.

        Raises ExceptionGroup of the following:
            Labware.Base.LabwareNotSupportedError

            DeckLocation.Base.DeckLocationNotSupportedError
        """

        Exceptions = list()

        UnsupportedDeckLocations = list()
        UnsupportedLabwares = list()

        for Options in OptionsList:
            DeckLocationInstance = Options.LayoutItem.DeckLocation
            LabwareInstance = Options.LayoutItem.Labware

            if DeckLocationInstance not in self.SupportedDeckLocations:
                UnsupportedDeckLocations.append(DeckLocationInstance)

            if LabwareInstance not in self.SupportedLabwares:
                UnsupportedLabwares.append(LabwareInstance)

        if len(UnsupportedLabwares) > 0:
            Exceptions.append(
                Labware.Base.LabwareNotSupportedError(UnsupportedLabwares)
            )

        if len(UnsupportedDeckLocations) > 0:
            Exceptions.append(
                DeckLocation.Base.DeckLocationNotSupportedError(
                    UnsupportedDeckLocations
                )
            )

        if len(Exceptions) > 0:
            raise ExceptionGroup(
                "ClosedContainer OpenCloseOptions Exceptions", Exceptions
            )

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
