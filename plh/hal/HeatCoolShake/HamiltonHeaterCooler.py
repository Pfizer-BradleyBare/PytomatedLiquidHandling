from dataclasses import field
from typing import Literal

from pydantic import dataclasses

from PytomatedLiquidHandling.Driver.Hamilton import Backend
from PytomatedLiquidHandling.Driver.Hamilton import (
    HamiltonHeaterCooler as HeaterCoolerDriver,
)
from PytomatedLiquidHandling.HAL import LayoutItem

from .Base import HeatCoolShakeABC
from .Base.Exceptions import ShakingNotSupportedError


@dataclasses.dataclass(kw_only=True)
class HamiltonHeaterCooler(HeatCoolShakeABC):
    Backend: Backend.HamiltonBackendABC
    BackendErrorHandling: Literal["N/A"] = "N/A"

    _HandleID: str = field(init=False)

    def AssertOptions(
        self,
        LayoutItem: LayoutItem.CoverablePlate | LayoutItem.Plate,
        Temperature: float | None = None,
        RPM: int | None = None,
    ):
        Exceptions = list()

        try:
            super().AssertOptions(LayoutItem, Temperature, RPM)
        except ExceptionGroup as e:
            Exceptions += e.exceptions

        if RPM is not None:
            Exceptions.append(ShakingNotSupportedError)

        if len(Exceptions) > 0:
            raise ExceptionGroup("HeatCoolShakeDevice Options Exceptions", Exceptions)

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
        raise ShakingNotSupportedError

    def GetShakingSpeed(self) -> int:
        raise ShakingNotSupportedError
