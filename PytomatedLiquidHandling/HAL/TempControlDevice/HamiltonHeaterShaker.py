from ...Driver.Hamilton.TemperatureControl import HeaterShaker as HeaterShakerDriver
from .BaseTempControlDevice import TempControlDevice
from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from dataclasses import dataclass, field


@dataclass
class HamiltonHeaterShaker(TempControlDevice):
    BackendInstance: HamiltonBackendABC
    ShakingSupported: bool = field(init=False, default=True)
    HandleID: int = field(init=False)

    def Initialize(self):
        if not isinstance(self.ComPort, int):
            raise Exception("Should never happen")

        try:
            CommandInstance = HeaterShakerDriver.Connect.Command(
                OptionsInstance=HeaterShakerDriver.Connect.Options(
                    ComPort=self.ComPort,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.BackendInstance.ExecuteCommand(CommandInstance)
            self.BackendInstance.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.BackendInstance.GetResponse(
                CommandInstance, CommandInstance.Response
            )

            self.HandleID = ResponseInstance.GetHandleID()
        except:
            ...

        try:
            CommandInstance = HeaterShakerDriver.SetPlateLock.Command(
                OptionsInstance=HeaterShakerDriver.SetPlateLock.Options(
                    HandleID=int(self.HandleID),
                    PlateLockState=1,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.BackendInstance.ExecuteCommand(CommandInstance)
            self.BackendInstance.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.BackendInstance.GetResponse(
                CommandInstance, CommandInstance.Response
            )

        except:
            ...

        try:
            CommandInstance = HeaterShakerDriver.SetPlateLock.Command(
                OptionsInstance=HeaterShakerDriver.SetPlateLock.Options(
                    HandleID=int(self.HandleID),
                    PlateLockState=0,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.BackendInstance.ExecuteCommand(CommandInstance)
            self.BackendInstance.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.BackendInstance.GetResponse(
                CommandInstance, CommandInstance.Response
            )

        except:
            ...

    def Deinitialize(self):
        try:
            CommandInstance = HeaterShakerDriver.StopTemperatureControl.Command(
                OptionsInstance=HeaterShakerDriver.StopTemperatureControl.Options(
                    HandleID=int(self.HandleID),
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.BackendInstance.ExecuteCommand(CommandInstance)
            self.BackendInstance.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.BackendInstance.GetResponse(
                CommandInstance, CommandInstance.Response
            )

        except:
            ...

        try:
            CommandInstance = HeaterShakerDriver.StopShakeControl.Command(
                OptionsInstance=HeaterShakerDriver.StopShakeControl.Options(
                    HandleID=int(self.HandleID)
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.BackendInstance.ExecuteCommand(CommandInstance)
            self.BackendInstance.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.BackendInstance.GetResponse(
                CommandInstance, CommandInstance.Response
            )

        except:
            ...

        try:
            CommandInstance = HeaterShakerDriver.SetPlateLock.Command(
                OptionsInstance=HeaterShakerDriver.SetPlateLock.Options(
                    HandleID=int(self.HandleID),
                    PlateLockState=0,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.BackendInstance.ExecuteCommand(CommandInstance)
            self.BackendInstance.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.BackendInstance.GetResponse(
                CommandInstance, CommandInstance.Response
            )

        except:
            ...

    def SetTemperature(self, *, Temperature: float):
        try:
            CommandInstance = HeaterShakerDriver.StartTemperatureControl.Command(
                OptionsInstance=HeaterShakerDriver.StartTemperatureControl.Options(
                    HandleID=int(self.HandleID),
                    Temperature=Temperature,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.BackendInstance.ExecuteCommand(CommandInstance)
            self.BackendInstance.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.BackendInstance.GetResponse(
                CommandInstance, CommandInstance.Response
            )

        except:
            ...

    def UpdateTemperature(self):
        try:
            CommandInstance = HeaterShakerDriver.GetTemperature.Command(
                OptionsInstance=HeaterShakerDriver.GetTemperature.Options(
                    HandleID=int(self.HandleID),
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.BackendInstance.ExecuteCommand(CommandInstance)
            self.BackendInstance.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.BackendInstance.GetResponse(
                CommandInstance, CommandInstance.Response
            )

            self.CurrentTemperature = ResponseInstance.GetTemperature()
        except:
            ...

    def StartShaking(self, *, RPM: int):
        try:
            CommandInstance = HeaterShakerDriver.SetPlateLock.Command(
                OptionsInstance=HeaterShakerDriver.SetPlateLock.Options(
                    HandleID=int(self.HandleID),
                    PlateLockState=1,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.BackendInstance.ExecuteCommand(CommandInstance)
            self.BackendInstance.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.BackendInstance.GetResponse(
                CommandInstance, CommandInstance.Response
            )

        except:
            ...

        try:
            CommandInstance = HeaterShakerDriver.StartShakeControl.Command(
                OptionsInstance=HeaterShakerDriver.StartShakeControl.Options(
                    HandleID=int(self.HandleID),
                    ShakingSpeed=RPM,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.BackendInstance.ExecuteCommand(CommandInstance)
            self.BackendInstance.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.BackendInstance.GetResponse(
                CommandInstance, CommandInstance.Response
            )

        except:
            ...

    def StopShaking(self):
        try:
            CommandInstance = HeaterShakerDriver.StopShakeControl.Command(
                OptionsInstance=HeaterShakerDriver.StopShakeControl.Options(
                    HandleID=int(self.HandleID),
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.BackendInstance.ExecuteCommand(CommandInstance)
            self.BackendInstance.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.BackendInstance.GetResponse(
                CommandInstance, CommandInstance.Response
            )

        except:
            ...

        try:
            CommandInstance = HeaterShakerDriver.SetPlateLock.Command(
                OptionsInstance=HeaterShakerDriver.SetPlateLock.Options(
                    HandleID=int(self.HandleID), PlateLockState=0
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.BackendInstance.ExecuteCommand(CommandInstance)
            self.BackendInstance.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.BackendInstance.GetResponse(
                CommandInstance, CommandInstance.Response
            )

        except:
            ...

    def UpdateShakingSpeed(self):
        try:
            CommandInstance = HeaterShakerDriver.GetShakingSpeed.Command(
                OptionsInstance=HeaterShakerDriver.GetShakingSpeed.Options(
                    HandleID=int(self.HandleID),
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.BackendInstance.ExecuteCommand(CommandInstance)
            self.BackendInstance.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.BackendInstance.GetResponse(
                CommandInstance, CommandInstance.Response
            )

            self.CurrentShakingSpeed = ResponseInstance.GetShakingSpeed()
        except:
            ...
