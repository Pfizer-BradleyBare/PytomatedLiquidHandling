from __future__ import annotations

from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.device.HAMILTON import HSLTipCountingLib
from plh.device.HAMILTON.backend import HamiltonBackendBase
from plh.implementation import backend

from .tip_base import *
from .tip_base import TipBase


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonFTR(TipBase):
    """Hamilton FTR (Filtered Tip Rack) tip device."""

    backend: Annotated[HamiltonBackendBase, BeforeValidator(backend.validate_instance)]
    """Only supported on Hamilton systems."""

    def initialize(self: HamiltonFTR) -> None:
        """Uses the FTR edit command to allow the user to specify the number of tips available."""
        command = HSLTipCountingLib.Edit.Command(
            options=HSLTipCountingLib.Edit.OptionsList(
                TipCounter=f"{type(self).__name__}_{int(self.volume)}",
                DialogTitle=f"Please update the number of {int(self.volume)}uL tips currently loaded on the system",
            ),
        )
        for tip_rack in self.tip_racks:
            command.options.append(
                HSLTipCountingLib.Edit.Options(LabwareID=tip_rack.labware_id),
            )

        self.backend.execute(command)
        self.backend.wait(command)

        self.update_available_positions(
            self.backend.acknowledge(
                command,
                HSLTipCountingLib.Edit.Response,
            ).AvailablePositions,
        )

    def deinitialize(self: HamiltonFTR) -> None:
        """Saves the current position using the FTR driver."""
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

    def remaining_tips(self: HamiltonFTR) -> int:
        """FTR tips do not have teirs so remaining tips is just all the tips left."""
        return len(self.available_positions)

    def discard_teir(
        self: HamiltonFTR,
    ) -> None:
        """Cannot discard teir for normal FTR tips. You must load more tips."""
        raise RuntimeError("TODO: Tip reload error")

    def update_available_positions(
        self: HamiltonFTR,
        raw_available_positions: list[dict[str, str]],
    ) -> None:
        self._parse_available_positions(raw_available_positions)
