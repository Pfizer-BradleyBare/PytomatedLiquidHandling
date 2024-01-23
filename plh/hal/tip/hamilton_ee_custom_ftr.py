from __future__ import annotations

from typing import cast

from pydantic import dataclasses

from plh.driver.HAMILTON import EntryExit, HSLTipCountingLib

from .hamilton_ee_tip_base import *
from .hamilton_ee_tip_base import HamiltonEETipBase


@dataclasses.dataclass(kw_only=True)
class HamiltonEECustomFTR(HamiltonEETipBase):
    """Hamilton custom stackable FTR (Filtered Tip Rack) tip device with integration with EE (entry exit) for higher tip capacity."""

    def deinitialize(self: HamiltonEECustomFTR) -> None:
        """Saves the current position using the FTR driver. Moves the EE stacks to the bottom position."""

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

    def update_available_positions(self: HamiltonEECustomFTR) -> None:
        """Counts the number of items in each stack. Edits the number of available tips using FTR edit."""

        for stack in self.tip_stacks:
            command = EntryExit.CountLabwareInStack.Command(
                options=EntryExit.CountLabwareInStack.Options(
                    ModuleNumber=stack.module_number,
                    StackNumber=stack.stack_number,
                    LabwareID=stack.tip_rack.labware_id,
                    IsNTRRack=False,
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
