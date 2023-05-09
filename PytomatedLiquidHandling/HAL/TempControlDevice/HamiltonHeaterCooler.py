from ...Driver.Hamilton.TemperatureControl import HeaterCooler as HeaterCoolerDriver
from ..LayoutItem import LayoutItemTracker
from .BaseTempControlDevice import TempControlDevice, TempLimits


class HamiltonHeaterCooler(TempControlDevice):
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
            False,
            TempLimitsInstance,
            LayoutItemTrackerInstance,
        )
        self.HandleID: str

    def Initialize(self):
        if not isinstance(self.ComPort, str):
            raise Exception("Should never happen")

        try:
            Command = HeaterCoolerDriver.Connect.Command(
                OptionsInstance=HeaterCoolerDriver.Connect.Options(
                    ComPort=self.ComPort,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )

            Command.Execute()

            self.HandleID = Command.GetHandleID()
        except:
            ...

    def Deinitialize(self):
        try:
            HeaterCoolerDriver.StopTemperatureControl.Command(
                OptionsInstance=HeaterCoolerDriver.StopTemperatureControl.Options(
                    HandleID=self.HandleID
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            ).Execute()
        except:
            ...

    def SetTemperature(
        self,
        *,
        Temperature: float,
    ):
        try:
            HeaterCoolerDriver.StartTemperatureControl.Command(
                OptionsInstance=HeaterCoolerDriver.StartTemperatureControl.Options(
                    HandleID=self.HandleID,
                    Temperature=Temperature,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            ).Execute()
        except:
            ...

    def UpdateCurrentTemperature(
        self,
    ):
        try:
            Command = HeaterCoolerDriver.GetTemperature.Command(
                OptionsInstance=HeaterCoolerDriver.GetTemperature.Options(
                    HandleID=self.HandleID,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )

            Command.Execute()

            self.CurrentTemperature = Command.GetTemperature()
        except:
            ...

    def StartShaking(self, *, RPM: float):
        raise Exception(
            "Shaking is not supported on this device. You did something wrong. Pleaes correct"
        )

    def StopShaking(self):
        ...

    def UpdateCurrentShakingSpeed(self):
        ...
