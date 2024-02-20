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

    def assert_supported_labware(
        self: CloseableContainerBase,
        labwares: list[labware.LabwareBase],
    ) -> None:
        exceptions = [
            labware.exceptions.LabwareNotSupportedError(self, item)
            for item in labwares
            if item not in self.supported_labware
        ]

        if len(exceptions) != 0:
            msg = "Some labware is not supported."
            raise ExceptionGroup(msg, exceptions)

    def assert_supported_deck_locations(
        self: CloseableContainerBase,
        deck_locations: list[deck_location.DeckLocationBase],
    ) -> None:
        exceptions = [
            deck_location.exceptions.DeckLocationNotSupportedError(self, item)
            for item in deck_locations
            if item not in self.supported_deck_locations
        ]

        if len(exceptions) != 0:
            msg = "Some deck locations are not supported."
            raise ExceptionGroup(msg, exceptions)

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
