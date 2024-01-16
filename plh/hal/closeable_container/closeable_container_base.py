from __future__ import annotations

from abc import abstractmethod

from pydantic import dataclasses, field_validator

from plh.driver.tools import OptionsBase
from plh.hal import deck_location, labware, layout_item
from plh.hal.tools import HALDevice, Interface


@dataclasses.dataclass(kw_only=True)
class OpenCloseOptions(OptionsBase):
    LayoutItem: layout_item.LayoutItemBase
    Position: str | int


@dataclasses.dataclass(kw_only=True)
class CloseableContainerBase(Interface, HALDevice):
    """A container that is part of a rack that can be opened with some kind of tool.

    This is NOT the same as a lid for a plate.

    Attributes
    ----------
        SupportedDeckLocations: The rack must be in one of these deck locations to perform an operation.
        SupportedLabwares: The device can only open labware of this type(s).
    """

    supported_deck_locations: list[deck_location.DeckLocationBase]
    supported_labware: list[labware.LabwareBase]

    @field_validator("SupportedDeckLocations", mode="before")
    @classmethod
    def __supported_deck_locations_validate(
        cls: type[CloseableContainerBase],
        v: list[str | deck_location.DeckLocationBase],
    ) -> list[deck_location.DeckLocationBase]:
        supported_objects = []

        objects = deck_location.devices

        for item in v:
            if isinstance(item, deck_location.DeckLocationBase):
                supported_objects.append(item)

            elif item not in objects:
                raise ValueError(
                    item
                    + " is not found in "
                    + deck_location.DeckLocationBase.__name__
                    + " objects.",
                )

            else:
                supported_objects.append(objects[item])

        return supported_objects

    @field_validator("SupportedLabwares", mode="before")
    @classmethod
    def __supported_labwares_validate(
        cls: type[CloseableContainerBase],
        v: list[str | labware.LabwareBase],
    ) -> list[labware.LabwareBase]:
        supported_objects = []

        objects = labware.devices

        for item in v:
            if isinstance(item, labware.LabwareBase):
                supported_objects.append(item)

            elif item not in objects:
                raise ValueError(
                    item
                    + " is not found in "
                    + labware.LabwareBase.__name__
                    + " objects.",
                )

            else:
                supported_objects.append(objects[item])

        return supported_objects

    def assert_open_close_options(
        self: CloseableContainerBase,
        options: list[OpenCloseOptions],
    ) -> None:
        """Must be called before calling Open, OpenTime, Close, or CloseTime.

        If LabwareNotSupportedError is thrown then you are trying to use the wrong ClosedContainerDevice.

        If DeckLocationNotSupportedError is thrown then you need to move the LayoutItem to a compatible location.

        Raises ExceptionGroup of the following:
            Labware.Base.LabwareNotSupportedError

            DeckLocation.Base.DeckLocationNotSupportedError
        """
        excepts = []

        unsupported_deck_locations = []
        unsupported_labware = []

        for opt in options:
            deck_location_instance = opt.LayoutItem.deck_location
            labware_instance = opt.LayoutItem.labware

            if deck_location_instance not in self.supported_deck_locations:
                unsupported_deck_locations.append(deck_location_instance)

            if labware_instance not in self.supported_labware:
                unsupported_labware.append(labware_instance)

        if len(unsupported_labware) > 0:
            excepts.append(
                labware.LabwareNotSupportedError(unsupported_labware),
            )

        if len(unsupported_deck_locations) > 0:
            excepts.append(
                deck_location.DeckLocationNotSupportedError(
                    unsupported_deck_locations,
                ),
            )

        if len(excepts) > 0:
            msg = "ClosedContainer OpenCloseoptions Exceptions"
            raise ExceptionGroup(msg, excepts)

    @abstractmethod
    def open(self: CloseableContainerBase, options: list[OpenCloseOptions]) -> None:
        ...

    @abstractmethod
    def time_to_open(
        self: CloseableContainerBase,
        options: list[OpenCloseOptions],
    ) -> float:
        ...

    @abstractmethod
    def close(self: CloseableContainerBase, options: list[OpenCloseOptions]) -> None:
        ...

    @abstractmethod
    def time_to_close(
        self: CloseableContainerBase,
        options: list[OpenCloseOptions],
    ) -> float:
        ...
