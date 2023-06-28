from dataclasses import dataclass, field

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.TemperatureControl import HeaterCooler as HeaterCoolerDriver
from .BaseTempControlDevice import TempControlDevice


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

    @TempControlDevice.Temperature.setter
    def Temperature(
        self,
        *,
        NewTemperature: float,
    ):
        CommandInstance = HeaterCoolerDriver.StartTemperatureControl.Command(
            OptionsInstance=HeaterCoolerDriver.StartTemperatureControl.Options(
                HandleID=str(self.HandleID),
                Temperature=NewTemperature,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.BackendInstance.GetResponse(
            CommandInstance, HeaterCoolerDriver.StartTemperatureControl.Response
        )

    def _UpdateActualTemperature(
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

        self._ActualTemperature = ResponseInstance.GetTemperature()

    @TempControlDevice.ShakingSpeed.setter
    def ShakingSpeed(self, NewRPM: int):
        raise Exception(
            "Shaking is not supported on this device. You did something wrong. Pleaes correct"
        )

    def _UpdateActualShakingSpeed(self):
        self._ActualShakingSpeed = 0
