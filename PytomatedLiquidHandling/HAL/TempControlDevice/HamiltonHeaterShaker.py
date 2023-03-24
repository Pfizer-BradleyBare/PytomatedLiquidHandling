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
            Command = HeaterShakerDriver.Connect.Command(
                ConnectOptions(self.ComPort),  # type:ignore
                True,
            )

            Command.Execute()

            self.HandleID = Command.GetHandleID()
        except:
            ...

        try:
            HeaterShakerDriver.SetPlateLock.Command(
                HeaterShakerDriver.SetPlateLock.Options(self.HandleID, 1), True
            ).Execute()
        except:
            ...

        try:
            HeaterShakerDriver.SetPlateLock.Command(
                HeaterShakerDriver.SetPlateLock.Options(self.HandleID, 0), True
            ).Execute()
        except:
            ...

    def Deinitialize(
        self,
    ):

        try:
            HeaterShakerDriver.StopTemperatureControl.Command(
                HeaterShakerDriver.StopTemperatureControl.Options(self.HandleID),
                True,
            ).Execute()
        except:
            ...

        try:
            HeaterShakerDriver.StopShakeControl.Command(
                HeaterShakerDriver.StopShakeControl.Options(self.HandleID), True
            ).Execute()
        except:
            ...

        try:
            HeaterShakerDriver.SetPlateLock.Command(
                HeaterShakerDriver.SetPlateLock.Options(self.HandleID, 0), True
            ).Execute()
        except:
            ...

    def SetTemperature(
        self,
        Temperature: float,
    ):

        try:
            HeaterShakerDriver.StartTemperatureControl.Command(
                HeaterShakerDriver.StartTemperatureControl.Options(
                    self.HandleID, Temperature
                ),
                True,
            ).Execute()
        except:
            ...

    def UpdateCurrentTemperature(
        self,
    ):
        try:
            Command = HeaterShakerDriver.GetTemperature.Command(
                HeaterShakerDriver.GetTemperature.Options(self.HandleID), True
            )

            Command.Execute()

            self.CurrentTemperature = Command.GetTemperature()
        except:
            ...

    def StartShaking(
        self,
        RPM: int,
    ):

        try:
            HeaterShakerDriver.SetPlateLock.Command(
                HeaterShakerDriver.SetPlateLock.Options(self.HandleID, 1), True
            ).Execute()
        except:
            ...

        try:
            HeaterShakerDriver.StartShakeControl.Command(
                HeaterShakerDriver.StartShakeControl.Options(self.HandleID, RPM),
                True,
            ).Execute()
        except:
            ...

    def StopShaking(
        self,
    ):

        try:
            HeaterShakerDriver.StopShakeControl.Command(
                HeaterShakerDriver.StopShakeControl.Options(self.HandleID), True
            ).Execute()
        except:
            ...

        try:
            HeaterShakerDriver.SetPlateLock.Command(
                HeaterShakerDriver.SetPlateLock.Options(self.HandleID, 0), True
            ).Execute()
        except:
            ...

    def UpdateCurrentShakingSpeed(
        self,
    ):

        try:
            Command = HeaterShakerDriver.GetShakingSpeed.Command(
                HeaterShakerDriver.GetShakingSpeed.Options(self.HandleID), True
            )

            Command.Execute()

            self.CurrentShakingSpeed = Command.GetShakingSpeed()
        except:
            ...
