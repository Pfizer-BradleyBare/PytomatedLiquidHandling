from __future__ import annotations

from typing import Annotated, Literal, cast

from loguru import logger
from pydantic import dataclasses, field_validator
from pydantic.functional_validators import BeforeValidator

from plh.driver.HAMILTON.backend import HamiltonBackendBase
from plh.driver.HAMILTON.ML_STAR import Channel1000uL
from plh.hal import backend, labware, layout_item
from plh.hal.pipette.options import AspirateOptions, DispenseOptions

from .pipette_base import *
from .pipette_base import PipetteBase
from .pipette_tip import PipetteTip


@dataclasses.dataclass(kw_only=True, eq=False)
class HamiltonPortraitCORE8(PipetteBase):
    backend: Annotated[HamiltonBackendBase, BeforeValidator(backend.validate_instance)]

    active_channels: list[
        Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    ]

    @field_validator("active_channels", mode="after")
    @classmethod
    def __validate_active_channels(
        cls: type[HamiltonPortraitCORE8],
        v: list[int],
    ) -> list[int]:
        if len(v) != len(set(v)):
            raise ValueError("active_channels value must all be unique!")

        return v

    def assert_transfer_options(
        self: PipetteBase,
        *args: tuple[AspirateOptions, *tuple[DispenseOptions, ...]],
    ) -> None:
        """Portrait channels can pretty much handle any case. So nothing to check and assert here."""
        ...

    def initialize(self: HamiltonPortraitCORE8) -> None: ...

    def deinitialize(self: HamiltonPortraitCORE8) -> None: ...

    def _align_pipetting_channel(
        self: HamiltonPortraitCORE8,
        channel_number: int,
        layout_item: layout_item.LayoutItemBase,
        position: str | int,
    ) -> str:
        """Used to align a channel to the correct position in labware that have more than one sequence per well.
        Very important for efficient pipetting.
        """
        pipettable_labware = cast(
            labware.PipettableLabware,
            layout_item.labware,
        )

        numeric_layout = labware.NumericLayout(
            rows=pipettable_labware.layout.rows,
            columns=pipettable_labware.layout.columns,
            direction=pipettable_labware.layout.direction,
        )

        position = (
            (int(numeric_layout.get_position_id(position)) - 1)
            * pipettable_labware.well_definition.positions_per_well
        ) + (
            (channel_number % pipettable_labware.well_definition.positions_per_well) + 1
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

        return pipettable_labware.layout.get_position_id(position)

    def _pickup(
        self: HamiltonPortraitCORE8,
        *args: tuple[int, PipetteTip],
    ) -> None:
        """Tips is a list of tuples of (channel_number, Tip)"""
        args = tuple(sorted(args, key=lambda x: x[0]))

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
                for channel_number, pipette_tip in args:
                    if channel_number in successful_pickups:
                        continue
                    # We need to check first if any tips were successful in being picked up. If so, we do not need to pickup a tip with that channel.

                    if channel_number in not_executed_pickups:
                        command.options.append(
                            Channel1000uL.Pickup.Options(
                                ChannelNumber=channel_number,
                                LabwareID=not_executed_pickups[channel_number][0],
                                PositionID=not_executed_pickups[channel_number][1],
                            ),
                        )
                        continue
                    # If there are any not executed pickups then those will trump any new positions. Let's at least give the non-attempted positions a chance.

                    try:
                        labware_id = pipette_tip.tip.available_positions[0].LabwareID
                        position_id = pipette_tip.tip.available_positions[0].PositionID
                        # There may not be any positions left. If not, we will catch that and attempt to discard the teir.

                        command.options.append(
                            Channel1000uL.Pickup.Options(
                                ChannelNumber=channel_number,
                                LabwareID=labware_id,
                                PositionID=position_id,
                            ),
                        )
                    except IndexError as e:
                        if len(successful_pickups) != 0:
                            self._eject(
                                *[
                                    (
                                        pickup_key,
                                        (
                                            successful_pickups[pickup_key][0],
                                            successful_pickups[pickup_key][1],
                                        ),
                                    )
                                    for pickup_key in successful_pickups
                                ],
                            )
                        # We DO NOT want to hold tips when a teir is empty. We need to be able to grab the gripper. So we will eject them.

                        successful_pickups = {}
                        not_executed_pickups = {}
                        # We have ejected all tips and will discard a teir. We need to start fresh.

                        pipette_tip.tip.discard_teir()

                        raise IndexError from e
                        # Raise error to help us break out and start over with new teir

                    # It is possible that there are not enough tips in the teir to support this pickup operation.

                    pipette_tip.tip.use_tips(1)
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

            except* IndexError:
                # Restarts the while loop
                ...

    def _eject(
        self: HamiltonPortraitCORE8,
        *args: tuple[int, tuple[str, str]],
    ) -> None:
        """Positions is a list of tuple of (channel_number,(labware_id,position_id))."""
        args = tuple(sorted(args, key=lambda x: x[0]))

        command = Channel1000uL.Eject.Command(backend_error_handling=False, options=[])

        for channel_number, (labware_id, position_id) in args:
            command.options.append(
                Channel1000uL.Eject.Options(
                    ChannelNumber=channel_number,
                    LabwareID=labware_id,
                    PositionID=position_id,
                ),
            )

        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, Channel1000uL.Eject.Response)

    def _eject_waste(
        self: HamiltonPortraitCORE8,
        *args: int,
    ) -> None:
        self._eject(
            *[
                (channel_number, (self.waste_labware_id, str(channel_number)))
                for channel_number in args
            ],
        )
