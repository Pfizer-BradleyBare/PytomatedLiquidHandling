from ...Driver.Hamilton.TemperatureControl import HeaterCooler as HeaterCoolerDriver
from ..LayoutItem import LayoutItemTracker
from .BaseTempControlDevice import TempControlDevice, TempLimits
from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC


class HamiltonHeaterCooler(TempControlDevice):
    def __init__(
        self,
        UniqueIdentifier: str,
        BackendInstance: HamiltonBackendABC,
        CustomErrorHandling: bool,
        ComPort: str,
        TempLimitsInstance: TempLimits,
        LayoutItemTrackerInstance: LayoutItemTracker,
    ):
        TempControlDevice.__init__(
            self,
            UniqueIdentifier,
            BackendInstance,
            CustomErrorHandling,
            ComPort,
            False,
            TempLimitsInstance,
            LayoutItemTrackerInstance,
        )

    def Initialize(self):
        if not isinstance(self.ComPort, str):
            raise Exception("Should never happen")

        try:
            CommandInstance = HeaterCoolerDriver.Connect.Command(
                OptionsInstance=HeaterCoolerDriver.Connect.Options(
                    ComPort=self.ComPort,
                ),
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.GetBackend().GetResponse(
                CommandInstance, CommandInstance.Response
            )

            self.HandleID = ResponseInstance.GetHandleID()
        except:
            ...

    def Deinitialize(self):
        try:
            CommandInstance = HeaterCoolerDriver.StopTemperatureControl.Command(
                OptionsInstance=HeaterCoolerDriver.StopTemperatureControl.Options(
                    HandleID=str(self.HandleID)
                ),
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.GetBackend().GetResponse(
                CommandInstance, CommandInstance.Response
            )
        except:
            ...

    def SetTemperature(
        self,
        *,
        Temperature: float,
    ):
        try:
            CommandInstance = HeaterCoolerDriver.StartTemperatureControl.Command(
                OptionsInstance=HeaterCoolerDriver.StartTemperatureControl.Options(
                    HandleID=str(self.HandleID),
                    Temperature=Temperature,
                ),
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.GetBackend().GetResponse(
                CommandInstance, CommandInstance.Response
            )
        except:
            ...

    def UpdateCurrentTemperature(
        self,
    ):
        try:
            CommandInstance = HeaterCoolerDriver.GetTemperature.Command(
                OptionsInstance=HeaterCoolerDriver.GetTemperature.Options(
                    HandleID=str(self.HandleID),
                ),
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.GetBackend().GetResponse(
                CommandInstance, CommandInstance.Response
            )

            self.CurrentTemperature = ResponseInstance.GetTemperature()
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
