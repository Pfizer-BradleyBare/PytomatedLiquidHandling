from __future__ import annotations

from dataclasses import field
from typing import cast

from pydantic import dataclasses, field_validator

from plh.driver.HAMILTON import EntryExit, HSLTipCountingLib
from plh.driver.HAMILTON.backend import VantageTrackGripperEntryExit
from plh.hal import deck_location, layout_item

from .tip_base import *
from .tip_base import TipBase


@dataclasses.dataclass(kw_only=True)
class HamiltonEENTR(TipBase):
    @dataclasses.dataclass(kw_only=True)
    class TipStack:
        tip_rack: layout_item.TipRack
        module_number: int
        stack_number: int
        stack_count: int = field(init=False, default=0)

        @field_validator("tip_rack", mode="before")
        @classmethod
        def __tip_rack_validate(
            cls,
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

    backend: VantageTrackGripperEntryExit

    tip_stacks: list[TipStack]
    tip_rack_waste: layout_item.TipRack

    @field_validator("tip_rack_waste", mode="before")
    @classmethod
    def __tip_rack_validate(
        cls: type[HamiltonEENTR],
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

    def deinitialize(self: HamiltonEENTR) -> None:
        command = HSLTipCountingLib.Write.Command(
            options=HSLTipCountingLib.Write.OptionsList(
                TipCounter=f"{type(self).__name__}_{int(self.volume)}",
            ),
        )
        for pos in self.available_positions:
            command.options.append(
                HSLTipCountingLib.Write.Options(
                    LabwareID=pos.LabwareID,
                    PositionID=pos.PositionID,
                ),
            )

        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, HSLTipCountingLib.Write.Response)

        for stack in self.tip_stacks:
            command = EntryExit.MoveRandomShelfAccess.Command(
                options=EntryExit.MoveRandomShelfAccess.Options(
                    ModuleNumber=stack.module_number,
                    StackNumber=stack.stack_number,
                    Position=EntryExit.MoveRandomShelfAccess.PositionOptions.Bottom,
                ),
                backend_error_handling=False,
            )

    def remaining_tips(self: HamiltonEENTR) -> int:
        tips_per_rack = self.tip_racks[0].labware.layout.total_positions()

        return len(self.tips_in_teir()) + sum(
            [tips_per_rack * stack.stack_count for stack in self.tip_stacks],
        )

    def discard_teir(self: HamiltonEENTR) -> None:
        for rack in self.tip_racks:
            success_flag = False
            # So we can track if we actually replaced a rack

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
                    backend_error_handling=False,
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
                success_flag = True
                break

            if success_flag == False:
                raise RuntimeError("TODO: tip reload error")

    def update_available_positions(self: HamiltonEENTR) -> None:
        for stack in self.tip_stacks:
            command = EntryExit.CountLabwareInStack.Command(
                options=EntryExit.CountLabwareInStack.Options(
                    ModuleNumber=stack.module_number,
                    StackNumber=stack.stack_number,
                    LabwareID=stack.tip_rack.labware_id,
                    IsNTRRack=True,
                ),
                backend_error_handling=False,
            )
            self.backend.execute(command)
            self.backend.wait(command)
            stack.stack_count = self.backend.acknowledge(
                command,
                EntryExit.CountLabwareInStack.Response,
            ).NumLabware

            if self.backend.simulation_on is True:
                stack.stack_count = 100

        command = HSLTipCountingLib.Edit.Command(
            options=HSLTipCountingLib.Edit.OptionsList(
                TipCounter=f"{type(self).__name__}_{int(self.volume)}",
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
