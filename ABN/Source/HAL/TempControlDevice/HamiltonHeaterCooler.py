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
from ..Layout import LayoutItemGroupingTracker
from .BaseTempControlDevice import TempControlDevice, TempLimits


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
    ):

        try:
            Command = ConnectCommand(
                "",
                ConnectOptions("", self.ComPort),  # type:ignore
                True,
            )

            Command.Execute()

            self.HandleID = Command.GetResponse().GetAdditional()["HandleID"]
        except:
            ...

    def Deinitialize(
        self,
    ):

        try:
            StopTemperatureControlCommand(
                "", StopTemperatureControlOptions("", self.HandleID), True
            ).Execute()
        except:
            ...

    def SetTemperature(
        self,
        Temperature: float,
    ):

        try:
            StartTemperatureControlCommand(
                "", StartTemperatureControlOptions("", self.HandleID, Temperature), True
            ).Execute()
        except:
            ...

    def UpdateCurrentTemperature(
        self,
    ):

        try:
            Command = GetTemperatureCommand(
                "", GetTemperatureOptions("", self.HandleID), True
            )

            Command.Execute()

            self.CurrentTemperature = Command.GetResponse().GetAdditional()[
                "Temperature"
            ]
        except:
            ...

    def StartShaking(
        self,
        RPM: float,
    ):

        raise Exception(
            "Shaking is not supported on this device. You did something wrong. Pleaes correct"
        )

    def StopShaking(
        self,
    ):
        ...

    def UpdateCurrentShakingSpeed(
        self,
    ):
        ...
