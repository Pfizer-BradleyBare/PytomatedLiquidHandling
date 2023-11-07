from abc import abstractmethod
from dataclasses import dataclass

from pydantic import field_validator

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC
from PytomatedLiquidHandling.HAL import DeckLocation, Labware, LayoutItem
from PytomatedLiquidHandling.HAL.Tools import AbstractClasses


@dataclass(kw_only=True)
class OpenCloseOptions(OptionsABC):
    LayoutItem: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
    Position: str | int


class ClosedContainerABC(AbstractClasses.Interface, AbstractClasses.HALDevice):
    ToolLabwareID: str
    ToolPositionID: str
    SupportedDeckLocations: list[DeckLocation.Base.DeckLocationABC]
    SupportedLabwares: list[Labware.Base.LabwareABC]

    @field_validator("SupportedDeckLocations", mode="before")
    def __SupportedDeckLocationsValidate(cls, v):
        SupportedObjects = list()

        Objects = DeckLocation.Devices

        for Identifier in v:
            if Identifier not in Objects:
                raise ValueError(
                    Identifier
                    + " is not found in "
                    + DeckLocation.Base.DeckLocationABC.__name__
                    + " objects."
                )

            SupportedObjects.append(Objects[Identifier])

        return SupportedObjects

    @field_validator("SupportedLabwares", mode="before")
    def __SupportedLabwaresValidate(cls, v):
        SupportedObjects = list()

        Objects = Labware.Devices

        for Identifier in v:
            if Identifier not in Objects:
                raise ValueError(
                    Identifier
                    + " is not found in "
                    + Labware.Base.LabwareABC.__name__
                    + " objects."
                )

            SupportedObjects.append(Objects[Identifier])

        return SupportedObjects

    def AssertOpenCloseOptions(self, Options: list[OpenCloseOptions]):
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

        for Opt in Options:
            DeckLocationInstance = Opt.LayoutItem.DeckLocation
            LabwareInstance = Opt.LayoutItem.Labware

            if DeckLocationInstance not in self.SupportedDeckLocations:
                UnsupportedDeckLocations.append(DeckLocationInstance)

            if LabwareInstance not in self.SupportedLabwares:
                UnsupportedLabwares.append(LabwareInstance)

        if len(UnsupportedLabwares) > 0:
            Exceptions.append(
                Labware.Base.Exceptions.LabwareNotSupportedError(UnsupportedLabwares)
            )

        if len(UnsupportedDeckLocations) > 0:
            Exceptions.append(
                DeckLocation.Base.Exceptions.DeckLocationNotSupportedError(
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
    def TimeToOpen(self, Options: list[OpenCloseOptions]) -> float:
        ...

    @abstractmethod
    def Close(self, Options: list[OpenCloseOptions]):
        ...

    @abstractmethod
    def TimeToClose(self, Options: list[OpenCloseOptions]) -> float:
        ...
