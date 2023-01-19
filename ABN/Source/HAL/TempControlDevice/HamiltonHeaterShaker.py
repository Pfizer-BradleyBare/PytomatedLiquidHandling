from typing import Callable

from ...Driver.Handler.DriverHandler import DriverHandler
from ...Driver.TemperatureControl.HeaterShaker import (
    ConnectCommand,
    ConnectOptions,
    GetShakingSpeedCommand,
    GetShakingSpeedOptions,
    GetTemperatureCommand,
    GetTemperatureOptions,
    SetPlateLockCommand,
    SetPlateLockOptions,
    StartShakeControlCommand,
    StartShakeControlOptions,
    StartTemperatureControlCommand,
    StartTemperatureControlOptions,
    StopShakeControlCommand,
    StopShakeControlOptions,
    StopTemperatureControlCommand,
    StopTemperatureControlOptions,
)
from ...Driver.Tools import Command, CommandTracker
from ...Server.Globals.HandlerRegistry import GetDriverHandler
from ..Layout import LayoutItemGroupingTracker
from .BaseTempControlDevice import TempControlDevice, TempLimits
from .BaseTempControlDevice.Interface import (
    UpdateCurrentShakingSpeedCallback,
    UpdateCurrentTemperatureCallback,
)


class HamiltonHeaterShaker(TempControlDevice):
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
            True,
            TempLimitsInstance,
            LayoutItemGroupingTrackerInstance,
        )
        self.HandleID: int

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

            DriverHandlerInstance: DriverHandler = GetDriverHandler()  # type:ignore

            DriverHandlerInstance.ExecuteCommand(
                SetPlateLockCommand(
                    "",
                    SetPlateLockOptions("", self.HandleID, 1),
                )
            )

            DriverHandlerInstance.ExecuteCommand(
                SetPlateLockCommand(
                    "",
                    SetPlateLockOptions("", self.HandleID, 0),
                    None,
                    args[1],
                    args[2],
                )
            )

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            ConnectCommand(
                "",
                ConnectOptions("", self.ComPort),  # type:ignore
                None,
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
                StopTemperatureControlOptions("", self.HandleID),
            )
        )

        ReturnCommandTracker.ManualLoad(
            StopShakeControlCommand(
                "",
                StopShakeControlOptions("", self.HandleID),
            )
        )

        ReturnCommandTracker.ManualLoad(
            SetPlateLockCommand(
                "",
                SetPlateLockOptions("", self.HandleID, 0),
                None,
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
                StartTemperatureControlOptions("", self.HandleID, Temperature),
                None,
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
                GetTemperatureOptions("", self.HandleID),
                None,
                UpdateCurrentTemperatureCallback,
                (self, CallbackFunction, CallbackArgs),
            )
        )

        return ReturnCommandTracker

    def StartShaking(
        self,
        RPM: int,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            SetPlateLockCommand(
                "",
                SetPlateLockOptions("", self.HandleID, 1),
            )
        )

        ReturnCommandTracker.ManualLoad(
            StartShakeControlCommand(
                "",
                StartShakeControlOptions("", self.HandleID, RPM),
                None,
                CallbackFunction,
                CallbackArgs,
            )
        )

        return ReturnCommandTracker

    def StopShaking(
        self,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            StopShakeControlCommand(
                "",
                StopShakeControlOptions("", self.HandleID),
            )
        )

        ReturnCommandTracker.ManualLoad(
            SetPlateLockCommand(
                "",
                SetPlateLockOptions("", self.HandleID, 0),
                None,
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
            GetShakingSpeedCommand(
                "",
                GetShakingSpeedOptions("", self.HandleID),
                None,
                UpdateCurrentShakingSpeedCallback,
                (self, CallbackFunction, CallbackArgs),
            )
        )

        return ReturnCommandTracker
