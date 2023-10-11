from dataclasses import dataclass, field

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.TemperatureControl import HeaterCooler as HeaterCoolerDriver
from .Base import HeatCoolShakeDeviceABC


@dataclass
class HamiltonHeaterCooler(HeatCoolShakeDeviceABC):
    BackendInstance: HamiltonBackendABC
    HeatingSupported: bool = field(init=False, default=True)
    CoolingSupported: bool = field(init=False, default=True)
    ShakingSupported: bool = field(init=False, default=False)
    HandleID: str = field(init=False)

    def Initialize(self):
        HeatCoolShakeDeviceABC.Initialize(self)

        if not isinstance(self.ComPort, str):
            raise Exception("Should never happen")

        CommandInstance = HeaterCoolerDriver.Connect.Command(
            Options=HeaterCoolerDriver.Connect.Options(
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
        HeatCoolShakeDeviceABC.Deinitialize(self)

        CommandInstance = HeaterCoolerDriver.StopTemperatureControl.Command(
            Options=HeaterCoolerDriver.StopTemperatureControl.Options(
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
        OptionsInstance: HeatCoolShakeDeviceABC.SetTemperatureOptions,
    ):
        CommandInstance = HeaterCoolerDriver.StartTemperatureControl.Command(
            Options=HeaterCoolerDriver.StartTemperatureControl.Options(
                HandleID=str(self.HandleID),
                Temperature=OptionsInstance.Temperature,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.BackendInstance.GetResponse(
            CommandInstance, HeaterCoolerDriver.StartTemperatureControl.Response
        )

    def SetTemperatureTime(
        self,
        OptionsInstance: HeatCoolShakeDeviceABC.SetTemperatureOptions,
    ) -> float:
        return 0

    def GetTemperature(
        self,
    ) -> float:
        CommandInstance = HeaterCoolerDriver.GetTemperature.Command(
            Options=HeaterCoolerDriver.GetTemperature.Options(
                HandleID=str(self.HandleID),
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.BackendInstance.GetResponse(
            CommandInstance, HeaterCoolerDriver.GetTemperature.Response
        )

        return ResponseInstance.GetTemperature()

    def GetTemperatureTime(self) -> float:
        return 0

    def SetShakingSpeed(
        self,
        OptionsInstance: HeatCoolShakeDeviceABC.SetShakingSpeedOptions,
    ):
        raise Exception(
            "Shaking is not supported on this device. You did something wrong. Pleaes correct"
        )

    def SetShakingSpeedTime(
        self,
        OptionsInstance: HeatCoolShakeDeviceABC.SetShakingSpeedOptions,
    ) -> float:
        raise Exception(
            "Shaking is not supported on this device. You did something wrong. Pleaes correct"
        )

    def GetShakingSpeed(self) -> int:
        raise Exception(
            "Shaking is not supported on this device. You did something wrong. Pleaes correct"
        )

    def GetShakingSpeedTime(self) -> float:
        raise Exception(
            "Shaking is not supported on this device. You did something wrong. Pleaes correct"
        )
