from __future__ import annotations

from pydantic import dataclasses, field_validator, model_validator

from plh.driver.HAMILTON import EntryExit
from plh.driver.HAMILTON.backend import VantageTrackGripperEntryExit
from plh.hal import layout_item, transport

from .tip_base import *
from .tip_base import TipBase


@dataclasses.dataclass(kw_only=True)
class EETipStack:
    """Entry exit containing a stack of tips."""

    tip_rack: layout_item.TipRack
    """Rack layout item that will be used to retrieve a tip rack from the EE stack."""

    module_number: int
    """EE module number"""

    stack_number: int
    """EE stack number"""

    stack_count: int = field(init=False, default=0)
    """Number of items in the stack."""

    @field_validator("tip_rack", mode="before")
    @classmethod
    def __tip_rack_validate(
        cls: type[EETipStack],
        v: str | layout_item.LayoutItemBase,
    ) -> layout_item.LayoutItemBase:
        if isinstance(v, layout_item.LayoutItemBase):
            return v

        objects = layout_item.devices
        identifier = v

        if identifier not in objects:
            raise ValueError(
                identifier
                + " is not found in "
                + layout_item.LayoutItemBase.__name__
                + " objects.",
            )

        return objects[identifier]


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonEETipBase(TipBase):
    """Hamilton tip device with integration with EE (entry exit) for higher tip capacity.
    In this configuration tips are stored in EE until needed then moved to the deck.
    NOTE: Your number of tip racks and tip stacks must be equal.
    """

    backend: VantageTrackGripperEntryExit
    """Only supported on Hamilton Vantage systems."""

    tip_stacks: list[EETipStack]
    """Stacks associated with this tip device."""

    tip_rack_waste: layout_item.TipRack
    """Rack waste location. Empty racks will be transport here to be thrown away."""

    @field_validator("tip_rack_waste", mode="before")
    @classmethod
    def __tip_rack_validate(
        cls: type[HamiltonEETipBase],
        v: str | layout_item.LayoutItemBase,
    ) -> layout_item.LayoutItemBase:
        if isinstance(v, layout_item.LayoutItemBase):
            return v

        objects = layout_item.devices
        identifier = v

        if identifier not in objects:
            raise ValueError(
                identifier
                + " is not found in "
                + layout_item.LayoutItemBase.__name__
                + " objects.",
            )

        return objects[identifier]

    @model_validator(mode="after")
    @staticmethod
    def __model_validate(v: HamiltonEETipBase) -> HamiltonEETipBase:
        if len(v.tip_racks) != len(v.tip_stacks):
            msg = "Number of tip_racks and tip_stacks must be equal."
            raise ValueError(msg)
        return v

    def remaining_tips(self: HamiltonEETipBase) -> int:
        """Remaining tips is the number of available positions + the number of stacks."""
        tips_per_rack = self.tip_racks[0].labware.layout.total_positions()

        return len(self.available_positions) + sum(
            [tips_per_rack * stack.stack_count for stack in self.tip_stacks],
        )

    def discard_teir(self: HamiltonEETipBase) -> list[transport.GetPlaceOptions]:
        """For any given number of racks the tip stacks will be used to replenish.
        If a stack runs out of tips then the stack will be moved to the so stacks are depleted in order.
        """
        for stack in self.tip_stacks:
            if stack.stack_count == 0:
                raise RuntimeError("Out of items. TODO reload error.")

            command = EntryExit.MoveToBeam.Command(
                options=EntryExit.MoveToBeam.Options(
                    ModuleNumber=stack.module_number,
                    StackNumber=stack.stack_number,
                    OffsetFromBeam=0,
                ),
                backend_error_handling=False,
            )

            self.backend.execute(command)
            self.backend.wait(command)
            self.backend.acknowledge(command, EntryExit.MoveToBeam.Response)
            # Move the stack to beam so we can access the tip rack.

            stack.stack_count -= 1

        return sum(
            [
                [
                    transport.GetPlaceOptions(
                        source_layout_item=rack,
                        destination_layout_item=self.tip_rack_waste,
                    ),
                    transport.GetPlaceOptions(
                        source_layout_item=stack.tip_rack,
                        destination_layout_item=rack,
                    ),
                ]
                for rack, stack in zip(self.tip_racks, self.tip_stacks)
            ],
            [],
        )
