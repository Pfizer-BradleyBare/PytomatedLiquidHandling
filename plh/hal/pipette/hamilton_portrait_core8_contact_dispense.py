from __future__ import annotations

from typing import Literal, cast

from pydantic import dataclasses

from plh.driver.HAMILTON.backend import HamiltonBackendBase
from plh.driver.HAMILTON.ML_STAR import Channel1000uL

from .pipette_base import *
from .pipette_base import PipetteBase, TransferOptions
from .pipette_tip import PipetteTip


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
        tips: list[PipetteTip],
    ) -> None:
        if len(tips) > len(self.active_channels):
            raise RuntimeError("Cannot pickup more tips than you have channels.")
        # Does num of tips match num of channels?

        successful_pickups: dict[int, tuple[str, str]] = {}
        # We can track which pickups worked here, so we do not arbitrarily waste tips when a bad tip fails to be picked up.

        not_executed_pickups: dict[int, tuple[str, str]] = {}

        while True:
            command = Channel1000uL.Pickup.Command(
                backend_error_handling=False,
                options=[],
            )

            try:
                for channel_number, tip in zip(self.active_channels, tips):
                    if channel_number in successful_pickups:
                        continue
                    # We need to check first if any tips were successful in being picked up. If so, we do not need to pickup a tip with that channel.

                    try:
                        labware_id = tip.tip.available_positions[0].LabwareID
                        position_id = tip.tip.available_positions[0].PositionID
                        # There may not be any positions left. If not, we will catch that and raise a teir discard event.

                        command.options.append(
                            Channel1000uL.Pickup.Options(
                                ChannelNumber=channel_number,
                                LabwareID=labware_id,
                                PositionID=position_id,
                            ),
                        )
                    except IndexError as e:
                        raise RuntimeError("Out of tips in teir.") from e
                    # It is possible that there are not enough tips in the teir to support this pickup operation.
                    # We DO NOT want to hold tips when a teir is empty. We need to be able to grab the gripper.

                    tip.tip.use_tips(1)
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

                non_success_pickups = [
                    exception.HamiltonBlockData.num
                    for exception in exceptions
                    if exception.HamiltonBlockData is not None
                ]
                # We cannot be sure if block data will be present.

                for options in command.options:
                    if options.ChannelNumber not in non_success_pickups:
                        not_executed_pickups[options.ChannelNumber] = (
                            options.LabwareID,
                            options.PositionID,
                        )
                # We need to figure out which tips we should retry
                # We are guarenteed by the Hamilton response base object that all except groups will be flat.

            except* Channel1000uL.Pickup.exceptions.NoTipError as e:
                exceptions = cast(
                    tuple[Channel1000uL.Pickup.exceptions.NoTipError, ...],
                    e.exceptions,
                )
                # We are guarenteed by the Hamilton response base object that all except groups will be flat.

                non_success_pickups = [
                    exception.HamiltonBlockData.num
                    for exception in exceptions
                    if exception.HamiltonBlockData is not None
                ]
                # We cannot be sure if block data will be present.

                for options in command.options:
                    if (
                        options.ChannelNumber not in non_success_pickups
                        and options.ChannelNumber not in not_executed_pickups
                    ):
                        successful_pickups[options.ChannelNumber] = (
                            options.LabwareID,
                            options.PositionID,
                        )
                # We need to figure out which tips were picked up successfully.

    def _eject(
        self: HamiltonPortraitCORE8ContactDispense,
        labware_ids: list[str],
        position_ids: list[str],
    ) -> None:
        ...

    def transfer(
        self: HamiltonPortraitCORE8ContactDispense,
        options: list[TransferOptions],
    ) -> None:
        ...

    def time_to_transfer(
        self: HamiltonPortraitCORE8ContactDispense,
        options: list[TransferOptions],
    ) -> float:
        return 0
