from dataclasses import dataclass, field

from PytomatedLiquidHandling.HAL.TempControlDevice.BaseTempControlDevice.TempControlDevice import (
    SetTemperatureInterfaceCommand,
)

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.TemperatureControl import HeaterShaker as HeaterShakerDriver
from .BaseTempControlDevice import TempControlDevice


@dataclass
class HamiltonHeaterShaker(TempControlDevice):
    BackendInstance: HamiltonBackendABC
    HeatingSupported: bool = field(init=False, default=True)
    CoolingSupported: bool = field(init=False, default=False)
    ShakingSupported: bool = field(init=False, default=True)
    HandleID: int = field(init=False)

    def _Initialize(self):
        TempControlDevice._Initialize(self)

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

    def _InitializeTime(self) -> float:
        return 0

    def _Deinitialize(self):
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

        TempControlDevice._Deinitialize(self)

    def _DeinitializeTime(self) -> float:
        return 0

    def _SetTemperature(
        self, OptionsInstance: TempControlDevice.SetTemperature.Options
    ):
        CommandInstance = HeaterShakerDriver.StartTemperatureControl.Command(
            OptionsInstance=HeaterShakerDriver.StartTemperatureControl.Options(
                HandleID=int(self.HandleID),
                Temperature=OptionsInstance.Temperature,
            ),
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.BackendInstance.ExecuteCommand(CommandInstance)
        self.BackendInstance.WaitForResponseBlocking(CommandInstance)
        ResponseInstance = self.BackendInstance.GetResponse(
            CommandInstance, HeaterShakerDriver.StartTemperatureControl.Response
        )

    def _SetTemperatureTime(
        self, OptionsInstance: TempControlDevice.SetTemperature.Options
    ) -> float:
        return 0

    def _GetTemperature(self) -> float:
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

        return ResponseInstance.GetTemperature()

    def _GetTemperatureTime(self) -> float:
        return 0

    def _SetShakingSpeed(
        self, OptionsInstance: TempControlDevice.SetShakingSpeed.Options
    ):
        if OptionsInstance.ShakingSpeed == 0:
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
                    ShakingSpeed=OptionsInstance.ShakingSpeed,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.BackendInstance.ExecuteCommand(CommandInstance)
            self.BackendInstance.WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.BackendInstance.GetResponse(
                CommandInstance, HeaterShakerDriver.StartShakeControl.Response
            )

    def _SetShakingSpeedTime(
        self, OptionsInstance: TempControlDevice.SetShakingSpeed.Options
    ) -> float:
        return 0

    def _GetShakingSpeed(self) -> int:
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

        return ResponseInstance.GetShakingSpeed()

    def _GetShakingSpeedTime(self) -> float:
        return 0
