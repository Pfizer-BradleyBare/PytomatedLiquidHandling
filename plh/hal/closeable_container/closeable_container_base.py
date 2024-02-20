from __future__ import annotations

from abc import abstractmethod
from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.hal import deck_location, labware
from plh.hal.tools import HALDevice, Interface

from .options import OpenCloseOptions


@dataclasses.dataclass(kw_only=True, eq=False)
class CloseableContainerBase(Interface, HALDevice):
    """A container that is part of a labware type that can be opened with some kind of tool.

    NOTE: This is NOT the same as a lid for a coverable plate.
    """

    supported_deck_locations: Annotated[
        list[deck_location.DeckLocationBase],
        BeforeValidator(deck_location.validate_list),
    ]
    """The supported deck locations to where an open/close operation can occur."""

    supported_labware: Annotated[
        list[labware.LabwareBase],
        BeforeValidator(labware.validate_list),
    ]
    """The device can only open/close labware of this type(s)."""

    def assert_open_close(
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

        for opt in options:
            deck_location_instance = opt.layout_item.deck_location
            labware_instance = opt.layout_item.labware

            if deck_location_instance not in self.supported_deck_locations:
                excepts.append(
                    deck_location.exceptions.DeckLocationNotSupportedError(
                        self,
                        deck_location_instance,
                    ),
                )

            if labware_instance not in self.supported_labware:
                excepts.append(
                    labware.exceptions.LabwareNotSupportedError(self, labware_instance),
                )

        if len(excepts) > 0:
            msg = "Exceptions"
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
