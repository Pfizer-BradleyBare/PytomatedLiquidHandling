from dataclasses import dataclass, field

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.TemperatureControl import HeaterShaker as HeaterShakerDriver
from .BaseTempControlDevice import TempControlDevice


@dataclass
class HamiltonHeaterShaker(TempControlDevice):
    BackendInstance: HamiltonBackendABC
    ShakingSupported: bool = field(init=False, default=True)
    HandleID: int = field(init=False)

    def Initialize(self):
        TempControlDevice.Initialize(self)

        if not isinstance(self.ComPort, int):
            raise Exception("Should never happen")

        CommandInstance = HeaterShakerDriver.Connect.Command(
            OptionsInstance=HeaterShakerDriver.Connect.Options(
                ComPort=self.ComPort,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.BackendInstance.GetResponse(
            CommandInstance, HeaterShakerDriver.Connect.Response
        )

        self.HandleID = ResponseInstance.GetHandleID()

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
            CommandInstance, HeaterShakerDriver.SetPlateLock.Response
        )

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
            CommandInstance, HeaterShakerDriver.SetPlateLock.Response
        )

    def Deinitialize(self):
        TempControlDevice.Deinitialize(self)

        CommandInstance = HeaterShakerDriver.StopTemperatureControl.Command(
            OptionsInstance=HeaterShakerDriver.StopTemperatureControl.Options(
                HandleID=int(self.HandleID),
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.BackendInstance.GetResponse(
            CommandInstance, HeaterShakerDriver.StopTemperatureControl.Response
        )

        CommandInstance = HeaterShakerDriver.StopShakeControl.Command(
            OptionsInstance=HeaterShakerDriver.StopShakeControl.Options(
                HandleID=int(self.HandleID)
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.BackendInstance.GetResponse(
            CommandInstance, HeaterShakerDriver.StopShakeControl.Response
        )

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
            CommandInstance, HeaterShakerDriver.SetPlateLock.Response
        )

    @TempControlDevice.SetTemperature.setter
    def SetTemperature(self, *, NewTemperature: float):
        CommandInstance = HeaterShakerDriver.StartTemperatureControl.Command(
            OptionsInstance=HeaterShakerDriver.StartTemperatureControl.Options(
                HandleID=int(self.HandleID),
                Temperature=NewTemperature,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.BackendInstance.GetResponse(
            CommandInstance, HeaterShakerDriver.StartTemperatureControl.Response
        )

    def _UpdateActualTemperature(self):
        CommandInstance = HeaterShakerDriver.GetTemperature.Command(
            OptionsInstance=HeaterShakerDriver.GetTemperature.Options(
                HandleID=int(self.HandleID),
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.BackendInstance.GetResponse(
            CommandInstance, HeaterShakerDriver.GetTemperature.Response
        )

        self._ActualTemperature = ResponseInstance.GetTemperature()

    @TempControlDevice.SetShakingSpeed.setter
    def SetShakingSpeed(self, NewRPM: int):
        if NewRPM == 0:
            CommandInstance = HeaterShakerDriver.StopShakeControl.Command(
                OptionsInstance=HeaterShakerDriver.StopShakeControl.Options(
                    HandleID=int(self.HandleID),
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.BackendInstance.ExecuteCommand(CommandInstance)
            self.BackendInstance.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.BackendInstance.GetResponse(
                CommandInstance, HeaterShakerDriver.StopShakeControl.Response
            )

            CommandInstance = HeaterShakerDriver.SetPlateLock.Command(
                OptionsInstance=HeaterShakerDriver.SetPlateLock.Options(
                    HandleID=int(self.HandleID), PlateLockState=0
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.BackendInstance.ExecuteCommand(CommandInstance)
            self.BackendInstance.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.BackendInstance.GetResponse(
                CommandInstance, HeaterShakerDriver.SetPlateLock.Response
            )

        else:
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
                CommandInstance, HeaterShakerDriver.SetPlateLock.Response
            )

            CommandInstance = HeaterShakerDriver.StartShakeControl.Command(
                OptionsInstance=HeaterShakerDriver.StartShakeControl.Options(
                    HandleID=int(self.HandleID),
                    ShakingSpeed=NewRPM,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.BackendInstance.ExecuteCommand(CommandInstance)
            self.BackendInstance.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.BackendInstance.GetResponse(
                CommandInstance, HeaterShakerDriver.StartShakeControl.Response
            )

    def _UpdateActualShakingSpeed(self):
        CommandInstance = HeaterShakerDriver.GetShakingSpeed.Command(
            OptionsInstance=HeaterShakerDriver.GetShakingSpeed.Options(
                HandleID=int(self.HandleID),
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.BackendInstance.GetResponse(
            CommandInstance, HeaterShakerDriver.GetShakingSpeed.Response
        )

        self._ActualShakingSpeed = ResponseInstance.GetShakingSpeed()
