from ...Driver.Hamilton.TemperatureControl import HeaterShaker as HeaterShakerDriver
from ..LayoutItem import LayoutItemTracker
from .BaseTempControlDevice import TempControlDevice, TempLimits


class HamiltonHeaterShaker(TempControlDevice):
    def __init__(
        self,
        UniqueIdentifier: str,
        CustomErrorHandling: bool,
        ComPort: str,
        TempLimitsInstance: TempLimits,
        LayoutItemTrackerInstance: LayoutItemTracker,
    ):
        TempControlDevice.__init__(
            self,
            UniqueIdentifier,
            CustomErrorHandling,
            ComPort,
            True,
            TempLimitsInstance,
            LayoutItemTrackerInstance,
        )
        self.HandleID: int

    def Initialize(self):
        if not isinstance(self.ComPort, int):
            raise Exception("Should never happen")

        try:
            Command = HeaterShakerDriver.Connect.Command(
                OptionsInstance=HeaterShakerDriver.Connect.Options(
                    ComPort=self.ComPort,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )

            Command.Execute()

            self.HandleID = Command.GetHandleID()
        except:
            ...

        try:
            HeaterShakerDriver.SetPlateLock.Command(
                OptionsInstance=HeaterShakerDriver.SetPlateLock.Options(
                    HandleID=self.HandleID,
                    PlateLockState=1,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            ).Execute()
        except:
            ...

        try:
            HeaterShakerDriver.SetPlateLock.Command(
                OptionsInstance=HeaterShakerDriver.SetPlateLock.Options(
                    HandleID=self.HandleID,
                    PlateLockState=0,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            ).Execute()
        except:
            ...

    def Deinitialize(self):
        try:
            HeaterShakerDriver.StopTemperatureControl.Command(
                OptionsInstance=HeaterShakerDriver.StopTemperatureControl.Options(
                    HandleID=self.HandleID,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            ).Execute()
        except:
            ...

        try:
            HeaterShakerDriver.StopShakeControl.Command(
                OptionsInstance=HeaterShakerDriver.StopShakeControl.Options(
                    HandleID=self.HandleID
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            ).Execute()
        except:
            ...

        try:
            HeaterShakerDriver.SetPlateLock.Command(
                OptionsInstance=HeaterShakerDriver.SetPlateLock.Options(
                    HandleID=self.HandleID,
                    PlateLockState=0,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            ).Execute()
        except:
            ...

    def SetTemperature(self, *, Temperature: float):
        try:
            HeaterShakerDriver.StartTemperatureControl.Command(
                OptionsInstance=HeaterShakerDriver.StartTemperatureControl.Options(
                    HandleID=self.HandleID,
                    Temperature=Temperature,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            ).Execute()
        except:
            ...

    def UpdateCurrentTemperature(self):
        try:
            Command = HeaterShakerDriver.GetTemperature.Command(
                OptionsInstance=HeaterShakerDriver.GetTemperature.Options(
                    HandleID=self.HandleID,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )

            Command.Execute()

            self.CurrentTemperature = Command.GetTemperature()
        except:
            ...

    def StartShaking(self, *, RPM: int):
        try:
            HeaterShakerDriver.SetPlateLock.Command(
                OptionsInstance=HeaterShakerDriver.SetPlateLock.Options(
                    HandleID=self.HandleID,
                    PlateLockState=1,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            ).Execute()
        except:
            ...

        try:
            HeaterShakerDriver.StartShakeControl.Command(
                OptionsInstance=HeaterShakerDriver.StartShakeControl.Options(
                    HandleID=self.HandleID,
                    ShakingSpeed=RPM,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            ).Execute()
        except:
            ...

    def StopShaking(self):
        try:
            HeaterShakerDriver.StopShakeControl.Command(
                OptionsInstance=HeaterShakerDriver.StopShakeControl.Options(
                    HandleID=self.HandleID,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            ).Execute()
        except:
            ...

        try:
            HeaterShakerDriver.SetPlateLock.Command(
                OptionsInstance=HeaterShakerDriver.SetPlateLock.Options(
                    HandleID=self.HandleID, PlateLockState=0
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            ).Execute()
        except:
            ...

    def UpdateCurrentShakingSpeed(self):
        try:
            Command = HeaterShakerDriver.GetShakingSpeed.Command(
                OptionsInstance=HeaterShakerDriver.GetShakingSpeed.Options(
                    HandleID=self.HandleID,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )

            Command.Execute()

            self.CurrentShakingSpeed = Command.GetShakingSpeed()
        except:
            ...
