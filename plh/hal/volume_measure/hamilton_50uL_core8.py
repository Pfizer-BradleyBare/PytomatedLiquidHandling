from __future__ import annotations

from dataclasses import field
from typing import Annotated

from pydantic import dataclasses, model_validator
from pydantic.functional_validators import BeforeValidator

from plh.driver.HAMILTON.backend import HamiltonBackendBase
from plh.driver.HAMILTON.HSLLabwrAccess import AbsolutePositionValuesGetForLabwareID
from plh.hal import deck_location, labware, layout_item, pipette
from plh.hal.layout_item.filter_plate_stack import *
from plh.hal.pipette.hamilton_portrait_core8_contact_dispense import *
from plh.hal.tools import HALDevice, Interface


@dataclasses.dataclass(kw_only=True, eq=False)
class Hamilton50uLCORE8(Interface, HALDevice):
    """Device that can be used to measure the volume of liquid in a container."""

    pipette: Annotated[
        pipette.HamiltonPortraitCORE8ContactDispense,
        BeforeValidator(pipette.validate_instance),
    ]

    backend: HamiltonBackendBase = field(init=False)

    supported_labware: Annotated[
        list[labware.PipettableLabware],
        BeforeValidator(labware.validate_list),
    ] = field(init=False)

    supported_deck_locations: Annotated[
        list[deck_location.DeckLocationBase],
        BeforeValidator(deck_location.validate_list),
    ] = field(init=False)

    def initialize(self: Hamilton50uLCORE8) -> None:
        self.pipette.initialize()

    def deinitialize(self: Hamilton50uLCORE8) -> None:
        self.pipette.deinitialize()

    @model_validator(mode="after")
    def __model_validate(self: Hamilton50uLCORE8) -> Hamilton50uLCORE8:
        self.supported_labware = self.pipette.supported_source_labware
        self.supported_deck_locations = self.pipette.supported_deck_locations
        self.backend = self.pipette.backend
        # Copy this info from the pipette because it drives our compatibility

        return self

    def measure_volume(
        self: Hamilton50uLCORE8,
        *args: tuple[layout_item.LayoutItemBase, int | str],
    ) -> list[float]:
        """Measures volume and returns a list of float volumes"""
        layout_items = {layout_item for layout_item, _ in args}

        command = AbsolutePositionValuesGetForLabwareID.Command(
            options=[
                AbsolutePositionValuesGetForLabwareID.Options(
                    LabwareID=layout_item.labware_id,
                )
                for layout_item in layout_items
            ],
        )
        self.backend.execute(command)
        self.backend.wait(command)

        z_heights = {
            layout_item: labware_position.ZPosition
            for layout_item, labware_position in zip(
                layout_items,
                self.backend.acknowledge(
                    command,
                    AbsolutePositionValuesGetForLabwareID.Response,
                ).LabwarePositions,
            )
        }
        # Collect Z heights
