from __future__ import annotations

import itertools
from copy import copy
from math import ceil
from typing import cast

from pydantic import dataclasses

from plh.driver.HAMILTON.ML_STAR import Channel1000uL
from plh.hal import labware

from .hamilton_portrait_core8 import *
from .hamilton_portrait_core8 import HamiltonPortraitCORE8
from .options import (
    AspirateOptions,
    DispenseOptions,
    _AspirateDispenseOptions,
)
from .pipette_tip import PipetteTip


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonPortraitCORE8ContactDispense(HamiltonPortraitCORE8):
    def _aspirate(
        self: HamiltonPortraitCORE8ContactDispense,
        *args: _AspirateDispenseOptions,
    ) -> None:
        options = sorted(args, key=lambda x: x.channel_number)

        command = Channel1000uL.Aspirate.Command(
            backend_error_handling=False,
            options=[],
        )

        for option in options:
            command.options.append(
                Channel1000uL.Aspirate.Options(
                    ChannelNumber=option.channel_number,
                    LabwareID=option.layout_item.labware_id,
                    PositionID=option.position_id,
                    LiquidClass=option.liquid_class,
                    Volume=option.volume,
                    Mode=Channel1000uL.Aspirate.AspirateModeOptions.AspirateAll,
                    CapacitiveLiquidLevelDetection=Channel1000uL.Aspirate.LLDOptions.Off,
                    SubmergeDepth=0,
                    PressureLiquidLevelDetection=Channel1000uL.Aspirate.LLDOptions.Off,
                    MaxHeightDifference=0,
                    FixHeightFromBottom=cast(
                        labware.PipettableLabware,
                        option.layout_item.labware,
                    ).interpolate_volume(option.well_volume),
                    RetractDistanceForTransportAir=5,
                    LiquidFollowing=True,
                    MixCycles=option.mix_cycles,
                    MixPosition=0,
                    MixVolume=option.mix_volume,
                ),
            )

        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, Channel1000uL.Aspirate.Response)

    def _dispense(
        self: HamiltonPortraitCORE8ContactDispense,
        *args: _AspirateDispenseOptions,
    ) -> None:
        options = sorted(args, key=lambda x: x.channel_number)

        command = Channel1000uL.Dispense.Command(
            backend_error_handling=False,
            options=[],
        )

        for option in options:
            command.options.append(
                Channel1000uL.Dispense.Options(
                    ChannelNumber=option.channel_number,
                    LabwareID=option.layout_item.labware_id,
                    PositionID=option.position_id,
                    LiquidClass=option.liquid_class,
                    Volume=option.volume,
                    Mode=Channel1000uL.Dispense.DispenseModeOptions.FromLiquidClassDefinition,
                    FixHeightFromBottom=cast(
                        labware.PipettableLabware,
                        option.layout_item.labware,
                    ).interpolate_volume(option.well_volume),
                    RetractDistanceForTransportAir=5,
                    CapacitiveLiquidLevelDetection=Channel1000uL.Dispense.LLDOptions.Off,
                    SubmergeDepth=0,
                    SideTouch=False,
                    LiquidFollowing=True,
                    MixCycles=option.mix_cycles,
                    MixPosition=0,
                    MixVolume=option.mix_volume,
                ),
            )

        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, Channel1000uL.Dispense.Response)

    def save(self):
        self.assert_supported_aspirate_labware(
            *{arg[0].layout_item.labware for arg in args},
        )
        self.assert_supported_dispense_labware(
            *{opt.layout_item.labware for arg in args for opt in arg[1:]},
        )
        self.assert_supported_deck_locations(
            *{opt.layout_item.deck_location for arg in args for opt in arg},
        )
        self.assert_supported_tips(*args)
        self.assert_transfer_options(*args)
        # Check everything is kosher.

    def transfer(
        self: HamiltonPortraitCORE8ContactDispense,
        *args: tuple[AspirateOptions, *tuple[DispenseOptions, ...]],
    ) -> None:

        tip_assignments = [(arg, self._get_supported_tips(*arg)[-1]) for arg in args]
        # From our tip assignments we will always use the largest tip.
        # Liquid classes should be validated so we can be confident in a good transfer

        for pipette_options, pipette_tip in tip_assignments[:]:
            tip_assignments.remove((pipette_options, pipette_tip))
            # Remove the assignment initially, we will add it back by the end of the inner loop.

            aspirate_option = pipette_options[0]

            max_volume = pipette_tip.supported_aspirate_liquid_class_categories[
                aspirate_option.liquid_class_category
            ][-1].max_volume

            chunk: list[DispenseOptions] = []
            for dispense_option in pipette_options[1:]:
                chunk.append(dispense_option)

                chunk_volume = sum([opt.transfer_volume for opt in chunk])

                if chunk_volume > max_volume:
                    tip_assignments.append(
                        ((aspirate_option, *chunk[:-1]), pipette_tip),
                    )
                    chunk = chunk[-1:]

            if len(chunk) != 0:
                tip_assignments.append(
                    ((aspirate_option, *chunk), pipette_tip),
                )
        # Check that the total dispense volume can actually be aspirated by the liquid class.
        # If not, we need to split the dispense steps to fit the aspirate liquid class.

        for pipette_options, pipette_tip in tip_assignments[:]:
            aspirate_option = pipette_options[0]

            max_volume = pipette_tip.tip.volume

            for dispense_option in pipette_options[1:]:
                transfer_volume = dispense_option.transfer_volume

                if transfer_volume > max_volume:
                    tip_assignments.remove((pipette_options, pipette_tip))
                    # We are going to remake the assignment below.

                    new_dispense_option = copy(dispense_option)
                    # Make a copy of dispense option because we are going to change it.

                    num_aspirations = ceil(transfer_volume / max_volume)
                    new_dispense_option.transfer_volume /= num_aspirations

                    tip_assignments += [
                        ((aspirate_option, new_dispense_option), pipette_tip)
                        for _ in range(num_aspirations)
                    ]
        # Check that the total dispense volume can actually be aspirated by the tip
        # If not, we need to split the dispense steps to fit the tip volume.

        max_volume_per_liquid_class_category_combo: dict[str, float] = {}

        for option in options:
            max_volume_per_liquid_class_category_combo[
                f"{option.source_liquid_class_category}|{option.destination_liquid_class_category}"
            ] = self._get_max_transfer_volume(
                option.source_liquid_class_category,
                option.destination_liquid_class_category,
            )
        # We need to figure out across all options what our potential combos are.

        truncated_options: list[list[TransferOptions]] = []
        non_truncated_options: list[TransferOptions] = []
        for option in options:
            temp_options = self._truncate_transfer_volume(
                option,
                max_volume_per_liquid_class_category_combo[
                    f"{option.source_liquid_class_category}|{option.destination_liquid_class_category}"
                ],
            )

            if len(temp_options) > 1:
                non_truncated_options.append(temp_options[0])
                truncated_options.append(temp_options[1:])
            else:
                non_truncated_options += temp_options
            # We want to do the transfers in order. So any truncated transfers will come at the end.
        # do we now need to truncate volumes because they exceed the max supported by the liquid classes?

        options = non_truncated_options
        # We will transfer the original series first, then we will follow up with the rest of the truncated volumes.

        options += [
            option
            for option_list in itertools.zip_longest(
                *truncated_options,
                fillvalue=None,
            )
            for option in option_list
            if option is not None
        ]
        # Shuffle our truncated options then add to the end.

        options_with_tips: list[tuple[PipetteTip, TransferOptions]] = [
            (
                self._get_tip(
                    option.source_liquid_class_category,
                    option.destination_liquid_class_category,
                    option.transfer_volume,
                ),
                option,
            )
            for option in options
        ]
        # Connect our options with tips we will use.

        channel_grouped_options_with_tips = [
            options_with_tips[x : x + len(self.active_channels)]
            for x in range(0, len(options_with_tips), len(self.active_channels))
        ]

        for channel_group in channel_grouped_options_with_tips:
            self._pickup(
                *[
                    (self.active_channels[index], tip)
                    for index, (tip, option) in enumerate(channel_group)
                ],
            )

            aspdis_options: list[_AspirateDispenseOptions] = []
            for index, (tip, option) in enumerate(channel_group):
                pipettable_labware = cast(
                    labware.PipettableLabware,
                    option.source_layout_item.labware,
                )

                numeric_layout = labware.NumericLayout(
                    rows=pipettable_labware.layout.rows,
                    columns=pipettable_labware.layout.columns,
                    direction=pipettable_labware.layout.direction,
                )

                position = (
                    (int(numeric_layout.get_position_id(option.source_position)) - 1)
                    * pipettable_labware.well_definition.positions_per_well
                ) + (
                    (index % pipettable_labware.well_definition.positions_per_well) + 1
                )
                # It is possible for labware types to have multiple sequences per well.
                # This will spread channels across all wells for more efficient pipetting.
                # What is the math?
                # Assume we have a plate of 5 wells with 8 sequences per well.
                # position can be from 1 to 5 for the 5 wells
                # Thus, we subtract one from the positions to make it zero indexed.
                # Then we will multiply by 8 to get to the correct positionID. (1-1) * 8 = 0 so first well.
                # We get the remainder of the channel number by the sequence positions to make sure we do not overshoot.
                # Then add 1 to assign it to the channel specific well.

                aspdis_options.append(
                    _AspirateDispenseOptions(
                        channel_number=self.active_channels[index],
                        layout_item=option.source_layout_item,
                        position_id=pipettable_labware.layout.get_position_id(position),
                        well_volume=option.source_well_volume,
                        mix_cycles=option.source_mix_cycles,
                        mix_volume=option.source_well_volume * 0.8,
                        liquid_class=self._get_liquid_class(
                            option.source_liquid_class_category,
                            option.transfer_volume,
                        ),
                        volume=option.transfer_volume,
                    ),
                )

            self._aspirate(aspdis_options)

            aspdis_options: list[_AspirateDispenseOptions] = []
            for index, (tip, option) in enumerate(channel_group):
                pipettable_labware = cast(
                    labware.PipettableLabware,
                    option.destination_layout_item.labware,
                )

                numeric_layout = labware.NumericLayout(
                    rows=pipettable_labware.layout.rows,
                    columns=pipettable_labware.layout.columns,
                    direction=pipettable_labware.layout.direction,
                )

                position = (
                    (
                        int(numeric_layout.get_position_id(option.destination_position))
                        - 1
                    )
                    * pipettable_labware.well_definition.positions_per_well
                ) + (
                    (index % pipettable_labware.well_definition.positions_per_well) + 1
                )
                # It is possible for labware types to have multiple sequences per well.
                # This will spread channels across all wells for more efficient pipetting.
                # What is the math?
                # Assume we have a plate of 5 wells with 8 sequences per well.
                # position can be from 1 to 5 for the 5 wells
                # Thus, we subtract one from the positions to make it zero indexed.
                # Then we will multiply by 8 to get to the correct positionID. (1-1) * 8 = 0 so first well.
                # We get the remainder of the channel number by the sequence positions to make sure we do not overshoot.
                # Then add 1 to assign it to the channel specific well.

                aspdis_options.append(
                    _AspirateDispenseOptions(
                        channel_number=self.active_channels[index],
                        layout_item=option.destination_layout_item,
                        position_id=pipettable_labware.layout.get_position_id(position),
                        well_volume=option.destination_well_volume,
                        mix_cycles=option.destination_mix_cycles,
                        mix_volume=option.destination_well_volume * 0.8,
                        liquid_class=self._get_liquid_class(
                            option.destination_liquid_class_category,
                            option.transfer_volume,
                        ),
                        volume=option.transfer_volume,
                    ),
                )

            self._dispense(aspdis_options)

            option.destination_well_volume += option.transfer_volume

            self._eject_waste(
                *[
                    self.active_channels[index]
                    for index, (_, _) in enumerate(channel_group)
                ],
            )

    def transfer_time(
        self: HamiltonPortraitCORE8ContactDispense,
        *args: tuple[AspirateOptions, *tuple[DispenseOptions, ...]],
    ) -> float:
        return 0
