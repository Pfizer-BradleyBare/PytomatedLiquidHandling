from __future__ import annotations

from typing import Literal, cast

from loguru import logger
from pydantic import dataclasses

from plh.driver.HAMILTON.backend import HamiltonBackendBase
from plh.driver.HAMILTON.ML_STAR import Channel1000uL
from plh.hal import labware, tip

from .pipette_base import *
from .pipette_base import (
    PipetteBase,
    TransferOptions,
    _AspirateDispenseOptions,
    _EjectOptions,
    _PickupOptions,
)


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
        options = sorted(options, key=lambda x: x.ChannelNumber)

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
                    if option.ChannelNumber in successful_pickups:
                        continue
                    # We need to check first if any tips were successful in being picked up. If so, we do not need to pickup a tip with that channel.

                    if option.ChannelNumber in not_executed_pickups:
                        command.options.append(
                            Channel1000uL.Pickup.Options(
                                ChannelNumber=option.ChannelNumber,
                                LabwareID=not_executed_pickups[option.ChannelNumber][0],
                                PositionID=not_executed_pickups[option.ChannelNumber][
                                    1
                                ],
                            ),
                        )
                        continue

                    try:
                        labware_id = option.PipetteTip.tip.available_positions[
                            0
                        ].LabwareID
                        position_id = option.PipetteTip.tip.available_positions[
                            0
                        ].PositionID
                        # There may not be any positions left. If not, we will catch that and raise a teir discard event.

                        command.options.append(
                            Channel1000uL.Pickup.Options(
                                ChannelNumber=option.ChannelNumber,
                                LabwareID=labware_id,
                                PositionID=position_id,
                            ),
                        )
                    except IndexError:
                        self._eject(
                            [
                                _EjectOptions(
                                    ChannelNumber=pickup_key,
                                    LabwareID=successful_pickups[pickup_key][0],
                                    PositionID=successful_pickups[pickup_key][1],
                                )
                                for pickup_key in successful_pickups
                            ],
                        )

                        raise ExceptionGroup(
                            "Errors during tip pickup",
                            [tip.TierOutOfTipsError(option.PipetteTip.tip)],
                        )
                    # It is possible that there are not enough tips in the teir to support this pickup operation.
                    # We DO NOT want to hold tips when a teir is empty. We need to be able to grab the gripper. So we will eject them.

                    option.PipetteTip.tip.use_tips(1)
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
        options = sorted(options, key=lambda x: x.ChannelNumber)

        command = Channel1000uL.Eject.Command(backend_error_handling=False, options=[])

        for option in options:
            command.options.append(
                Channel1000uL.Eject.Options(
                    ChannelNumber=option.ChannelNumber,
                    LabwareID=option.LabwareID,
                    PositionID=option.PositionID,
                ),
            )

        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, Channel1000uL.Eject.Response)

    def _aspirate(
        self: HamiltonPortraitCORE8ContactDispense,
        options: list[_AspirateDispenseOptions],
    ) -> None:
        options = sorted(options, key=lambda x: x.ChannelNumber)

        command = Channel1000uL.Aspirate.Command(
            backend_error_handling=False,
            options=[],
        )

        for option in options:
            command.options.append(
                Channel1000uL.Aspirate.Options(
                    ChannelNumber=option.ChannelNumber,
                    LabwareID=option.LayoutItem.labware_id,
                    PositionID=option.PositionID,
                    LiquidClass=option.LiquidClass,
                    Volume=option.Volume,
                    Mode=Channel1000uL.Aspirate.ModeOptions.AspirateAll,
                    CapacitiveLiquidLevelDetection=Channel1000uL.Aspirate.LLDOptions.Off,
                    SubmergeDepth=0,
                    PressureLiquidLevelDetection=Channel1000uL.Aspirate.LLDOptions.Off,
                    MaxHeightDifference=0,
                    FixHeightFromBottom=cast(
                        labware.PipettableLabware,
                        option.LayoutItem.labware,
                    ).get_height_from_volume(option.WellVolume),
                    RetractDistanceForTransportAir=5,
                    LiquidFollowing=Channel1000uL.Aspirate.YesNoOptions.Yes,
                    MixCycles=option.MixCycles,
                    MixPosition=0,
                    MixVolume=option.MixVolume,
                ),
            )

        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, Channel1000uL.Aspirate.Response)

    def _dispense(
        self: HamiltonPortraitCORE8ContactDispense,
        options: list[_AspirateDispenseOptions],
    ) -> None:
        options = sorted(options, key=lambda x: x.ChannelNumber)

        command = Channel1000uL.Dispense.Command(
            backend_error_handling=False,
            options=[],
        )

        for option in options:
            command.options.append(
                Channel1000uL.Dispense.Options(
                    ChannelNumber=option.ChannelNumber,
                    LabwareID=option.LayoutItem.labware_id,
                    PositionID=option.PositionID,
                    LiquidClass=option.LiquidClass,
                    Volume=option.Volume,
                    Mode=Channel1000uL.Dispense.ModeOptions.FromLiquidClassDefinition,
                    FixHeightFromBottom=cast(
                        labware.PipettableLabware,
                        option.LayoutItem.labware,
                    ).get_height_from_volume(option.WellVolume),
                    RetractDistanceForTransportAir=5,
                    CapacitiveLiquidLevelDetection=Channel1000uL.Dispense.LLDOptions.Off,
                    SubmergeDepth=0,
                    SideTouch=Channel1000uL.Dispense.YesNoOptions.No,
                    LiquidFollowing=Channel1000uL.Dispense.YesNoOptions.Yes,
                    MixCycles=option.MixCycles,
                    MixPosition=0,
                    MixVolume=option.MixVolume,
                ),
            )

        self.backend.execute(command)
        self.backend.wait(command)
        self.backend.acknowledge(command, Channel1000uL.Dispense.Response)

    def transfer(
        self: HamiltonPortraitCORE8ContactDispense,
        options: list[TransferOptions],
    ) -> None:
        ...

    def transfer_time(
        self: HamiltonPortraitCORE8ContactDispense,
        options: list[TransferOptions],
    ) -> float:
        return 0
