from __future__ import annotations

from abc import abstractmethod
from dataclasses import field
from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.device.HAMILTON import EntryExit
from plh.device.HAMILTON.backend import VantageTrackGripperEntryExit
from plh.implementation import backend, layout_item, transport

from .tip_base import AvailablePosition, TipBase


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

    def remaining_tips(self: HamiltonEETipBase) -> int:
        """Remaining tips is the number of available positions + the number of stacks."""
        tips_per_rack = self.tip_racks[0].labware.layout.total_positions()

        return len(self.available_positions) + sum(
            [tips_per_rack * stack.stack_count for stack in self.tip_stacks],
        )

    @abstractmethod
    def initialize(self: HamiltonEETipBase) -> None:
        """Counts the number of items in each stack. Edits the number of available tips using FTR edit."""

    def discard_teir(
        self: HamiltonEETipBase,
    ) -> None:
        """For any given number of racks the tip stacks will be used to replenish.
        If a stack runs out of tips then the stack will be moved to the so stacks are depleted in order.
        """
        if len(self.tip_racks) > sum(stack.stack_count for stack in self.tip_stacks):
            raise RuntimeError("Not enough stack items to replenish racks.")

        for rack in self.tip_racks:
            for stack in self.tip_stacks[:]:
                if stack.stack_count == 0:
                    self.tip_stacks.remove(stack)
                    self.tip_stacks.append(stack)
                    continue
                # If we have emptied a tip stack then we will skip it.
                # Before we skip it we want to move it to the end of our list of stacks so we use whole stacks.

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

                break

            transport.transport_layout_items(
                (rack, self.tip_rack_waste),
                (stack.tip_rack, rack),
            )
        # repeat for all racks

        self.available_positions = [
            AvailablePosition(
                LabwareID=tip_rack.labware_id,
                PositionID=tip_rack.labware.layout.get_position_id(i),
            )
            for tip_rack in self.tip_racks
            for i in range(1, tip_rack.labware.layout.total_positions() + 1)
        ]
