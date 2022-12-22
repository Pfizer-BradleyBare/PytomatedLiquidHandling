from typing import Callable

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
from ..Layout import LayoutItemGroupingTracker
from .BaseTempControlDevice import TempControlDevice, TempLimits
from .BaseTempControlDevice.Interface import (
    InitializeCallback,
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

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            ConnectCommand(
                "",
                True,
                ConnectOptions("", self.ComPort),  # type:ignore
                InitializeCallback,
                (self,),
            )
        )

        ReturnCommandTracker.ManualLoad(
            SetPlateLockCommand(
                "",
                True,
                SetPlateLockOptions("", self.HandleID, 1),
            )
        )

        ReturnCommandTracker.ManualLoad(
            SetPlateLockCommand(
                "",
                True,
                SetPlateLockOptions("", self.HandleID, 0),
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
            StopTemperatureControlCommand(
                "",
                True,
                StopTemperatureControlOptions("", self.HandleID),
            )
        )

        ReturnCommandTracker.ManualLoad(
            StopShakeControlCommand(
                "",
                True,
                StopShakeControlOptions("", self.HandleID),
            )
        )

        ReturnCommandTracker.ManualLoad(
            SetPlateLockCommand(
                "",
                True,
                SetPlateLockOptions("", self.HandleID, 0),
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
        RPM: int,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:

        ReturnCommandTracker = CommandTracker()

        ReturnCommandTracker.ManualLoad(
            SetPlateLockCommand(
                "",
                True,
                SetPlateLockOptions("", self.HandleID, 1),
            )
        )

        ReturnCommandTracker.ManualLoad(
            StartShakeControlCommand(
                "",
                True,
                StartShakeControlOptions("", self.HandleID, RPM),
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
                True,
                StopShakeControlOptions("", self.HandleID),
            )
        )

        ReturnCommandTracker.ManualLoad(
            SetPlateLockCommand(
                "",
                True,
                SetPlateLockOptions("", self.HandleID, 0),
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
                True,
                GetShakingSpeedOptions("", self.HandleID),
                UpdateCurrentShakingSpeedCallback,
                (self, CallbackFunction, CallbackArgs),
            )
        )

        return ReturnCommandTracker
