from __future__ import annotations

from abc import abstractmethod

from pydantic import dataclasses, field_validator

from plh.hal import deck_location, labware
from plh.hal.tools import HALDevice, Interface

from .options import OpenCloseOptions


@dataclasses.dataclass(kw_only=True)
class CloseableContainerBase(Interface, HALDevice):
    """A container that is part of a labware type that can be opened with some kind of tool.

    NOTE: This is NOT the same as a lid for a coverable plate.
    """

    supported_deck_locations: list[deck_location.DeckLocationBase]
    """The supported deck locations to where an open/close operation can occur."""

    supported_labware: list[labware.LabwareBase]
    """The device can only open/close labware of this type(s)."""

    @field_validator("supported_deck_locations", mode="before")
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

    @field_validator("supported_labware", mode="before")
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

    def assert_options(
        self: CloseableContainerBase,
        options: list[OpenCloseOptions],
    ) -> None:
        """Must be called before calling ```open```, ```open_time```, ```close```, or ```close_time```.

        If LabwareNotSupportedError is thrown then you are trying to use the wrong ClosedContainerDevice.

        If DeckLocationNotSupportedError is thrown then you need to move the LayoutItem to a compatible location.

        Raises ExceptionGroup of the following:

            Labware.LabwareNotSupportedError

            DeckLocation.DeckLocationNotSupportedError
        """
        excepts = []

        unsupported_deck_locations = []
        unsupported_labware = []

        for opt in options:
            deck_location_instance = opt.layout_item.deck_location
            labware_instance = opt.layout_item.labware

            if deck_location_instance not in self.supported_deck_locations:
                unsupported_deck_locations.append(deck_location_instance)

            if labware_instance not in self.supported_labware:
                unsupported_labware.append(labware_instance)

        if len(unsupported_labware) > 0:
            excepts.append(
                labware.exceptions.LabwareNotSupportedError(unsupported_labware),
            )

        if len(unsupported_deck_locations) > 0:
            excepts.append(
                deck_location.exceptions.DeckLocationNotSupportedError(
                    unsupported_deck_locations,
                ),
            )

        if len(excepts) > 0:
            msg = "ClosedContainer OpenCloseoptions Exceptions"
            raise ExceptionGroup(msg, excepts)

    @abstractmethod
    def open(self: CloseableContainerBase, options: list[OpenCloseOptions]) -> None:
        """Initiates an open event dependent on ```OpenCloseOptions```."""

    @abstractmethod
    def open_time(
        self: CloseableContainerBase,
        options: list[OpenCloseOptions],
    ) -> float:
        """Calculates the time to open dependent on ```OpenCloseOptions```."""

    @abstractmethod
    def close(self: CloseableContainerBase, options: list[OpenCloseOptions]) -> None:
        """Initiates an close event dependent on ```OpenCloseOptions```."""

    @abstractmethod
    def close_time(
        self: CloseableContainerBase,
        options: list[OpenCloseOptions],
    ) -> float:
        """Calculates the time to close dependent on ```OpenCloseOptions```."""
