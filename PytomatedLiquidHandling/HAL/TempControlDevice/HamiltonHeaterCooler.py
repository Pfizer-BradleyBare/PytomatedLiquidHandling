from ...Driver.TemperatureControl import HeaterCooler as HeaterCoolerDriver
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
            Name,
            ComPort,
            False,
            TempLimitsInstance,
            LayoutItemTrackerInstance,
        )
        self.HandleID: str

    def Initialize(
        self,
    ):
        try:
            Command = HeaterCoolerDriver.Connect.Command(
                ConnectOptions(self.ComPort),  # type:ignore
                True,
            )

            Command.Execute()

            self.HandleID = Command.GetHandleID()
        except:
            ...

    def Deinitialize(
        self,
    ):
        try:
            HeaterCoolerDriver.StopTemperatureControl.Command(
                HeaterCoolerDriver.StopTemperatureControl.Options(self.HandleID),
                True,
            ).Execute()
        except:
            ...

    def SetTemperature(
        self,
        Temperature: float,
    ):
        try:
            HeaterCoolerDriver.StartTemperatureControl.Command(
                HeaterCoolerDriver.StartTemperatureControl.Options(
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
            Command = HeaterCoolerDriver.GetTemperature.Command(
                HeaterCoolerDriver.GetTemperature.Options(self.HandleID), True
            )

            Command.Execute()

            self.CurrentTemperature = Command.GetTemperature()
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
