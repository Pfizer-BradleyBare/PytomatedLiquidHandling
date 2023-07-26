from dataclasses import dataclass, field

from PytomatedLiquidHandling.HAL.TempControlDevice.BaseTempControlDevice.TempControlDevice import (
    SetTemperatureInterfaceCommand,
)

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.TemperatureControl import HeaterCooler as HeaterCoolerDriver
from .BaseTempControlDevice import TempControlDevice


@dataclass
class HamiltonHeaterCooler(TempControlDevice):
    BackendInstance: HamiltonBackendABC
    HeatingSupported: bool = field(init=False, default=True)
    CoolingSupported: bool = field(init=False, default=True)
    ShakingSupported: bool = field(init=False, default=False)
    HandleID: str = field(init=False)

    def _Initialize(self):
        TempControlDevice._Initialize(self)

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

    def _InitializeTime(self) -> float:
        return 0

    def _Deinitialize(self):
        TempControlDevice._Deinitialize(self)

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

    def _DeinitializeTime(self) -> float:
        return 0

    def _SetTemperature(
        self, OptionsInstance: TempControlDevice.SetTemperature.Options
    ):
        CommandInstance = HeaterCoolerDriver.StartTemperatureControl.Command(
            OptionsInstance=HeaterCoolerDriver.StartTemperatureControl.Options(
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
        self, OptionsInstance: TempControlDevice.SetTemperature.Options
    ) -> float:
        return 0

    def _GetTemperature(
        self,
    ) -> float:
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

        return ResponseInstance.GetTemperature()

    def _GetTemperatureTime(self) -> float:
        return 0

    def _SetShakingSpeed(
        self, OptionsInstance: TempControlDevice.SetShakingSpeed.Options
    ):
        raise Exception(
            "Shaking is not supported on this device. You did something wrong. Pleaes correct"
        )

    def _SetShakingSpeedTime(
        self, OptionsInstance: TempControlDevice.SetShakingSpeed.Options
    ) -> float:
        raise Exception(
            "Shaking is not supported on this device. You did something wrong. Pleaes correct"
        )

    def _GetShakingSpeed(
        self, OptionsInstance: TempControlDevice.SetShakingSpeed.Options
    ) -> int:
        raise Exception(
            "Shaking is not supported on this device. You did something wrong. Pleaes correct"
        )

    def _GetShakingSpeedTime(
        self, OptionsInstance: TempControlDevice.SetShakingSpeed.Options
    ) -> float:
        raise Exception(
            "Shaking is not supported on this device. You did something wrong. Pleaes correct"
        )
