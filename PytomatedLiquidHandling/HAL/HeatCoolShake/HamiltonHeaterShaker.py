from typing import Literal

from pydantic import PrivateAttr

from PytomatedLiquidHandling.Driver.Hamilton import Backend
from PytomatedLiquidHandling.Driver.Hamilton import (
    HSLHamHeaterShakerLib as HeaterShakerDriver,
)

from .Base import Exceptions, HeatCoolShakeABC


class HamiltonHeaterShaker(HeatCoolShakeABC):
    Backend: Backend.HamiltonBackendABC
    CustomErrorHandling: Literal["N/A"] = "N/A"

    _HeatingSupported: bool = PrivateAttr(default=True)
    _CoolingSupported: bool = PrivateAttr(default=False)
    _ShakingSupported: bool = PrivateAttr(default=True)
    _HandleID: int = PrivateAttr()

    def Initialize(self):
        HeatCoolShakeABC.Initialize(self)

        if not isinstance(self.ComPort, int):
            raise Exception("Should never happen")

        CommandInstance = HeaterShakerDriver.CreateUSBDevice.Command(
            Options=HeaterShakerDriver.CreateUSBDevice.Options(
                ComPort=self.ComPort,
            )
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.Backend.GetResponse(
            CommandInstance, HeaterShakerDriver.CreateUSBDevice.Response
        )

        self._HandleID = ResponseInstance.HandleID

        CommandInstance = HeaterShakerDriver.SetPlateLock.Command(
            Options=HeaterShakerDriver.SetPlateLock.Options(
                HandleID=int(self._HandleID),
                PlateLockState=1,
            )
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.Backend.GetResponse(
            CommandInstance, HeaterShakerDriver.SetPlateLock.Response
        )

        CommandInstance = HeaterShakerDriver.SetPlateLock.Command(
            Options=HeaterShakerDriver.SetPlateLock.Options(
                HandleID=int(self._HandleID),
                PlateLockState=0,
            )
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.Backend.GetResponse(
            CommandInstance, HeaterShakerDriver.SetPlateLock.Response
        )

    def Deinitialize(self):
        CommandInstance = HeaterShakerDriver.StopTempCtrl.Command(
            Options=HeaterShakerDriver.StopTempCtrl.Options(
                HandleID=int(self._HandleID),
            )
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.Backend.GetResponse(
            CommandInstance, HeaterShakerDriver.StopTempCtrl.Response
        )

        CommandInstance = HeaterShakerDriver.StopShaker.Command(
            Options=HeaterShakerDriver.StopShaker.Options(HandleID=int(self._HandleID))
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.Backend.GetResponse(
            CommandInstance, HeaterShakerDriver.StopShaker.Response
        )

        CommandInstance = HeaterShakerDriver.SetPlateLock.Command(
            Options=HeaterShakerDriver.SetPlateLock.Options(
                HandleID=int(self._HandleID),
                PlateLockState=0,
            )
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.Backend.GetResponse(
            CommandInstance, HeaterShakerDriver.SetPlateLock.Response
        )

        HeatCoolShakeABC.Deinitialize(self)

    def SetTemperature(self, Temperature: float):
        if Temperature < 25:
            raise Exceptions.CoolingNotSupportedError

        CommandInstance = HeaterShakerDriver.StartTempCtrl.Command(
            Options=HeaterShakerDriver.StartTempCtrl.Options(
                HandleID=int(self._HandleID),
                Temperature=Temperature,
            )
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.Backend.GetResponse(
            CommandInstance, HeaterShakerDriver.StartTempCtrl.Response
        )

    def TimeToTemperature(self, Temperature: float) -> float:
        return 0

    def GetTemperature(self) -> float:
        CommandInstance = HeaterShakerDriver.GetTemperature.Command(
            Options=HeaterShakerDriver.GetTemperature.Options(
                HandleID=int(self._HandleID),
            ),
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.Backend.GetResponse(
            CommandInstance, HeaterShakerDriver.GetTemperature.Response
        )

        return ResponseInstance.Temperature

    def SetShakingSpeed(self, RPM: int):
        if RPM == 0:
            CommandInstance = HeaterShakerDriver.StopShaker.Command(
                Options=HeaterShakerDriver.StopShaker.Options(
                    HandleID=int(self._HandleID),
                )
            )
            self.Backend.ExecuteCommand(CommandInstance)
            self.Backend.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.Backend.GetResponse(
                CommandInstance, HeaterShakerDriver.StopShaker.Response
            )

            CommandInstance = HeaterShakerDriver.SetPlateLock.Command(
                Options=HeaterShakerDriver.SetPlateLock.Options(
                    HandleID=int(self._HandleID), PlateLockState=0
                )
            )
            self.Backend.ExecuteCommand(CommandInstance)
            self.Backend.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.Backend.GetResponse(
                CommandInstance, HeaterShakerDriver.SetPlateLock.Response
            )

        else:
            CommandInstance = HeaterShakerDriver.SetPlateLock.Command(
                Options=HeaterShakerDriver.SetPlateLock.Options(
                    HandleID=int(self._HandleID),
                    PlateLockState=1,
                )
            )
            self.Backend.ExecuteCommand(CommandInstance)
            self.Backend.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.Backend.GetResponse(
                CommandInstance, HeaterShakerDriver.SetPlateLock.Response
            )

            CommandInstance = HeaterShakerDriver.StartShaker.Command(
                Options=HeaterShakerDriver.StartShaker.Options(
                    HandleID=int(self._HandleID),
                    ShakingSpeed=RPM,
                )
            )
            self.Backend.ExecuteCommand(CommandInstance)
            self.Backend.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.Backend.GetResponse(
                CommandInstance, HeaterShakerDriver.StartShaker.Response
            )

    def GetShakingSpeed(self) -> int:
        CommandInstance = HeaterShakerDriver.GetShakerSpeed.Command(
            Options=HeaterShakerDriver.GetShakerSpeed.Options(
                HandleID=int(self._HandleID),
            )
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.Backend.GetResponse(
            CommandInstance, HeaterShakerDriver.GetShakerSpeed.Response
        )

        return ResponseInstance.ShakerSpeed
