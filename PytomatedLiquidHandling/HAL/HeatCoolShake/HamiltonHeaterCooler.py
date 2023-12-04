from typing import Literal

from pydantic import PrivateAttr

from PytomatedLiquidHandling.Driver.Hamilton import Backend
from PytomatedLiquidHandling.Driver.Hamilton import (
    HamiltonHeaterCooler as HeaterCoolerDriver,
)

from .Base import Exceptions, HeatCoolShakeABC


class HamiltonHeaterCooler(HeatCoolShakeABC):
    Backend: Backend.HamiltonBackendABC
    CustomErrorHandling: Literal["N/A"] = "N/A"

    _HeatingSupported: bool = PrivateAttr(default=True)
    _CoolingSupported: bool = PrivateAttr(default=True)
    _ShakingSupported: bool = PrivateAttr(default=False)
    _HandleID: str = PrivateAttr()

    def Initialize(self):
        HeatCoolShakeABC.Initialize(self)

        if not isinstance(self.ComPort, str):
            raise Exception("Should never happen")

        CommandInstance = HeaterCoolerDriver.Connect.Command(
            Options=HeaterCoolerDriver.Connect.Options(
                ComPort=self.ComPort,
            )
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.Backend.GetResponse(
            CommandInstance, HeaterCoolerDriver.Connect.Response
        )

        self._HandleID = ResponseInstance.HandleID

    def Deinitialize(self):
        HeatCoolShakeABC.Deinitialize(self)

        CommandInstance = HeaterCoolerDriver.StopTemperatureControl.Command(
            Options=HeaterCoolerDriver.StopTemperatureControl.Options(
                HandleID=str(self._HandleID)
            )
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.Backend.GetResponse(
            CommandInstance, HeaterCoolerDriver.StopTemperatureControl.Response
        )

    def SetTemperature(self, Temperature: float):
        CommandInstance = HeaterCoolerDriver.SetTemperature.Command(
            Options=HeaterCoolerDriver.SetTemperature.Options(
                HandleID=str(self._HandleID),
                Temperature=Temperature,
            )
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.Backend.GetResponse(
            CommandInstance, HeaterCoolerDriver.SetTemperature.Response
        )

    def TimeToTemperature(self, Temperature: float) -> float:
        return 0

    def GetTemperature(
        self,
    ) -> float:
        CommandInstance = HeaterCoolerDriver.GetTemperature.Command(
            Options=HeaterCoolerDriver.GetTemperature.Options(
                HandleID=str(self._HandleID),
            ),
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.Backend.GetResponse(
            CommandInstance, HeaterCoolerDriver.GetTemperature.Response
        )

        return ResponseInstance.Temperature

    def SetShakingSpeed(self, RPM: int):
        raise Exceptions.ShakingNotSupportedError

    def GetShakingSpeed(self) -> int:
        raise Exceptions.ShakingNotSupportedError
