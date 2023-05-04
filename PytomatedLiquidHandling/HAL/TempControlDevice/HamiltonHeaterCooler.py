from ...Driver.Hamilton.TemperatureControl import HeaterCooler as HeaterCoolerDriver
from ..LayoutItem import LayoutItemTracker
from .BaseTempControlDevice import TempControlDevice, TempLimits


class HamiltonHeaterCooler(TempControlDevice):
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
            False,
            TempLimitsInstance,
            LayoutItemTrackerInstance,
        )
        self.HandleID: str

    def Initialize(
        self,
        *,
        AdvancedOptionsInstance: HeaterCoolerDriver.Connect.AdvancedOptions = HeaterCoolerDriver.Connect.AdvancedOptions(),
    ):
        if not isinstance(self.ComPort, str):
            raise Exception("Should never happen")

        try:
            Command = HeaterCoolerDriver.Connect.Command(
                HeaterCoolerDriver.Connect.Options(
                    ComPort=self.ComPort,
                    AdvancedOptionsInstance=HeaterCoolerDriver.Connect.AdvancedOptions().UpdateOptions(
                        AdvancedOptionsInstance
                    ),
                ),
            )

            Command.Execute()

            self.HandleID = Command.GetHandleID()
        except:
            ...

    def Deinitialize(
        self,
        *,
        AdvancedOptionsInstance: HeaterCoolerDriver.StopTemperatureControl.AdvancedOptions = HeaterCoolerDriver.StopTemperatureControl.AdvancedOptions(),
    ):
        try:
            HeaterCoolerDriver.StopTemperatureControl.Command(
                HeaterCoolerDriver.StopTemperatureControl.Options(
                    HandleID=self.HandleID,
                    AdvancedOptionsInstance=HeaterCoolerDriver.StopTemperatureControl.AdvancedOptions().UpdateOptions(
                        AdvancedOptionsInstance
                    ),
                ),
            ).Execute()
        except:
            ...

    def SetTemperature(
        self,
        Temperature: float,
        *,
        AdvancedOptionsInstance: HeaterCoolerDriver.StartTemperatureControl.AdvancedOptions = HeaterCoolerDriver.StartTemperatureControl.AdvancedOptions(),
    ):
        try:
            HeaterCoolerDriver.StartTemperatureControl.Command(
                HeaterCoolerDriver.StartTemperatureControl.Options(
                    HandleID=self.HandleID,
                    Temperature=Temperature,
                    AdvancedOptionsInstance=HeaterCoolerDriver.StartTemperatureControl.AdvancedOptions().UpdateOptions(
                        AdvancedOptionsInstance
                    ),
                ),
            ).Execute()
        except:
            ...

    def UpdateCurrentTemperature(
        self,
        *,
        AdvancedOptionsInstance: HeaterCoolerDriver.GetTemperature.AdvancedOptions = HeaterCoolerDriver.GetTemperature.AdvancedOptions(),
    ):
        try:
            Command = HeaterCoolerDriver.GetTemperature.Command(
                HeaterCoolerDriver.GetTemperature.Options(
                    HandleID=self.HandleID,
                    AdvancedOptionsInstance=HeaterCoolerDriver.GetTemperature.AdvancedOptions().UpdateOptions(
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
        RPM: float,
        *,
        AdvancedOptionsInstance: HeaterCoolerDriver.StopTemperatureControl.AdvancedOptions = HeaterCoolerDriver.StopTemperatureControl.AdvancedOptions(),
    ):
        raise Exception(
            "Shaking is not supported on this device. You did something wrong. Pleaes correct"
        )

    def StopShaking(
        self,
        *,
        AdvancedOptionsInstance: HeaterCoolerDriver.StopTemperatureControl.AdvancedOptions = HeaterCoolerDriver.StopTemperatureControl.AdvancedOptions(),
    ):
        ...

    def UpdateCurrentShakingSpeed(
        self,
        *,
        AdvancedOptionsInstance: HeaterCoolerDriver.StopTemperatureControl.AdvancedOptions = HeaterCoolerDriver.StopTemperatureControl.AdvancedOptions(),
    ):
        ...
