from ...Driver.Hamilton.TemperatureControl import HeaterCooler as HeaterCoolerDriver
from .BaseTempControlDevice import TempControlDevice
from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from dataclasses import dataclass, field


@dataclass
class HamiltonHeaterCooler(TempControlDevice):
    BackendInstance: HamiltonBackendABC
    ShakingSupported: bool = field(init=False, default=False)
    HandleID: str = field(init=False)

    def Initialize(self):
        if not isinstance(self.ComPort, str):
            raise Exception("Should never happen")

        CommandInstance = HeaterCoolerDriver.Connect.Command(
            OptionsInstance=HeaterCoolerDriver.Connect.Options(
                ComPort=self.ComPort,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.BackendInstance.GetResponse(
            CommandInstance, HeaterCoolerDriver.Connect.Response
        )

        self.HandleID = ResponseInstance.GetHandleID()

    def Deinitialize(self):
        CommandInstance = HeaterCoolerDriver.StopTemperatureControl.Command(
            OptionsInstance=HeaterCoolerDriver.StopTemperatureControl.Options(
                HandleID=str(self.HandleID)
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.BackendInstance.GetResponse(
            CommandInstance, HeaterCoolerDriver.StopTemperatureControl.Response
        )

    def SetTemperature(
        self,
        *,
        Temperature: float,
    ):
        CommandInstance = HeaterCoolerDriver.StartTemperatureControl.Command(
            OptionsInstance=HeaterCoolerDriver.StartTemperatureControl.Options(
                HandleID=str(self.HandleID),
                Temperature=Temperature,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.BackendInstance.GetResponse(
            CommandInstance, HeaterCoolerDriver.StartTemperatureControl.Response
        )

    def UpdateTemperature(
        self,
    ):
        CommandInstance = HeaterCoolerDriver.GetTemperature.Command(
            OptionsInstance=HeaterCoolerDriver.GetTemperature.Options(
                HandleID=str(self.HandleID),
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.BackendInstance.GetResponse(
            CommandInstance, HeaterCoolerDriver.GetTemperature.Response
        )

        self.CurrentTemperature = ResponseInstance.GetTemperature()

    def StartShaking(self, *, RPM: float):
        raise Exception(
            "Shaking is not supported on this device. You did something wrong. Pleaes correct"
        )

    def StopShaking(self):
        ...

    def UpdateShakingSpeed(self):
        ...
