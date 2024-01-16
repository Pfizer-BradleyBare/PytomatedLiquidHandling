from __future__ import annotations

from typing import Literal, cast

from pydantic import dataclasses

from plh.driver.HAMILTON import HSLTipCountingLib
from plh.driver.HAMILTON.backend import HamiltonBackendBase

from .tip_base import TipBase


@dataclasses.dataclass(kw_only=True)
class HamiltonFTR(TipBase):
    backend: HamiltonBackendBase
    backend_error_handling: Literal["N/A"] = "N/A"

    def remaining_tips_in_tier(self: HamiltonFTR) -> int:
        return self.remaining_tips()

    def discard_layer_to_waste(self: HamiltonFTR) -> None:
        msg = "FTR tips cannot waste tiers. Reload tips."
        raise RuntimeError(msg)

    def update_available_positions(self: HamiltonFTR) -> None:
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
