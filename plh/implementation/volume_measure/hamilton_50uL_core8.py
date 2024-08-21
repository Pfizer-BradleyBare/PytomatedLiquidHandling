from __future__ import annotations

from dataclasses import field
from typing import Annotated, DefaultDict, cast

from pydantic import dataclasses, model_validator
from pydantic.functional_validators import BeforeValidator

from plh.device.HAMILTON.backend import HamiltonBackendBase
from plh.device.HAMILTON.HSLLabwrAccess import AbsolutePositionValuesGetForLabwareID
from plh.device.HAMILTON.ML_STAR import Channel1000uL
from plh.implementation import carrier_location, labware, layout_item, pipette

from .volume_measure_base import MeasureValues, VolumeMeasureBase


@dataclasses.dataclass(kw_only=True, eq=False)
class Hamilton50uLCORE8(VolumeMeasureBase):
    """Device that can be used to measure the volume of liquid in a container."""

    pipette: Annotated[
        pipette.HamiltonPortraitCORE8,
        BeforeValidator(pipette.validate_instance),
    ]

    backend: HamiltonBackendBase = field(init=False)

    supported_labware: Annotated[
        list[labware.PipettableLabware],
        BeforeValidator(labware.validate_list),
    ] = field(init=False)

    supported_deck_locations: Annotated[
        list[carrier_location.CarrierLocationBase],
        BeforeValidator(carrier_location.validate_list),
    ] = field(init=False)

    _pipette_tip: pipette.PipetteTip = field(init=False)

    def initialize(self: Hamilton50uLCORE8) -> None:
        self.pipette.initialize()

    def deinitialize(self: Hamilton50uLCORE8) -> None:
        self.pipette.deinitialize()

    @model_validator(mode="after")
    def __model_validate(self: Hamilton50uLCORE8) -> Hamilton50uLCORE8:

        tips = {tip.tip.volume: tip for tip in self.pipette.supported_tips}

        try:
            self._pipette_tip = tips[50]
        except KeyError as e:
            msg = "50uL tip not available with the chosen pipette."
            raise ValueError(msg) from e

        self.supported_labware = self.pipette.supported_aspirate_labware
        self.supported_deck_locations = self.pipette.supported_deck_locations
        self.backend = self.pipette.backend
        # Copy this info from the pipette because it drives our compatibility

        return self

    def measure(
        self: Hamilton50uLCORE8,
        *args: tuple[layout_item.LayoutItemBase, int | str],
    ) -> list[MeasureValues]:
        """Measures volume and returns a list of MeasureValues."""
        if len(args) > self._pipette_tip.tip.remaining_tips():
            raise RuntimeError("Not enough tips remaining to do this measurement.")

        layout_items = {layout_item for layout_item, _ in args}

        command = AbsolutePositionValuesGetForLabwareID.Command(
            options=[
                AbsolutePositionValuesGetForLabwareID.Options(
                    LabwareID=layout_item.labware_id,
                )
                for layout_item in layout_items
            ],
        )
        self.backend.execute(command)
        self.backend.wait(command)

        z_heights = {
            layout_item: labware_position.ZPosition
            for layout_item, labware_position in zip(
                layout_items,
                self.backend.acknowledge(
                    command,
                    AbsolutePositionValuesGetForLabwareID.Response,
                ).LabwarePositions,
            )
        }
        # Collect Z heights

        tip_length = 42.3
        # 50uL tip height

        layout_item_positions: dict[layout_item.LayoutItemBase, list[str | int]] = (
            DefaultDict(list)
        )
        grouped_layout_item_positions: dict[
            layout_item.LayoutItemBase,
            list[list[str]],
        ] = DefaultDict(list)

        for layout_item, position in args:
            layout_item_positions[layout_item].append(position)
        # Collect positions organized by layout item

        for layout_item, positions in layout_item_positions.items():
            groups = layout_item.labware.layout.group_positions_columnwise(
                positions,
            )

            grouped_layout_item_positions[layout_item] = [
                group[i : i + len(self.pipette.active_channels)]
                for group in groups
                for i in range(0, len(group), len(self.pipette.active_channels))
            ]
            # Max number in each group is number of active channels

        liquid_levels: dict[tuple, list[float]] = DefaultDict(list)

        for layout_item, grouped_positions in grouped_layout_item_positions.items():
            for group in grouped_positions:
                self.pipette._pickup(
                    *[
                        (self.pipette.active_channels[index], self._pipette_tip)
                        for index, position in enumerate(group)
                    ],
                )

                command = Channel1000uL.Aspirate.Command(
                    backend_error_handling=False,
                    options=[],
                )
                for index, pos_id in enumerate(group):
                    pipettable_labware = cast(
                        labware.PipettableLabware,
                        layout_item.labware,
                    )

                    numeric_layout = labware.NumericLayout(
                        rows=pipettable_labware.layout.rows,
                        columns=pipettable_labware.layout.columns,
                        direction=pipettable_labware.layout.direction,
                    )

                    true_position = (
                        (int(numeric_layout.get_position_id(pos_id)) - 1)
                        * pipettable_labware.positions_per_well
                    ) + ((index % pipettable_labware.positions_per_well) + 1)
                    # It is possible for labware types to have multiple sequences per well.
                    # This will spread channels across all wells for more efficient pipetting.
                    # What is the math?
                    # Assume we have a plate of 5 wells with 8 sequences per well.
                    # position can be from 1 to 5 for the 5 wells
                    # Thus, we subtract one from the positions to make it zero indexed.
                    # Then we will multiply by 8 to get to the correct positionID. (1-1) * 8 = 0 so first well.
                    # We get the remainder of the channel number by the sequence positions to make sure we do not overshoot.
                    # Then add 1 to assign it to the channel specific well.

                    command.options.append(
                        Channel1000uL.Aspirate.Options(
                            ChannelNumber=self.pipette.active_channels[index],
                            LabwareID=layout_item.labware_id,
                            PositionID=layout_item.labware.layout.get_position_id(
                                true_position,
                            ),
                            LiquidClass=list(
                                self._pipette_tip.supported_aspirate_liquid_class_categories.values(),
                            )[0][0].liquid_class_name,
                            Volume=0,
                            Mode=Channel1000uL.Aspirate.AspirateModeOptions.AspirateAll,
                            SubmergeDepth=0,
                            PressureLiquidLevelDetection=Channel1000uL.Aspirate.LLDOptions.High,
                            RetractDistanceForTransportAir=5,
                        ),
                    )

                self.backend.execute(command)
                self.backend.wait(command)
                self.backend.acknowledge(command, Channel1000uL.Aspirate.Response)
                # Do the dummy aspiration.

                self.pipette._eject_waste(
                    *[
                        self.pipette.active_channels[index]
                        for index, position in enumerate(group)
                    ],
                )

                command = Channel1000uL.GetLastLiquidLevel.Command()
                self.backend.execute(command)
                self.backend.wait(command)
                channel_liquid_levels = self.backend.acknowledge(
                    command,
                    Channel1000uL.GetLastLiquidLevel.Response,
                ).ChannelLiquidLevels

                for index, pos_id in enumerate(group):
                    liquid_levels[(layout_item, pos_id)].append(
                        float(channel_liquid_levels.block_data[index].step_data),
                    )
                # Get them measured liquid levels.

        out = []
        for layout_item, position in args:
            pos_id = layout_item.labware.layout.get_position_id(position)

            liquid_level = liquid_levels[(layout_item, pos_id)].pop(0)

            height = liquid_level - z_heights[layout_item] - tip_length
            volume = cast(
                labware.PipettableLabware,
                layout_item.labware,
            ).interpolate_height(height)

            out.append(MeasureValues(volume=volume, height=height))

        return out
        # Calculate the volume
