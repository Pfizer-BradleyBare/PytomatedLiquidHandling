from __future__ import annotations

import itertools
from collections import defaultdict
from typing import Literal, cast

from pydantic import dataclasses

from plh.driver.HAMILTON.backend import HamiltonBackendBase
from plh.driver.HAMILTON.ML_STAR import Channel1000uL
from plh.hal import labware

from .options import TransferOptions
from .pipette_base import PipetteBase
from .pipette_tip import PipetteTip


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonPortraitCORE8(PipetteBase):
    backend: HamiltonBackendBase
    active_channels: list[Literal[1, 2, 3, 4, 5, 6, 7, 8]]

    def _group_options(
        self: HamiltonPortraitCORE8,
        options: list[TransferOptions],
    ) -> defaultdict[str, list[tuple[PipetteTip, TransferOptions]]]:
        liquid_class_max_volumes: dict[str, float] = {}
        for opt in options:
            combined_name = (
                opt.source_liquid_class_category
                + ":"
                + opt.destination_liquid_class_category
            )

            if combined_name not in liquid_class_max_volumes:
                liquid_class_max_volumes[combined_name] = self._get_max_transfer_volume(
                    opt.source_liquid_class_category,
                    opt.destination_liquid_class_category,
                )
        # Max volume for each liquid class pairing. Important

        final_tranfer_options: list[TransferOptions] = []
        truncated_final_tranfer_options: list[list[TransferOptions]] = []

        for opt in options:
            combined_name = (
                opt.source_liquid_class_category
                + ":"
                + opt.destination_liquid_class_category
            )

            truncated_options = self._truncate_transfer_volume(
                opt,
                liquid_class_max_volumes[combined_name],
            )

            if len(truncated_options) == 1:
                final_tranfer_options += truncated_options
                # If there is only 1 option then no truncation occured. We want to perform all non truncated transfers first.
            else:
                truncated_final_tranfer_options.append(truncated_options)
                # If there is more than one we want to collect them so we can shuffle. This may increaes final pipetting speed.=
        # Truncate based on max volume

        final_tranfer_options += [
            i
            for l in itertools.zip_longest(
                *truncated_final_tranfer_options,
                fillvalue=None,
            )
            for i in l
            if i is not None
        ]
        # Shuffle our truncated options then add to the end.

        tip_grouped_options: defaultdict[
            str,
            list[tuple[PipetteTip, TransferOptions]],
        ] = defaultdict(list)
        for opt in options:
            tip = self._get_tip(
                opt.source_liquid_class_category,
                opt.destination_liquid_class_category,
                opt.transfer_volume,
            )

            tip_grouped_options[tip.tip.identifier].append((tip, opt))
        return tip_grouped_options

    def transfer(self: HamiltonPortraitCORE8, options: list[TransferOptions]) -> None:
        num_active_channels = len(self.active_channels)

        tip_grouped_options = self._group_options(options)

        for tip_opt_group in tip_grouped_options.values():
            tip = tip_opt_group[0][0]

            packages_opts = [
                [tip_opt[1] for tip_opt in tip_opt_group][x : x + num_active_channels]
                for x in range(0, len(tip_opt_group), num_active_channels)
            ]
            # Packaging in sets of num channels

            if len(packages_opts) > tip.tip.remaining_tips():
                raise RuntimeError("Not enough tips left")
            # are there at minimum enough tips left?

            for opts in packages_opts:
                if len(tip.tip.available_positions) < len(opts):
                    tip.tip.discard_teir()
                # If not enough tips then get user to help

                tip_positions = tip.tip.available_positions[: len(opts)]

                get_options: list[Channel1000uL.Pickup.Options] = []
                for index, (opt, channel_number) in enumerate(
                    zip(opts, self.active_channels),
                ):
                    get_options.append(
                        Channel1000uL.Pickup.Options(
                            ChannelNumber=channel_number,
                            LabwareID=tip_positions[index].LabwareID,
                            PositionID=tip_positions[index].PositionID,
                        ),
                    )
                command = Channel1000uL.Pickup.Command(
                    backend_error_handling=False,
                    options=get_options,
                )
                self.backend.execute(command)
                self.backend.wait(command)
                self.backend.acknowledge(command, Channel1000uL.Pickup.Response)
                # Pickup the tips

                aspirate_options: list[Channel1000uL.Aspirate.Options] = []
                for index, (opt, channel_number) in enumerate(
                    zip(opts, self.active_channels),
                ):
                    aspirate_labware = cast(
                        labware.PipettableLabware,
                        opt.source_layout_item.labware,
                    )

                    numeric_layout = labware.NumericLayout(
                        rows=opt.source_layout_item.labware.layout.rows,
                        columns=opt.source_layout_item.labware.layout.columns,
                        direction=opt.source_layout_item.labware.layout.direction,
                    )
                    # we need to do some numeric offsets to the position so convert it to a number first if it is not one.

                    aspirate_position = (
                        (int(numeric_layout.get_position_id(opt.source_position)) - 1)
                        * aspirate_labware.well_definition.positions_per_well
                        + index
                        + 1
                    )
                    # The position MUST take into account the number of sequences per well.
                    # This calculates the proper position in the well for each channel if the container has multiple position positions.

                    aspirate_options.append(
                        Channel1000uL.Aspirate.Options(
                            ChannelNumber=channel_number,
                            LabwareID=opt.source_layout_item.labware_id,
                            PositionID=opt.source_layout_item.labware.layout.get_position_id(
                                aspirate_position,
                            ),
                            LiquidClass=str(
                                self._get_liquid_class(
                                    opt.source_liquid_class_category,
                                    opt.transfer_volume,
                                ),
                            ),
                            Volume=opt.transfer_volume,
                        ),
                    )

                command = Channel1000uL.Aspirate.Command(
                    backend_error_handling=False,
                    options=aspirate_options,
                )
                self.backend.execute(command)
                self.backend.wait(command)
                self.backend.acknowledge(command, Channel1000uL.Aspirate.Response)

                dispense_options: list[Channel1000uL.Dispense.Options] = []
                for index, (opt, channel_number) in enumerate(
                    zip(opts, self.active_channels),
                ):
                    dispense_labware = cast(
                        labware.PipettableLabware,
                        opt.destination_layout_item.labware,
                    )

                    numeric_layout = labware.NumericLayout(
                        rows=opt.destination_layout_item.labware.layout.rows,
                        columns=opt.destination_layout_item.labware.layout.columns,
                        direction=opt.destination_layout_item.labware.layout.direction,
                    )
                    # we need to do some numeric offsets to the position so convert it to a number first if it is not one.

                    dispense_position = (
                        (
                            int(
                                numeric_layout.get_position_id(
                                    opt.destination_position,
                                ),
                            )
                            - 1
                        )
                        * dispense_labware.well_definition.positions_per_well
                        + index
                        + 1
                    )
                    # The position MUST take into account the number of sequences per well.
                    # This calculates the proper position in the well for each channel if the container has multiple position positions.

                    dispense_options.append(
                        Channel1000uL.Dispense.Options(
                            ChannelNumber=channel_number,
                            LabwareID=opt.destination_layout_item.labware_id,
                            PositionID=opt.destination_layout_item.labware.layout.get_position_id(
                                dispense_position,
                            ),
                            LiquidClass=str(
                                self._get_liquid_class(
                                    opt.destination_liquid_class_category,
                                    opt.transfer_volume,
                                ),
                            ),
                            Volume=opt.transfer_volume,
                        ),
                    )

                command = Channel1000uL.Dispense.Command(
                    backend_error_handling=False,
                    options=dispense_options,
                )
                self.backend.execute(command)
                self.backend.wait(command)
                self.backend.acknowledge(command, Channel1000uL.Dispense.Response)

                eject_positions = ["1", "2", "3", "4", "13", "14", "15", "16"]
                # Hamilton waste always has 16 positions. Do be compatible with liquid waste we want to use the outer positions
                eject_options: list[Channel1000uL.Eject.Options] = []
                for index, (opt, channel_number) in enumerate(
                    zip(opts, self.active_channels),
                ):
                    eject_options.append(
                        Channel1000uL.Eject.Options(
                            LabwareID=tip.tip_waste_labware_id,
                            ChannelNumber=channel_number,
                            PositionID=eject_positions[index],
                        ),
                    )

                command = Channel1000uL.Eject.Command(
                    backend_error_handling=False,
                    options=eject_options,
                )
                self.backend.execute(command)
                self.backend.wait(command)
                self.backend.acknowledge(command, Channel1000uL.Eject.Response)

    def transfer_time(
        self: HamiltonPortraitCORE8,
        options: list[TransferOptions],
    ) -> float:
        return 0
