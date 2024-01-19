from __future__ import annotations

from typing import Literal, cast

from pydantic import dataclasses

from plh.driver.HAMILTON import HSLTipCountingLib
from plh.driver.HAMILTON.backend import HamiltonBackendBase

from .tip_base import *
from .tip_base import AvailablePosition, TipBase


@dataclasses.dataclass(kw_only=True)
class HamiltonFTR(TipBase):
    backend: HamiltonBackendBase
    backend_error_handling: Literal["N/A"] = "N/A"

    def initialize(self: HamiltonFTR) -> None:
        self.update_available_positions()

    def deinitialize(self: HamiltonFTR) -> None:
        command = HSLTipCountingLib.Write.Command(options=HSLTipCountingLib.Write.OptionsList(TipCounter=f"{type(self).__name__}_{int(self.volume)}"))
        for pos in self.available_positions:
            command.options.append(HSLTipCountingLib.Write.Options(LabwareID=pos.LabwareID,PositionID=pos.PositionID))

        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command,HSLTipCountingLib.Write.Response)

    def tips_in_teir(self: TipBase) -> list[AvailablePosition]:
        return self.available_positions

    def discard_layer_to_waste(self: HamiltonFTR) -> None:
        msg = "FTR tips cannot waste tiers. Reload tips."
        raise RuntimeError(msg)

    def update_available_positions(self: HamiltonFTR) -> None:
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
        self._parse_available_positions(
            cast(
                list[dict[str, str]],
                self.backend.acknowledge(
                    command,
                    HSLTipCountingLib.Edit.Response,
                ).AvailablePositions,
            ),
        )
