from dataclasses import dataclass, field

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.TemperatureControl import HeaterShaker as HeaterShakerDriver
from .Base import CoolingNotSupportedError, HeatCoolShakeDeviceABC


@dataclass
class HamiltonHeaterShaker(HeatCoolShakeDeviceABC):
    Backend: HamiltonBackendABC
    HeatingSupported: bool = field(init=False, default=True)
    CoolingSupported: bool = field(init=False, default=False)
    ShakingSupported: bool = field(init=False, default=True)
    HandleID: int = field(init=False)

    def Initialize(self):
        HeatCoolShakeDeviceABC.Initialize(self)

        if not isinstance(self.ComPort, int):
            raise Exception("Should never happen")

        CommandInstance = HeaterShakerDriver.Connect.Command(
            Options=HeaterShakerDriver.Connect.Options(
                ComPort=self.ComPort,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.Backend.GetResponse(
            CommandInstance, HeaterShakerDriver.Connect.Response
        )

        self.HandleID = ResponseInstance.GetHandleID()

        CommandInstance = HeaterShakerDriver.SetPlateLock.Command(
            Options=HeaterShakerDriver.SetPlateLock.Options(
                HandleID=int(self.HandleID),
                PlateLockState=1,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.Backend.GetResponse(
            CommandInstance, HeaterShakerDriver.SetPlateLock.Response
        )

        CommandInstance = HeaterShakerDriver.SetPlateLock.Command(
            Options=HeaterShakerDriver.SetPlateLock.Options(
                HandleID=int(self.HandleID),
                PlateLockState=0,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.Backend.GetResponse(
            CommandInstance, HeaterShakerDriver.SetPlateLock.Response
        )

    def Deinitialize(self):
        CommandInstance = HeaterShakerDriver.StopTemperatureControl.Command(
            Options=HeaterShakerDriver.StopTemperatureControl.Options(
                HandleID=int(self.HandleID),
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.Backend.GetResponse(
            CommandInstance, HeaterShakerDriver.StopTemperatureControl.Response
        )

        CommandInstance = HeaterShakerDriver.StopShakeControl.Command(
            Options=HeaterShakerDriver.StopShakeControl.Options(
                HandleID=int(self.HandleID)
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.Backend.GetResponse(
            CommandInstance, HeaterShakerDriver.StopShakeControl.Response
        )

        CommandInstance = HeaterShakerDriver.SetPlateLock.Command(
            Options=HeaterShakerDriver.SetPlateLock.Options(
                HandleID=int(self.HandleID),
                PlateLockState=0,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.Backend.GetResponse(
            CommandInstance, HeaterShakerDriver.SetPlateLock.Response
        )

        HeatCoolShakeDeviceABC.Deinitialize(self)

    def SetTemperature(self, Temperature: float):
        if Temperature < 25:
            raise CoolingNotSupportedError

        CommandInstance = HeaterShakerDriver.StartTemperatureControl.Command(
            Options=HeaterShakerDriver.StartTemperatureControl.Options(
                HandleID=int(self.HandleID),
                Temperature=Temperature,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.Backend.GetResponse(
            CommandInstance, HeaterShakerDriver.StartTemperatureControl.Response
        )

    def SetTemperatureTime(self, Temperature: float) -> float:
        return 0

    def GetTemperature(self) -> float:
        CommandInstance = HeaterShakerDriver.GetTemperature.Command(
            Options=HeaterShakerDriver.GetTemperature.Options(
                HandleID=int(self.HandleID),
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.Backend.GetResponse(
            CommandInstance, HeaterShakerDriver.GetTemperature.Response
        )

        return ResponseInstance.GetTemperature()

    def SetShakingSpeed(self, RPM: int):
        if RPM == 0:
            CommandInstance = HeaterShakerDriver.StopShakeControl.Command(
                Options=HeaterShakerDriver.StopShakeControl.Options(
                    HandleID=int(self.HandleID),
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.Backend.ExecuteCommand(CommandInstance)
            self.Backend.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.Backend.GetResponse(
                CommandInstance, HeaterShakerDriver.StopShakeControl.Response
            )

            CommandInstance = HeaterShakerDriver.SetPlateLock.Command(
                Options=HeaterShakerDriver.SetPlateLock.Options(
                    HandleID=int(self.HandleID), PlateLockState=0
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.Backend.ExecuteCommand(CommandInstance)
            self.Backend.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.Backend.GetResponse(
                CommandInstance, HeaterShakerDriver.SetPlateLock.Response
            )

        else:
            CommandInstance = HeaterShakerDriver.SetPlateLock.Command(
                Options=HeaterShakerDriver.SetPlateLock.Options(
                    HandleID=int(self.HandleID),
                    PlateLockState=1,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.Backend.ExecuteCommand(CommandInstance)
            self.Backend.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.Backend.GetResponse(
                CommandInstance, HeaterShakerDriver.SetPlateLock.Response
            )

            CommandInstance = HeaterShakerDriver.StartShakeControl.Command(
                Options=HeaterShakerDriver.StartShakeControl.Options(
                    HandleID=int(self.HandleID),
                    ShakingSpeed=RPM,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.Backend.ExecuteCommand(CommandInstance)
            self.Backend.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.Backend.GetResponse(
                CommandInstance, HeaterShakerDriver.StartShakeControl.Response
            )

    def GetShakingSpeed(self) -> int:
        CommandInstance = HeaterShakerDriver.GetShakingSpeed.Command(
            Options=HeaterShakerDriver.GetShakingSpeed.Options(
                HandleID=int(self.HandleID),
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.Backend.GetResponse(
            CommandInstance, HeaterShakerDriver.GetShakingSpeed.Response
        )

        return ResponseInstance.GetShakingSpeed()
