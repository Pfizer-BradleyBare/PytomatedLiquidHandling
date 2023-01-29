from ...Driver.TemperatureControl import HeaterShaker as HeaterShakerDriver
from ..Layout import LayoutItemGroupingTracker
from .BaseTempControlDevice import TempControlDevice, TempLimits


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
    ):

        try:
            Command = HeaterShakerDriver.ConnectCommand(
                "",
                ConnectOptions("", self.ComPort),  # type:ignore
                True,
            )

            Command.Execute()

            self.HandleID = Command.GetResponse().GetAdditional()["HandleID"]
        except:
            ...

        try:
            HeaterShakerDriver.SetPlateLockCommand(
                "", HeaterShakerDriver.SetPlateLockOptions("", self.HandleID, 1), True
            ).Execute()
        except:
            ...

        try:
            HeaterShakerDriver.SetPlateLockCommand(
                "", HeaterShakerDriver.SetPlateLockOptions("", self.HandleID, 0), True
            ).Execute()
        except:
            ...

    def Deinitialize(
        self,
    ):

        try:
            HeaterShakerDriver.StopTemperatureControlCommand(
                "",
                HeaterShakerDriver.StopTemperatureControlOptions("", self.HandleID),
                True,
            ).Execute()
        except:
            ...

        try:
            HeaterShakerDriver.StopShakeControlCommand(
                "", HeaterShakerDriver.StopShakeControlOptions("", self.HandleID), True
            ).Execute()
        except:
            ...

        try:
            HeaterShakerDriver.SetPlateLockCommand(
                "", HeaterShakerDriver.SetPlateLockOptions("", self.HandleID, 0), True
            ).Execute()
        except:
            ...

    def SetTemperature(
        self,
        Temperature: float,
    ):

        try:
            HeaterShakerDriver.StartTemperatureControlCommand(
                "",
                HeaterShakerDriver.StartTemperatureControlOptions(
                    "", self.HandleID, Temperature
                ),
                True,
            ).Execute()
        except:
            ...

    def UpdateCurrentTemperature(
        self,
    ):
        try:
            Command = HeaterShakerDriver.GetTemperatureCommand(
                "", HeaterShakerDriver.GetTemperatureOptions("", self.HandleID), True
            )

            Command.Execute()

            self.CurrentTemperature = Command.GetResponse().GetAdditional()[
                "Temperature"
            ]
        except:
            ...

    def StartShaking(
        self,
        RPM: int,
    ):

        try:
            HeaterShakerDriver.SetPlateLockCommand(
                "", HeaterShakerDriver.SetPlateLockOptions("", self.HandleID, 1), True
            ).Execute()
        except:
            ...

        try:
            HeaterShakerDriver.StartShakeControlCommand(
                "",
                HeaterShakerDriver.StartShakeControlOptions("", self.HandleID, RPM),
                True,
            ).Execute()
        except:
            ...

    def StopShaking(
        self,
    ):

        try:
            HeaterShakerDriver.StopShakeControlCommand(
                "", HeaterShakerDriver.StopShakeControlOptions("", self.HandleID), True
            ).Execute()
        except:
            ...

        try:
            HeaterShakerDriver.SetPlateLockCommand(
                "", HeaterShakerDriver.SetPlateLockOptions("", self.HandleID, 0), True
            ).Execute()
        except:
            ...

    def UpdateCurrentShakingSpeed(
        self,
    ):

        try:
            Command = HeaterShakerDriver.GetShakingSpeedCommand(
                "", HeaterShakerDriver.GetShakingSpeedOptions("", self.HandleID), True
            )

            Command.Execute()

            self.CurrentShakingSpeed = Command.GetResponse().GetAdditional()[
                "ShakingSpeed"
            ]
        except:
            ...
