from __future__ import annotations

import itertools
from typing import Literal, cast

from loguru import logger
from pydantic import dataclasses

from plh.driver.HAMILTON.backend import HamiltonBackendBase
from plh.driver.HAMILTON.ML_STAR import Channel1000uL
from plh.hal import labware, tip

from .options import (
    TransferOptions,
    _AspirateDispenseOptions,
    _EjectOptions,
    _PickupOptions,
)
from .pipette_base import *
from .pipette_base import PipetteBase


@dataclasses.dataclass(kw_only=True)
class HamiltonPortraitCORE8ContactDispense(PipetteBase):
    backend: HamiltonBackendBase
    active_channels: list[Literal[1, 2, 3, 4, 5, 6, 7, 8]]

    def initialize(self: HamiltonPortraitCORE8ContactDispense) -> None:
        ...

    def deinitialize(self: HamiltonPortraitCORE8ContactDispense) -> None:
        ...

    def _pickup(
        self: HamiltonPortraitCORE8ContactDispense,
        options: list[_PickupOptions],
    ) -> None:
        """Tips is a list of tuples of (channel_number, Tip)"""
        options = sorted(options, key=lambda x: x.channel_number)

        successful_pickups: dict[int, tuple[str, str]] = {}
        # We can track which pickups worked here, so we do not arbitrarily waste tips when a bad tip fails to be picked up.

        not_executed_pickups: dict[int, tuple[str, str]] = {}
        # If a tip isn't executed we may want to save it and try again. We only want to abort NoTipErrors

        while True:
            command = Channel1000uL.Pickup.Command(
                backend_error_handling=False,
                options=[],
            )

            try:
                for option in options:
                    if option.channel_number in successful_pickups:
                        continue
                    # We need to check first if any tips were successful in being picked up. If so, we do not need to pickup a tip with that channel.

                    if option.channel_number in not_executed_pickups:
                        command.options.append(
                            Channel1000uL.Pickup.Options(
                                ChannelNumber=option.channel_number,
                                LabwareID=not_executed_pickups[option.channel_number][
                                    0
                                ],
                                PositionID=not_executed_pickups[option.channel_number][
                                    1
                                ],
                            ),
                        )
                        continue
                    # If there are any not executed pickups then those will trump any new positions. Let's at least give the non-attempted positions a chance.

                    try:
                        labware_id = option.pipette_tip.tip.available_positions[
                            0
                        ].LabwareID
                        position_id = option.pipette_tip.tip.available_positions[
                            0
                        ].PositionID
                        # There may not be any positions left. If not, we will catch that and raise a teir discard event.

                        command.options.append(
                            Channel1000uL.Pickup.Options(
                                ChannelNumber=option.channel_number,
                                LabwareID=labware_id,
                                PositionID=position_id,
                            ),
                        )
                    except IndexError:
                        self._eject(
                            [
                                _EjectOptions(
                                    channel_number=pickup_key,
                                    labware_id=successful_pickups[pickup_key][0],
                                    position_id=successful_pickups[pickup_key][1],
                                )
                                for pickup_key in successful_pickups
                            ],
                        )

                        raise ExceptionGroup(
                            "Errors during tip pickup",
                            [tip.exceptions.TierOutOfTipsError(option.pipette_tip.tip)],
                        )
                    # It is possible that there are not enough tips in the teir to support this pickup operation.
                    # We DO NOT want to hold tips when a teir is empty. We need to be able to grab the gripper. So we will eject them.

                    option.pipette_tip.tip.use_tips(1)
                    # We are going to assume straight off that the pickup will be successful. If it is not then we will handle later.

                not_executed_pickups = {}
                # We will rebild our not executed pickups on each round as needed.

                self.backend.execute(command)
                self.backend.wait(command)
                self.backend.acknowledge(command, Channel1000uL.Pickup.Response)
                # Give 'er a shot

                break
                # Yay we picked up the tips!

            except* Channel1000uL.Pickup.exceptions.NotExecutedError as e:
                exceptions = cast(
                    tuple[Channel1000uL.Pickup.exceptions.NotExecutedError, ...],
                    e.exceptions,
                )

                logger.info(exceptions)

                non_executed_pickups = [
                    exception.HamiltonBlockData.num
                    for exception in exceptions
                    if exception.HamiltonBlockData is not None
                ]
                # We cannot be sure if block data will be present.

                for option in command.options:
                    if option.ChannelNumber in non_executed_pickups:
                        not_executed_pickups[option.ChannelNumber] = (
                            option.LabwareID,
                            option.PositionID,
                        )
                # We need to figure out which tips we should retry
                # We are guarenteed by the Hamilton response base object that all except groups will be flat.

            except* Channel1000uL.Pickup.exceptions.NoTipError as e:
                exceptions = cast(
                    tuple[Channel1000uL.Pickup.exceptions.NoTipError, ...],
                    e.exceptions,
                )
                # We are guarenteed by the Hamilton response base object that all except groups will be flat.

                logger.info(exceptions)

                non_success_pickups = [
                    exception.HamiltonBlockData.num
                    for exception in exceptions
                    if exception.HamiltonBlockData is not None
                ]
                # We cannot be sure if block data will be present.

                for option in command.options:
                    if (
                        option.ChannelNumber not in non_success_pickups
                        and option.ChannelNumber not in not_executed_pickups
                    ):
                        successful_pickups[option.ChannelNumber] = (
                            option.LabwareID,
                            option.PositionID,
                        )
                # We need to figure out which tips were picked up successfully.

    def _eject(
        self: HamiltonPortraitCORE8ContactDispense,
        options: list[_EjectOptions],
    ) -> None:
        """Positions is a list of tuple of (channel_number,(labware_id,position_id))."""
        options = sorted(options, key=lambda x: x.channel_number)

        command = Channel1000uL.Eject.Command(backend_error_handling=False, options=[])

        for option in options:
            command.options.append(
                Channel1000uL.Eject.Options(
                    ChannelNumber=option.channel_number,
                    LabwareID=option.labware_id,
                    PositionID=option.position_id,
                ),
            )

        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, Channel1000uL.Eject.Response)

    def _waste(
        self: HamiltonPortraitCORE8ContactDispense,
        channel_numbers: list[int],
    ) -> None:
        self._eject(
            [
                _EjectOptions(
                    channel_number=channel_number,
                    labware_id=self.waste_labware_id,
                    position_id=str(channel_number),
                )
                for channel_number in channel_numbers
            ],
        )

    def _aspirate(
        self: HamiltonPortraitCORE8ContactDispense,
        options: list[_AspirateDispenseOptions],
    ) -> None:
        options = sorted(options, key=lambda x: x.channel_number)

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
                    Mode=Channel1000uL.Aspirate.ModeOptions.AspirateAll,
                    CapacitiveLiquidLevelDetection=Channel1000uL.Aspirate.LLDOptions.Off,
                    SubmergeDepth=0,
                    PressureLiquidLevelDetection=Channel1000uL.Aspirate.LLDOptions.Off,
                    MaxHeightDifference=0,
                    FixHeightFromBottom=cast(
                        labware.PipettableLabware,
                        option.layout_item.labware,
                    ).get_height_from_volume(option.well_volume),
                    RetractDistanceForTransportAir=5,
                    LiquidFollowing=Channel1000uL.Aspirate.YesNoOptions.Yes,
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
        options: list[_AspirateDispenseOptions],
    ) -> None:
        options = sorted(options, key=lambda x: x.channel_number)

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
                    Mode=Channel1000uL.Dispense.ModeOptions.FromLiquidClassDefinition,
                    FixHeightFromBottom=cast(
                        labware.PipettableLabware,
                        option.layout_item.labware,
                    ).get_height_from_volume(option.well_volume),
                    RetractDistanceForTransportAir=5,
                    CapacitiveLiquidLevelDetection=Channel1000uL.Dispense.LLDOptions.Off,
                    SubmergeDepth=0,
                    SideTouch=Channel1000uL.Dispense.YesNoOptions.No,
                    LiquidFollowing=Channel1000uL.Dispense.YesNoOptions.Yes,
                    MixCycles=option.mix_cycles,
                    MixPosition=0,
                    MixVolume=option.mix_volume,
                ),
            )

        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, Channel1000uL.Dispense.Response)

    def transfer(
        self: HamiltonPortraitCORE8ContactDispense,
        options: list[TransferOptions],
    ) -> None:
        # assuming the options are sorted for now.

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
                [
                    _PickupOptions(
                        channel_number=self.active_channels[index],
                        pipette_tip=tip,
                    )
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

            self._eject(
                [
                    _EjectOptions(
                        channel_number=self.active_channels[index],
                        labware_id=self.waste_labware_id,
                        position_id=str(self.active_channels[index]),
                    )
                    for index, (tip, option) in enumerate(channel_group)
                ],
            )

    def transfer_time(
        self: HamiltonPortraitCORE8ContactDispense,
        options: list[TransferOptions],
    ) -> float:
        return 0
