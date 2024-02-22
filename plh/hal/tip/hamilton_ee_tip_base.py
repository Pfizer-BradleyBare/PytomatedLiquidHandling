from __future__ import annotations

from typing import Annotated, cast

from pydantic import dataclasses, model_validator
from pydantic.functional_validators import BeforeValidator

from plh.driver.HAMILTON import EntryExit
from plh.driver.HAMILTON.backend import VantageTrackGripperEntryExit
from plh.hal import backend, layout_item

from .tip_base import *
from .tip_base import TipBase


@dataclasses.dataclass(kw_only=True)
class EETipStack:
    """Entry exit containing a stack of tips."""

    tip_rack: Annotated[
        layout_item.TipRack,
        BeforeValidator(layout_item.validate_instance),
    ]
    """Rack layout item that will be used to retrieve a tip rack from the EE stack."""

    module_number: int
    """EE module number"""

    stack_number: int
    """EE stack number"""

    stack_count: int = field(init=False, default=0)
    """Number of items in the stack."""


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonEETipBase(TipBase):
    """Hamilton tip device with integration with EE (entry exit) for higher tip capacity.
    In this configuration tips are stored in EE until needed then moved to the deck.
    NOTE: Your number of tip racks and tip stacks must be equal.
    """

    backend: Annotated[
        VantageTrackGripperEntryExit,
        BeforeValidator(backend.validate_instance),
    ]
    """Only supported on Hamilton Vantage systems."""

    tip_stacks: list[EETipStack]
    """Stacks associated with this tip device."""

    tip_rack_waste: Annotated[
        layout_item.TipRack,
        BeforeValidator(layout_item.validate_instance),
    ]
    """Rack waste location. Empty racks will be transport here to be thrown away."""

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

    def discard_teir(
        self: HamiltonEETipBase,
    ) -> list[tuple[layout_item.LayoutItemBase, layout_item.LayoutItemBase]]:
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
                    (
                        cast(layout_item.LayoutItemBase, rack),
                        cast(layout_item.LayoutItemBase, self.tip_rack_waste),
                    ),
                    (
                        cast(layout_item.LayoutItemBase, stack.tip_rack),
                        cast(layout_item.LayoutItemBase, rack),
                    ),
                ]
                for rack, stack in zip(self.tip_racks, self.tip_stacks)
            ],
            [],
        )
