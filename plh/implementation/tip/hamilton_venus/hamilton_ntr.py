from __future__ import annotations

from dataclasses import field
from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.device.hamilton_venus import Visual_NTR_Library
from plh.device.hamilton_venus.backend import HamiltonBackendBase
from plh.implementation import backend, layout_item, transport

from ..tip_base import AvailablePosition, TipBase


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonNTR(TipBase):
    """Hamilton NTR(Nested Tip Rack) tip device."""

    backend: Annotated[HamiltonBackendBase, BeforeValidator(backend.validate_instance)]
    """Only supported on Hamilton systems."""

    tip_racks: Annotated[
        list[layout_item.hamilton_venus.HamiltonVenusTipRack],
        BeforeValidator(layout_item.validate_list),
    ]

    tip_rack_waste: Annotated[
        layout_item.hamilton_venus.HamiltonVenusTipRack,
        BeforeValidator(layout_item.validate_instance),
    ]
    """Rack waste location. Empty racks will be transport here to be thrown away."""

    available_positions_per_teir: list[list[AvailablePosition]] = field(
        init=False,
        default_factory=list,
    )
    """NTR racks are stacked. Thus, we need to track the available positions in each row of the stack. These are the inactive positions."""

    available_racks_per_teir: list[
        list[layout_item.hamilton_venus.HamiltonVenusTipRack]
    ] = field(
        init=False,
        default_factory=list,
    )
    """NTR racks are stacked. Thus, we need to track the racks in each row of the stack. These are all racks (active and inactive)."""

    def initialize(self: HamiltonNTR) -> None:
        """Uses the NTR library to edit the number of available tips."""
        command = Visual_NTR_Library.Channels_TipCounter_Edit.Command(
            options=Visual_NTR_Library.Channels_TipCounter_Edit.OptionsList(
                TipCounter=f"{type(self).__name__}_{int(self.volume)}",
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

        self.update_available_positions(
            self.backend.acknowledge(
                command,
                Visual_NTR_Library.Channels_TipCounter_Edit.Response,
            ).AvailablePositions,
        )

    def deinitialize(self: HamiltonNTR) -> None:
        """Saves the current position of the tips using the NTR driver."""
        command = Visual_NTR_Library.Channels_TipCounter_Write.Command(
            options=Visual_NTR_Library.Channels_TipCounter_Write.OptionsList(
                TipCounter=f"{type(self).__name__}_{int(self.volume)}",
            ),
        )

        for pos in self.available_positions + [
            pos for teir in self.available_positions_per_teir for pos in teir
        ]:
            command.options.append(
                Visual_NTR_Library.Channels_TipCounter_Write.Options(
                    LabwareID=pos.LabwareID,
                    PositionID=pos.PositionID,
                ),
            )

        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(
            command,
            Visual_NTR_Library.Channels_TipCounter_Write.Response,
        )

    def remaining_tips(self: HamiltonNTR) -> int:
        """Remaining tips is the number of available positions + the number of unused teirs."""
        tips_per_rack = self.tip_racks[0].labware.layout.total_positions()

        return len(self.available_positions) + (
            len(
                [rack for teir in self.available_racks_per_teir[1:] for rack in teir],
            )
            * tips_per_rack
        )

    def discard_teir(
        self: HamiltonNTR,
    ) -> None:
        """NOTE: The top teir after edit will be partially available.
        Thus, we use the ```available_positions_per_teir``` information to only discard the remaining teirs.
        """
        discard_racks = self.available_racks_per_teir[0]
        self.available_racks_per_teir = self.available_racks_per_teir[1:]

        if len(self.available_racks_per_teir) == 0:
            raise RuntimeError("TODO: tip reload error")

        self.available_positions = self.available_positions_per_teir[0]
        self.available_positions_per_teir = self.available_positions_per_teir[1:]

        transport.transport_layout_items(
            *[(rack, self.tip_rack_waste) for rack in discard_racks],
        )
        # discard the racks

    def update_available_positions(
        self: HamiltonNTR,
        raw_available_positions: list[dict[str, str]],
    ) -> None:
        """Extracts information about the teirs in current and subsequence layers."""
        self._parse_available_positions(
            raw_available_positions,
        )

        teirs = len(self.tip_racks)
        tips_per_rack = self.tip_racks[0].labware.layout.total_positions()

        available_positions_per_teir = list(
            reversed(
                [
                    list(
                        reversed(
                            list(reversed(self.available_positions))[
                                i : i + teirs * tips_per_rack
                            ],
                        ),
                    )
                    for i in range(
                        0,
                        len(self.available_positions),
                        teirs * tips_per_rack,
                    )
                ],
            ),
        )
        # NTR returns all the tips available accross all teirs. So we parse that down to a list of list of positions.
        # The list of positions can be considered all positions available across a teir.
        # the list of list of positions is each row through the teirs.
        # What does the function above do? Copy it and try it on a list of your own.

        self.available_positions_per_teir = available_positions_per_teir[1:]
        self.available_positions = available_positions_per_teir[0]

        self.available_racks_per_teir = []

        for teir in available_positions_per_teir:
            teir_labware_ids = {pos.LabwareID for pos in teir}

            self.available_racks_per_teir.append(
                [
                    rack
                    for rack in self.tip_racks
                    if rack.labware_id in teir_labware_ids
                ],
            )
        # We need to be able to track the racks per teir as well to enable discards
