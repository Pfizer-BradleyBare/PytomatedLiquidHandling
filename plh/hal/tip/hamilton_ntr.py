from __future__ import annotations

from dataclasses import field
from typing import Literal, cast

from pydantic import dataclasses

from plh.driver.HAMILTON import Visual_NTR_Library
from plh.driver.HAMILTON.backend import HamiltonBackendBase
from plh.hal import deck_location, layout_item

from .tip_base import *
from .tip_base import TipBase


@dataclasses.dataclass(kw_only=True)
class HamiltonNTR(TipBase):
    backend: HamiltonBackendBase
    backend_error_handling: Literal["N/A"] = "N/A"

    tiers: int
    tip_rack_waste: layout_item.TipRack
    tier_discard_number: int = field(init=False, default=100)
    discarded_tip_racks: list[layout_item.TipRack] = field(
        init=False,
        default_factory=list,
    )

    def initialize(self: HamiltonNTR) -> None:
        ...

    def deinitialize(self: HamiltonNTR) -> None:
        ...

    def remaining_tips_in_tier(self: HamiltonNTR) -> int:
        remaining = self.remaining_tips() % (self.tips_per_rack * self.tiers)

        if remaining == 0:
            available_ids = {pos.LabwareID for pos in self.available_positions}

            if len(available_ids) + len(self.discarded_tip_racks) == len(
                self.tip_racks,
            ):
                return self.tips_per_rack * self.tiers
                # We are at the start of a fresh layer

            return 0
            # We just emptied a layer and must discard

        return remaining

    def discard_layer_to_waste(self: HamiltonNTR) -> None:
        present_labware_ids = {pos.LabwareID for pos in self.available_positions}
        present_tip_racks = [
            tip_rack
            for tip_rack in self.tip_racks
            if tip_rack.labware_id not in present_labware_ids
        ]
        discard_tip_racks = [
            tip_rack
            for tip_rack in self.tip_racks
            if tip_rack.labware_id not in present_labware_ids
            and tip_rack not in self.discarded_tip_racks
        ]

        for i in range(self._TierDiscardNumber - len(discard_tip_racks)):
            discard_tip_racks.append(present_tip_racks[i])
        # Basically we should always discard the same number of racks as we have tiers.
        # There is a special case during tip counter edit where an NTR rack is removed manually by the user. We handle that here.

        for tip_rack in discard_tip_racks:
            self.discarded_tip_racks.append(tip_rack)
            deck_location.TransportableDeckLocation.get_compatible_transport_configs(
                tip_rack.deck_location,
                self.tip_rack_waste.deck_location,
            )[0][0].transport_device.transport(tip_rack, self.tip_rack_waste)

        self.available_positions = [
            pos
            for pos in self.available_positions
            if pos.LabwareID
            not in [tip_rack.labware_id for tip_rack in self.discarded_tip_racks]
        ]
        # Update available positions

        self.tier_discard_number = self.tiers
        # Reset the Tier discard number. This will only be changed here and in the TipCounterEdit method

        if len(self.available_positions) == 0:
            msg = "Out of tips. Reload tips."
            raise RuntimeError(msg)

    def update_available_positions(self: HamiltonNTR) -> None:
        command = Visual_NTR_Library.Channels_TipCounter_Edit.Command(
            options=Visual_NTR_Library.Channels_TipCounter_Edit.OptionsList(
                TipCounter="HamiltonTipNTR_" + str(self.volume) + "uL_TipCounter",
                DialogTitle="Please update the number of "
                + str(self.volume)
                + "uL tips currently loaded on the system",
            ),
        )
        for tip_rack in self.tip_racks:
            command.options.append(
                Visual_NTR_Library.Channels_TipCounter_Edit.Options(
                    LabwareID=tip_rack.labware_id,
                ),
            )

        self.backend.execute(command)
        self.backend.wait(command)
        self._parse_available_positions(
            cast(
                list[dict[str, str]],
                self.backend.acknowledge(
                    command,
                    Visual_NTR_Library.Channels_TipCounter_Edit.Response,
                ).AvailablePositions,
            ),
        )

        available_ids = {pos.LabwareID for pos in self.available_positions}
        self.discarded_tip_racks = [
            tip_rack
            for tip_rack in self.tip_racks
            if tip_rack.labware_id not in available_ids
        ]
        # We automatically assume the if a labwareID is NOT in the available positions, then it is basically already discarded.

        self._TierDiscardNumber = len(self.discarded_tip_racks) % self.tiers
        # Once we know which labwareIDs are already gone we can calculate how many to throw away on the first pass.
        # We basically say: "I assume to have a multiple of NumTiers so if I have any remainder then that is number of tiers to be thrown away."
