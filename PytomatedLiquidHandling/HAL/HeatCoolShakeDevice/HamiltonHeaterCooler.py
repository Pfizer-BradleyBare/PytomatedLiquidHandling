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

    def _Initialize(self):
        HeatCoolShakeDeviceABC._Initialize(self)

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

    def _InitializeTime(self) -> float:
        return 0

    def _Deinitialize(self):
        HeatCoolShakeDeviceABC._Deinitialize(self)

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

    def _DeinitializeTime(self) -> float:
        return 0

    def _SetTemperature(
        self,
        OptionsInstance: HeatCoolShakeDeviceABC.SetTemperatureInterfaceCommand.Options,
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

    def _SetTemperatureTime(
        self,
        OptionsInstance: HeatCoolShakeDeviceABC.SetTemperatureInterfaceCommand.Options,
    ) -> float:
        return 0

    def _GetTemperature(
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

    def _GetTemperatureTime(self) -> float:
        return 0

    def _SetShakingSpeed(
        self,
        OptionsInstance: HeatCoolShakeDeviceABC.SetShakingSpeedInterfaceCommand.Options,
    ):
        raise Exception(
            "Shaking is not supported on this device. You did something wrong. Pleaes correct"
        )

    def _SetShakingSpeedTime(
        self,
        OptionsInstance: HeatCoolShakeDeviceABC.SetShakingSpeedInterfaceCommand.Options,
    ) -> float:
        raise Exception(
            "Shaking is not supported on this device. You did something wrong. Pleaes correct"
        )

    def _GetShakingSpeed(self) -> int:
        raise Exception(
            "Shaking is not supported on this device. You did something wrong. Pleaes correct"
        )

    def _GetShakingSpeedTime(self) -> float:
        raise Exception(
            "Shaking is not supported on this device. You did something wrong. Pleaes correct"
        )
