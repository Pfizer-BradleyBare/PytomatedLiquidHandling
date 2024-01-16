from __future__ import annotations

from dataclasses import field
from typing import cast

from pydantic import dataclasses

from plh.driver.HAMILTON import EntryExit, HSLTipCountingLib
from plh.driver.HAMILTON.backend import VantageTrackGripperEntryExit
from plh.hal import deck_location, layout_item

from .tip_base import TipBase


@dataclasses.dataclass(kw_only=True)
class HamiltonEENTR(TipBase):
    @dataclasses.dataclass(kw_only=True)
    class TipStack:
        tip_rack: layout_item.TipRack
        module_number: int
        stack_number: int
        stack_count: int = field(init=False, default=0)

    backend: VantageTrackGripperEntryExit

    tip_stacks: list[TipStack]
    racks_per_stack: int
    tip_rack_waste: layout_item.TipRack

    def initialize(self: HamiltonEENTR) -> None:
        TipBase.initialize(self)

    def remaining_tips(self: HamiltonEENTR) -> int:
        return self.remaining_tips_in_tier() + sum(
            [self.tips_per_rack * stack.stack_count for stack in self.tip_stacks],
        )

    def remaining_tips_in_tier(self: HamiltonEENTR) -> int:
        return TipBase.remaining_tips(self)

    def discard_layer_to_waste(self: HamiltonEENTR) -> None:
        for rack in self.tip_racks:
            for stack in self.tip_stacks:
                if stack.stack_count == 0:
                    continue
                # only use stacks that have racks

                command = EntryExit.MoveToBeam.Command(
                    options=EntryExit.MoveToBeam.Options(
                        ModuleNumber=stack.module_number,
                        StackNumber=stack.stack_number,
                        OffsetFromBeam=0,
                    ),
                    backend_error_handling=self.backend_error_handling,
                )

                self.backend.execute(command)
                self.backend.wait(command)
                self.backend.acknowledge(command, EntryExit.MoveToBeam.Response)
                # Move the stack to beam so we can access the tip rack.

                stack.stack_count -= 1

                deck_location.TransportableDeckLocation.get_compatible_transport_configs(
                    rack.deck_location,
                    self.tip_rack_waste.deck_location,
                )[
                    0
                ][
                    0
                ].transport_device.transport(
                    rack,
                    self.tip_rack_waste,
                )
                # Dispose of the empty rack

                deck_location.TransportableDeckLocation.get_compatible_transport_configs(
                    rack.deck_location,
                    self.tip_rack_waste.deck_location,
                )[
                    0
                ][
                    0
                ].transport_device.transport(
                    rack,
                    stack.tip_rack,
                )
                # Move the full rack from the stack.

    def update_available_positions(self: HamiltonEENTR) -> None:
        for stack in self.tip_stacks:
            command = EntryExit.CountLabwareInStack.Command(
                options=EntryExit.CountLabwareInStack.Options(
                    ModuleNumber=stack.module_number,
                    StackNumber=stack.stack_number,
                    LabwareID=stack.tip_rack.labware_id,
                    IsNTRRack=True,
                ),
                backend_error_handling=self.backend_error_handling,
            )
            self.backend.execute(command)
            self.backend.wait(command)
            stack.stack_count = self.backend.acknowledge(
                command,
                EntryExit.CountLabwareInStack.Response,
            ).NumLabware

        command = HSLTipCountingLib.Edit.Command(
            options=HSLTipCountingLib.Edit.OptionsList(
                TipCounter="HamiltonTipFTR_" + str(self.volume) + "uL_TipCounter",
                DialogTitle="Please update the number of "
                + str(self.volume)
                + "uL tips currently loaded on the system",
            ),
        )
        for tip_rack in self.tip_racks:
            command.options.append(
                HSLTipCountingLib.Edit.Options(LabwareID=tip_rack.labware_id),
            )

        self.backend.execute(command)
        self.backend.wait(command)
        self._parse_available_positions(
            cast(
                list[dict[str, str]],
                self.backend.acknowledge(
                    command,
                    HSLTipCountingLib.Edit.Response,
                ).AvailablePositions,
            ),
        )
