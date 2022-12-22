from typing import Callable

from ...Driver.NOP import NOPCommand
from ...Driver.Tools import Command, CommandTracker
from ..Labware import LabwareTracker
from ..Pipette import TransferOptionsTracker
from .BasePipette import Pipette, PipetteTipTracker, PipettingDeviceTypes


class Pipette96Channel(Pipette):
    def __init__(
        self,
        Enabled: bool,
        SupoortedPipetteTipTrackerInstance: PipetteTipTracker,
        SupportedLabwareTrackerInstance: LabwareTracker,
    ):
        Pipette.__init__(
            self,
            PipettingDeviceTypes.Pipette96Channel,
            Enabled,
            SupoortedPipetteTipTrackerInstance,
            SupportedLabwareTrackerInstance,
        )

    def Initialize(
        self,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            NOPCommand(
                "Pipette96Channel Initialize NOP",
                CallbackFunction,
                CallbackArgs,
            )
        )

        return ReturnCommandTracker

    def Deinitialize(
        self,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            NOPCommand(
                "Pipette96Channel Deinitialize NOP",
                CallbackFunction,
                CallbackArgs,
            )
        )

        return ReturnCommandTracker

    def Transfer(
        self,
        TransferOptionsTrackerInstance: TransferOptionsTracker,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:
        ...
