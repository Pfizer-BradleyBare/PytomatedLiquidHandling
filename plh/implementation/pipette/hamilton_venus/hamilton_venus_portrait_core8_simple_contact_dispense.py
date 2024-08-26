from __future__ import annotations

from copy import copy
from math import ceil
from typing import DefaultDict, cast

from pydantic import dataclasses

from plh.device.hamilton_venus.ML_STAR import Channel1000uL
from plh.implementation import labware
from plh.implementation import layout_item as li

from ..options import (
    AspirateOptions,
    DispenseOptions,
)
from ..pipette_tip import PipetteTip
from .hamilton_venus_portrait_core8 import HamiltonPortraitCORE8


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonPortraitCORE8SimpleContactDispense(HamiltonPortraitCORE8):
    def _aspirate(
        self: HamiltonPortraitCORE8SimpleContactDispense,
        *args: tuple[
            int,
            str,
            str,
            float,
            int,
            float,
            str,
            float,
        ],
    ) -> None:

        options = sorted(args, key=lambda x: x[0])

        command = Channel1000uL.Aspirate.Command(
            backend_error_handling=False,
            options=[],
        )

        for (
            channel_number,
            labware_id,
            position_id,
            tip_height,
            mix_cycles,
            mix_volume,
            liquid_class,
            volume,
        ) in options:
            command.options.append(
                Channel1000uL.Aspirate.Options(
                    ChannelNumber=channel_number,
                    LabwareID=labware_id,
                    PositionID=position_id,
                    LiquidClass=liquid_class,
                    Volume=volume,
                    Mode=Channel1000uL.Aspirate.AspirateModeOptions.AspirateAll,
                    CapacitiveLiquidLevelDetection=Channel1000uL.Aspirate.LLDOptions.Off,
                    SubmergeDepth=0,
                    PressureLiquidLevelDetection=Channel1000uL.Aspirate.LLDOptions.Off,
                    MaxHeightDifference=0,
                    FixHeightFromBottom=tip_height,
                    RetractDistanceForTransportAir=5,
                    LiquidFollowing=True,
                    MixCycles=mix_cycles,
                    MixPosition=0,
                    MixVolume=mix_volume,
                ),
            )

        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, Channel1000uL.Aspirate.Response)

    def _dispense(
        self: HamiltonPortraitCORE8SimpleContactDispense,
        *args: tuple[
            int,
            str,
            str,
            float,
            int,
            float,
            str,
            float,
        ],
    ) -> None:
        options = sorted(args, key=lambda x: x[0])

        command = Channel1000uL.Dispense.Command(
            backend_error_handling=False,
            options=[],
        )

        for (
            channel_number,
            labware_id,
            position_id,
            tip_height,
            mix_cycles,
            mix_volume,
            liquid_class,
            volume,
        ) in options:
            command.options.append(
                Channel1000uL.Dispense.Options(
                    ChannelNumber=channel_number,
                    LabwareID=labware_id,
                    PositionID=position_id,
                    LiquidClass=liquid_class,
                    Volume=volume,
                    Mode=Channel1000uL.Dispense.DispenseModeOptions.FromLiquidClassDefinition,
                    FixHeightFromBottom=tip_height,
                    RetractDistanceForTransportAir=5,
                    CapacitiveLiquidLevelDetection=Channel1000uL.Dispense.LLDOptions.Off,
                    SubmergeDepth=0,
                    SideTouch=False,
                    LiquidFollowing=True,
                    MixCycles=mix_cycles,
                    MixPosition=0,
                    MixVolume=mix_volume,
                ),
            )

        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, Channel1000uL.Dispense.Response)

    def transfer(
        self: HamiltonPortraitCORE8SimpleContactDispense,
        *args: tuple[AspirateOptions, *tuple[DispenseOptions, ...]],
    ) -> None:

        self.assert_supported_aspirate_labware(
            *{arg[0].layout_item.labware for arg in args},
        )
        self.assert_supported_dispense_labware(
            *{opt.layout_item.labware for arg in args for opt in arg[1:]},
        )
        self.assert_supported_carrier_locations(
            *{opt.layout_item.carrier_location for arg in args for opt in arg},
        )
        self.assert_supported_tips(*args)
        self.assert_transfer_options(*args)
        if not all(
            isinstance(layout_item, li.hamilton_venus.HamiltonVenusLayoutItemBase)
            for layout_item, position in args
        ):
            raise ValueError("Only HamiltonLayoutItemBase are accepted.")
        # Check everything is kosher.

        for arg in args:
            for pipette_option in arg:
                pipette_option.position = (
                    pipette_option.layout_item.labware.layout.get_position_id(
                        pipette_option.position,
                    )
                )
        # convert all positions to a string

        tip_assignments = [(arg, self._get_supported_tips(*arg)[-1]) for arg in args]
        # From our tip assignments we will always use the largest tip.
        # Liquid classes should be validated so we can be confident in a precise transfer

        for pipette_options, pipette_tip in tip_assignments[:]:
            tip_assignments.remove((pipette_options, pipette_tip))
            # Remove the assignment initially, we will add it back by the end of the inner loop.

            aspirate_option = pipette_options[0]

            max_volume = pipette_tip.tip.volume

            for dispense_option in pipette_options[1:]:
                required_volume = dispense_option.transfer_volume

                if required_volume > max_volume:
                    new_dispense_option = copy(dispense_option)
                    # Make a copy of dispense option because we are going to change it.

                    num_aspirations = ceil(required_volume / max_volume)
                    new_dispense_option.transfer_volume /= num_aspirations

                    tip_assignments += [
                        ((aspirate_option, new_dispense_option), pipette_tip)
                        for _ in range(num_aspirations)
                    ]
                else:
                    tip_assignments.append(
                        ((aspirate_option, dispense_option), pipette_tip),
                    )
        # This is a simple pipettor so we are going to flatten the repeat dispense steps into a single aspirate and dispense.
        # We also check that the volume is supported by the tip. If not, then we need to split into multiple aspirate and dispense steps.

        #
        #
        # At this point the pipette steps have a tip assigned and the steps are guarenteed to be supported by the liquid classes and tip volumes.
        #
        #

        tip_groups: dict[
            PipetteTip,
            list[tuple[AspirateOptions, *tuple[DispenseOptions, ...]]],
        ] = DefaultDict(list)
        for pipette_options, pipette_tip in tip_assignments:
            tip_groups[pipette_tip].append(pipette_options)
        # group by tip

        tip_layout_item_groups: dict[
            PipetteTip,
            dict[
                li.LayoutItemBase,
                list[tuple[AspirateOptions, *tuple[DispenseOptions, ...]]],
            ],
        ] = {}
        for pipette_tip, pipette_groups in tip_groups.items():
            layout_item_groups: dict[
                li.LayoutItemBase,
                list[tuple[AspirateOptions, *tuple[DispenseOptions, ...]]],
            ] = DefaultDict(list)

            for pipette_options in pipette_groups:
                aspirate_option, dispense_option = pipette_options
                # Unpack. We are guarenteed that only two options will be present.

                layout_item_groups[dispense_option.layout_item].append(pipette_options)

            tip_layout_item_groups[pipette_tip] = layout_item_groups
        # group by destination layout_item

        tip_layout_item_cycle_groups: dict[
            PipetteTip,
            dict[
                li.LayoutItemBase,
                list[list[tuple[AspirateOptions, *tuple[DispenseOptions, ...]]]],
            ],
        ] = {}
        for pipette_tip, layout_item_groups in tip_layout_item_groups.items():

            layout_item_cycle_groups: dict[
                li.LayoutItemBase,
                list[list[tuple[AspirateOptions, *tuple[DispenseOptions, ...]]]],
            ] = {}

            for (
                layout_item,
                pipette_groups,
            ) in layout_item_groups.items():

                cycle_counter: dict[str, int] = DefaultDict(int)
                groups_dict: dict[
                    int,
                    list[tuple[AspirateOptions, *tuple[DispenseOptions, ...]]],
                ] = DefaultDict(list)

                for pipette_options in pipette_groups:
                    aspirate_option, dispense_option = pipette_options

                    position: str = str(dispense_option.position)

                    groups_dict[cycle_counter[position]].append(pipette_options)

                    cycle_counter[position] += 1

                cycle_groups: list[
                    list[tuple[AspirateOptions, *tuple[DispenseOptions, ...]]]
                ] = list(groups_dict.values())

                layout_item_cycle_groups[layout_item] = cycle_groups

            tip_layout_item_cycle_groups[pipette_tip] = layout_item_cycle_groups
        # Lets say we have to split a dispense step into 2 or more parts (required volume is higher than tip volume).
        # We should try to pipette in cycles, thus we will pipette the first part first then the second part, etc. until the full volume is satisfied.
        # Create the pipette cycles

        tip_layout_item_cycle_column_groups: dict[
            PipetteTip,
            dict[
                li.LayoutItemBase,
                list[list[list[tuple[AspirateOptions, *tuple[DispenseOptions, ...]]]]],
            ],
        ] = {}

        for (
            pipette_tip,
            layout_item_cycle_groups,
        ) in tip_layout_item_cycle_groups.items():

            layout_item_cycle_column_groups: dict[
                li.LayoutItemBase,
                list[list[list[tuple[AspirateOptions, *tuple[DispenseOptions, ...]]]]],
            ] = {}

            for layout_item, cycle_groups in layout_item_cycle_groups.items():

                cycle_column_groups: list[
                    list[list[tuple[AspirateOptions, *tuple[DispenseOptions, ...]]]]
                ] = []

                for pipette_groups in cycle_groups:
                    positions = {
                        pipette_options[1].position: pipette_options
                        for pipette_options in pipette_groups
                    }

                    position_groups = (
                        layout_item.labware.layout.group_positions_columnwise(
                            list(positions.keys()),
                        )
                    )

                    column_groups = [
                        [positions[position] for position in group]
                        for group in position_groups
                    ]

                cycle_column_groups.append(column_groups)

            layout_item_cycle_column_groups[layout_item] = cycle_column_groups

        tip_layout_item_cycle_column_groups[pipette_tip] = (
            layout_item_cycle_column_groups
        )
        # group by column because hamilton tips are always column aligned.

        well_volume_tracker: dict[tuple[li.LayoutItemBase, str | int], float] = {}

        for (aspirate_option, dispense_option), _ in tip_assignments:
            well_volume_tracker[
                (aspirate_option.layout_item, aspirate_option.position)
            ] = aspirate_option.current_volume
            well_volume_tracker[
                (dispense_option.layout_item, dispense_option.position)
            ] = dispense_option.current_volume
        # Use this to track the volumes as we asp and disp

        #
        #
        # At this point the pipette steps have been grouped in the following way: tip -> destination layout_item -> cycle -> column
        #
        #

        for (
            pipette_tip,
            layout_item_cycle_column_groups,
        ) in tip_layout_item_cycle_column_groups.items():
            for cycle_column_groups in layout_item_cycle_column_groups.values():
                for column_groups in cycle_column_groups:
                    for column_group in column_groups:

                        channel_groups = [
                            column_group[x : x + len(self.active_channels)]
                            for x in range(
                                0,
                                len(column_group),
                                len(self.active_channels),
                            )
                        ]
                        # It is possible to have more or less channels than grouped rows per column. So we need to channel group them

                        for channel_group in channel_groups:

                            self._pickup(
                                *[
                                    (channel_number, pipette_tip)
                                    for channel_number, _ in zip(
                                        self.active_channels,
                                        channel_group,
                                    )
                                ],
                            )

                            aspirate_options: list[
                                tuple[
                                    int,
                                    str,
                                    str,
                                    float,
                                    int,
                                    float,
                                    str,
                                    float,
                                ]
                            ] = []

                            dispense_options: list[
                                tuple[
                                    int,
                                    str,
                                    str,
                                    float,
                                    int,
                                    float,
                                    str,
                                    float,
                                ]
                            ] = []

                            for channel_number, (
                                aspirate_option,
                                dispense_option,
                            ) in zip(self.active_channels, channel_group):

                                aspirate_well_volume = well_volume_tracker[
                                    (
                                        aspirate_option.layout_item,
                                        aspirate_option.position,
                                    )
                                ]

                                well_volume_tracker[
                                    (
                                        aspirate_option.layout_item,
                                        aspirate_option.position,
                                    )
                                ] -= dispense_option.transfer_volume

                                dispense_well_volume = well_volume_tracker[
                                    (
                                        dispense_option.layout_item,
                                        dispense_option.position,
                                    )
                                ]

                                well_volume_tracker[
                                    (
                                        dispense_option.layout_item,
                                        dispense_option.position,
                                    )
                                ] += dispense_option.transfer_volume

                                transfer_volume = dispense_option.transfer_volume

                                aspirate_options.append(
                                    (
                                        channel_number,
                                        cast(
                                            li.hamilton_venus.HamiltonVenusLayoutItemBase,
                                            aspirate_option.layout_item,
                                        ).labware_id,
                                        self._align_pipetting_channel(
                                            channel_number,
                                            aspirate_option.layout_item,
                                            aspirate_option.position,
                                        ),
                                        cast(
                                            labware.PipettableLabware,
                                            aspirate_option.layout_item.labware,
                                        ).interpolate_volume(aspirate_well_volume),
                                        aspirate_option.mix_cycles,
                                        aspirate_well_volume * 0.75,
                                        pipette_tip.get_aspirate_liquid_class(
                                            aspirate_option.liquid_class_category,
                                            transfer_volume,
                                        ).liquid_class_name,
                                        transfer_volume,
                                    ),
                                )

                                dispense_options.append(
                                    (
                                        channel_number,
                                        cast(
                                            li.hamilton_venus.HamiltonVenusLayoutItemBase,
                                            dispense_option.layout_item,
                                        ).labware_id,
                                        self._align_pipetting_channel(
                                            channel_number,
                                            dispense_option.layout_item,
                                            dispense_option.position,
                                        ),
                                        cast(
                                            labware.PipettableLabware,
                                            dispense_option.layout_item.labware,
                                        ).interpolate_volume(aspirate_well_volume),
                                        dispense_option.mix_cycles,
                                        (dispense_well_volume + transfer_volume) * 0.75,
                                        pipette_tip.get_aspirate_liquid_class(
                                            dispense_option.liquid_class_category,
                                            transfer_volume,
                                        ).liquid_class_name,
                                        transfer_volume,
                                    ),
                                )

                            self._aspirate(*aspirate_options)
                            # asp

                            self._dispense(*dispense_options)
                            # Disp

                            self._eject_waste(
                                *[
                                    channel_number
                                    for channel_number, _ in zip(
                                        self.active_channels,
                                        channel_group,
                                    )
                                ],
                            )

    def transfer_time(
        self: HamiltonPortraitCORE8SimpleContactDispense,
        *args: tuple[AspirateOptions, *tuple[DispenseOptions, ...]],
    ) -> float:
        return 0
