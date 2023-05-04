from ...Driver.Hamilton.TemperatureControl import HeaterShaker as HeaterShakerDriver
from ..LayoutItem import LayoutItemTracker
from .BaseTempControlDevice import TempControlDevice, TempLimits


class HamiltonHeaterShaker(TempControlDevice):
    def __init__(
        self,
        UniqueIdentifier: str,
        ComPort: str,
        TempLimitsInstance: TempLimits,
        LayoutItemTrackerInstance: LayoutItemTracker,
    ):
        TempControlDevice.__init__(
            self,
            UniqueIdentifier,
            ComPort,
            True,
            TempLimitsInstance,
            LayoutItemTrackerInstance,
        )
        self.HandleID: int

    def Initialize(
        self,
        *,
        ConnectAdvancedOptionsInstance: HeaterShakerDriver.Connect.AdvancedOptions = HeaterShakerDriver.Connect.AdvancedOptions(),
        SetPlateLockAdvancedOptionsInstance: HeaterShakerDriver.SetPlateLock.AdvancedOptions = HeaterShakerDriver.SetPlateLock.AdvancedOptions()
    ):
        if not isinstance(self.ComPort, int):
            raise Exception("Should never happen")

        try:
            Command = HeaterShakerDriver.Connect.Command(
                HeaterShakerDriver.Connect.Options(
                    ComPort=self.ComPort,
                    AdvancedOptionsInstance=HeaterShakerDriver.Connect.AdvancedOptions().UpdateOptions(
                        ConnectAdvancedOptionsInstance
                    ),
                ),
            )

            Command.Execute()

            self.HandleID = Command.GetHandleID()
        except:
            ...

        try:
            HeaterShakerDriver.SetPlateLock.Command(
                HeaterShakerDriver.SetPlateLock.Options(
                    HandleID=self.HandleID,
                    PlateLockState=1,
                    AdvancedOptionsInstance=HeaterShakerDriver.SetPlateLock.AdvancedOptions().UpdateOptions(
                        SetPlateLockAdvancedOptionsInstance
                    ),
                ),
            ).Execute()
        except:
            ...

        try:
            HeaterShakerDriver.SetPlateLock.Command(
                HeaterShakerDriver.SetPlateLock.Options(
                    HandleID=self.HandleID,
                    PlateLockState=0,
                    AdvancedOptionsInstance=HeaterShakerDriver.SetPlateLock.AdvancedOptions().UpdateOptions(
                        SetPlateLockAdvancedOptionsInstance
                    ),
                )
            ).Execute()
        except:
            ...

    def Deinitialize(
        self,
        *,
        StopTempControlAdvancedOptionsInstance: HeaterShakerDriver.StopTemperatureControl.AdvancedOptions = HeaterShakerDriver.StopTemperatureControl.AdvancedOptions(),
        StopShakeControlAdvancedOptionsInstance: HeaterShakerDriver.StopShakeControl.AdvancedOptions = HeaterShakerDriver.StopShakeControl.AdvancedOptions(),
        SetPlateLockAdvancedOptionsInstance: HeaterShakerDriver.SetPlateLock.AdvancedOptions = HeaterShakerDriver.SetPlateLock.AdvancedOptions()
    ):
        try:
            HeaterShakerDriver.StopTemperatureControl.Command(
                HeaterShakerDriver.StopTemperatureControl.Options(
                    HandleID=self.HandleID,
                    AdvancedOptionsInstance=HeaterShakerDriver.StopTemperatureControl.AdvancedOptions().UpdateOptions(
                        StopTempControlAdvancedOptionsInstance
                    ),
                ),
            ).Execute()
        except:
            ...

        try:
            HeaterShakerDriver.StopShakeControl.Command(
                HeaterShakerDriver.StopShakeControl.Options(
                    HandleID=self.HandleID,
                    AdvancedOptionsInstance=HeaterShakerDriver.StopShakeControl.AdvancedOptions().UpdateOptions(
                        StopShakeControlAdvancedOptionsInstance
                    ),
                )
            ).Execute()
        except:
            ...

        try:
            HeaterShakerDriver.SetPlateLock.Command(
                HeaterShakerDriver.SetPlateLock.Options(
                    HandleID=self.HandleID,
                    PlateLockState=0,
                    AdvancedOptionsInstance=HeaterShakerDriver.SetPlateLock.AdvancedOptions().UpdateOptions(
                        SetPlateLockAdvancedOptionsInstance
                    ),
                ),
            ).Execute()
        except:
            ...

    def SetTemperature(
        self,
        Temperature: float,
        *,
        AdvancedOptionsInstance: HeaterShakerDriver.StartTemperatureControl.AdvancedOptions = HeaterShakerDriver.StartTemperatureControl.AdvancedOptions()
    ):
        try:
            HeaterShakerDriver.StartTemperatureControl.Command(
                HeaterShakerDriver.StartTemperatureControl.Options(
                    HandleID=self.HandleID,
                    Temperature=Temperature,
                    AdvancedOptionsInstance=HeaterShakerDriver.StartTemperatureControl.AdvancedOptions().UpdateOptions(
                        AdvancedOptionsInstance
                    ),
                ),
            ).Execute()
        except:
            ...

    def UpdateCurrentTemperature(
        self,
        *,
        AdvancedOptionsInstance: HeaterShakerDriver.GetTemperature.AdvancedOptions = HeaterShakerDriver.GetTemperature.AdvancedOptions()
    ):
        try:
            Command = HeaterShakerDriver.GetTemperature.Command(
                HeaterShakerDriver.GetTemperature.Options(
                    HandleID=self.HandleID,
                    AdvancedOptionsInstance=HeaterShakerDriver.GetTemperature.AdvancedOptions().UpdateOptions(
                        AdvancedOptionsInstance
                    ),
                )
            )

            Command.Execute()

            self.CurrentTemperature = Command.GetTemperature()
        except:
            ...

    def StartShaking(
        self,
        RPM: int,
        *,
        StartShakeControlAdvancedOptionsInstance: HeaterShakerDriver.StartShakeControl.AdvancedOptions = HeaterShakerDriver.StartShakeControl.AdvancedOptions(),
        SetPlateLockAdvancedOptionsInstance: HeaterShakerDriver.SetPlateLock.AdvancedOptions = HeaterShakerDriver.SetPlateLock.AdvancedOptions()
    ):
        try:
            HeaterShakerDriver.SetPlateLock.Command(
                HeaterShakerDriver.SetPlateLock.Options(
                    HandleID=self.HandleID,
                    PlateLockState=1,
                    AdvancedOptionsInstance=HeaterShakerDriver.SetPlateLock.AdvancedOptions().UpdateOptions(
                        SetPlateLockAdvancedOptionsInstance
                    ),
                ),
            ).Execute()
        except:
            ...

        try:
            HeaterShakerDriver.StartShakeControl.Command(
                HeaterShakerDriver.StartShakeControl.Options(
                    HandleID=self.HandleID,
                    ShakingSpeed=RPM,
                    AdvancedOptionsInstance=HeaterShakerDriver.StartShakeControl.AdvancedOptions().UpdateOptions(
                        StartShakeControlAdvancedOptionsInstance
                    ),
                ),
            ).Execute()
        except:
            ...

    def StopShaking(
        self,
        *,
        StopShakeControlAdvancedOptionsInstance: HeaterShakerDriver.StopShakeControl.AdvancedOptions = HeaterShakerDriver.StopShakeControl.AdvancedOptions(),
        SetPlateLockAdvancedOptionsInstance: HeaterShakerDriver.SetPlateLock.AdvancedOptions = HeaterShakerDriver.SetPlateLock.AdvancedOptions()
    ):
        try:
            HeaterShakerDriver.StopShakeControl.Command(
                HeaterShakerDriver.StopShakeControl.Options(
                    HandleID=self.HandleID,
                    AdvancedOptionsInstance=HeaterShakerDriver.StopShakeControl.AdvancedOptions().UpdateOptions(
                        StopShakeControlAdvancedOptionsInstance
                    ),
                ),
            ).Execute()
        except:
            ...

        try:
            HeaterShakerDriver.SetPlateLock.Command(
                HeaterShakerDriver.SetPlateLock.Options(
                    HandleID=self.HandleID,
                    PlateLockState=0,
                    AdvancedOptionsInstance=HeaterShakerDriver.SetPlateLock.AdvancedOptions().UpdateOptions(
                        SetPlateLockAdvancedOptionsInstance
                    ),
                )
            ).Execute()
        except:
            ...

    def UpdateCurrentShakingSpeed(
        self,
        *,
        AdvancedOptionsInstance: HeaterShakerDriver.GetShakingSpeed.AdvancedOptions = HeaterShakerDriver.GetShakingSpeed.AdvancedOptions()
    ):
        try:
            Command = HeaterShakerDriver.GetShakingSpeed.Command(
                HeaterShakerDriver.GetShakingSpeed.Options(
                    HandleID=self.HandleID,
                    AdvancedOptionsInstance=HeaterShakerDriver.GetShakingSpeed.AdvancedOptions().UpdateOptions(
                        AdvancedOptionsInstance
                    ),
                ),
            )

            Command.Execute()

            self.CurrentShakingSpeed = Command.GetShakingSpeed()
        except:
            ...
