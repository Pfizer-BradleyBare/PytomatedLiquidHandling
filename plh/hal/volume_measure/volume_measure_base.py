from __future__ import annotations

from abc import abstractmethod
from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.hal import deck_location, labware, layout_item
from plh.hal.layout_item.filter_plate_stack import *
from plh.hal.tools import HALDevice, Interface


@dataclasses.dataclass(kw_only=True, eq=False)
class VolumeMeasureBase(Interface, HALDevice):
    """Device that can be used to measure the volume of liquid in a container."""

    supported_labware: Annotated[
        list[labware.PipettableLabware],
        BeforeValidator(labware.validate_list),
    ]
    supported_deck_locations: Annotated[
        list[deck_location.DeckLocationBase],
        BeforeValidator(deck_location.validate_list),
    ]

    def assert_supported_labware(
        self: VolumeMeasureBase,
        *args: labware.LabwareBase,
    ) -> None:
        exceptions = [
            labware.exceptions.LabwareNotSupportedError(self, item)
            for item in args
            if item not in self.supported_labware
        ]

        if len(exceptions) != 0:
            msg = "Some labware is not supported."
            raise ExceptionGroup(msg, exceptions)

    def assert_supported_deck_locations(
        self: VolumeMeasureBase,
        *args: deck_location.DeckLocationBase,
    ) -> None:
        exceptions = [
            deck_location.exceptions.DeckLocationNotSupportedError(self, item)
            for item in args
            if item not in self.supported_deck_locations
        ]

        if len(exceptions) != 0:
            msg = "Some deck locations are not supported."
            raise ExceptionGroup(msg, exceptions)

    @abstractmethod
    def measure_volume(
        self: VolumeMeasureBase,
        *args: tuple[layout_item.LayoutItemBase, int | str],
    ) -> list[float]:
        """Measures volume and returns a list of float volumes"""
