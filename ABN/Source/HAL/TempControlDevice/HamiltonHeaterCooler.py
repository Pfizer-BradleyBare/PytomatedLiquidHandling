from typing import Callable

from ...Driver.NOP import NOPCommand
from ...Driver.TemperatureControl.HeaterCooler import (
    ConnectCommand,
    ConnectOptions,
    GetTemperatureCommand,
    GetTemperatureOptions,
    StartTemperatureControlCommand,
    StartTemperatureControlOptions,
    StopTemperatureControlCommand,
    StopTemperatureControlOptions,
)
from ...Driver.Tools import Command, CommandTracker, ExecuteCallback
from ..Layout import LayoutItemGroupingTracker
from .BaseTempControlDevice import TempControlDevice, TempLimits
from .BaseTempControlDevice.Interface import UpdateCurrentTemperatureCallback


class HamiltonHeaterCooler(TempControlDevice):
    def __init__(
        self,
        Name: str,
        ComPort: str,
        TempLimitsInstance: TempLimits,
        LayoutItemGroupingTrackerInstance: LayoutItemGroupingTracker,
    ):
        TempControlDevice.__init__(
            self,
            Name,
            ComPort,
            False,
            TempLimitsInstance,
            LayoutItemGroupingTrackerInstance,
        )
        self.HandleID: str

    def Initialize(
        self,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:
        def InitializeCallback(CommandInstance: Command, args: tuple):

            TempControlDeviceInstance: TempControlDevice = args[0]
            ResponseInstance = CommandInstance.GetResponse()

            TempControlDeviceInstance.HandleID = ResponseInstance.GetAdditional()[
                "HandleID"
            ]

            ExecuteCallback(args[1], CommandInstance, args[2])

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            ConnectCommand(
                "",
                True,
                ConnectOptions("", self.ComPort),  # type:ignore
                InitializeCallback,
                (self, CallbackFunction, CallbackArgs),
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
            StopTemperatureControlCommand(
                "",
                True,
                StopTemperatureControlOptions("", self.HandleID),
                CallbackFunction,
                CallbackArgs,
            )
        )

        return ReturnCommandTracker

    def SetTemperature(
        self,
        Temperature: float,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            StartTemperatureControlCommand(
                "",
                True,
                StartTemperatureControlOptions("", self.HandleID, Temperature),
                CallbackFunction,
                CallbackArgs,
            )
        )

        return ReturnCommandTracker

    def UpdateCurrentTemperature(
        self,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            GetTemperatureCommand(
                "",
                True,
                GetTemperatureOptions("", self.HandleID),
                UpdateCurrentTemperatureCallback,
                (self, CallbackFunction, CallbackArgs),
            )
        )

        return ReturnCommandTracker

    def StartShaking(
        self,
        RPM: float,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:

        raise Exception(
            "Shaking is not supported on this device. You did something wrong. Pleaes correct"
        )

    def StopShaking(
        self,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            NOPCommand(
                "HamiltonHeaterCooler StopShaking NOP",
                CallbackFunction,
                CallbackArgs,
            )
        )

        return ReturnCommandTracker

    def UpdateCurrentShakingSpeed(
        self,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            NOPCommand(
                "HamiltonHeaterCooler UpdateCurrentShakingSpeed NOP",
                CallbackFunction,
                CallbackArgs,
            )
        )

        return ReturnCommandTracker
