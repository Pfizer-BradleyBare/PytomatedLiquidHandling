from __future__ import annotations

from abc import abstractmethod
from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.implementation import deck_location, labware, layout_item
from plh.implementation.layout_item.filter_plate_stack import *
from plh.implementation.tools import HALDevice, Interface


@dataclasses.dataclass(kw_only=True)
class MeasureValues:
    volume: float
    height: float


@dataclasses.dataclass(kw_only=True, eq=False)
class ContainerMeasureBase(Interface, HALDevice):
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
        self: ContainerMeasureBase,
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
        self: ContainerMeasureBase,
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
    def measure(
        self: ContainerMeasureBase,
        *args: tuple[layout_item.LayoutItemBase, int | str],
    ) -> list[MeasureValues]:
        """Measures container and returns a list of MeasureValues."""
