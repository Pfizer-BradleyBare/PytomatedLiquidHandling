from ...Driver.Hamilton.TemperatureControl import HeaterShaker as HeaterShakerDriver
from ..LayoutItem import LayoutItemTracker
from .BaseTempControlDevice import TempControlDevice, TempLimits
from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC


class HamiltonHeaterShaker(TempControlDevice):
    def __init__(
        self,
        UniqueIdentifier: str,
        BackendInstance: HamiltonBackendABC,
        CustomErrorHandling: bool,
        ComPort: str,
        TempLimitsInstance: TempLimits,
        LayoutItemTrackerInstance: LayoutItemTracker,
    ):
        TempControlDevice.__init__(
            self,
            UniqueIdentifier,
            BackendInstance,
            CustomErrorHandling,
            ComPort,
            True,
            TempLimitsInstance,
            LayoutItemTrackerInstance,
        )

    def Initialize(self):
        if not isinstance(self.ComPort, int):
            raise Exception("Should never happen")

        try:
            CommandInstance = HeaterShakerDriver.Connect.Command(
                OptionsInstance=HeaterShakerDriver.Connect.Options(
                    ComPort=self.ComPort,
                ),
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.GetBackend().GetResponse(
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
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.GetBackend().GetResponse(
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
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.GetBackend().GetResponse(
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
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.GetBackend().GetResponse(
                CommandInstance, CommandInstance.Response
            )

        except:
            ...

        try:
            CommandInstance = HeaterShakerDriver.StopShakeControl.Command(
                OptionsInstance=HeaterShakerDriver.StopShakeControl.Options(
                    HandleID=int(self.HandleID)
                ),
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.GetBackend().GetResponse(
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
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.GetBackend().GetResponse(
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
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.GetBackend().GetResponse(
                CommandInstance, CommandInstance.Response
            )

        except:
            ...

    def UpdateCurrentTemperature(self):
        try:
            CommandInstance = HeaterShakerDriver.GetTemperature.Command(
                OptionsInstance=HeaterShakerDriver.GetTemperature.Options(
                    HandleID=int(self.HandleID),
                ),
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.GetBackend().GetResponse(
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
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.GetBackend().GetResponse(
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
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.GetBackend().GetResponse(
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
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.GetBackend().GetResponse(
                CommandInstance, CommandInstance.Response
            )

        except:
            ...

        try:
            CommandInstance = HeaterShakerDriver.SetPlateLock.Command(
                OptionsInstance=HeaterShakerDriver.SetPlateLock.Options(
                    HandleID=int(self.HandleID), PlateLockState=0
                ),
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.GetBackend().GetResponse(
                CommandInstance, CommandInstance.Response
            )

        except:
            ...

    def UpdateCurrentShakingSpeed(self):
        try:
            CommandInstance = HeaterShakerDriver.GetShakingSpeed.Command(
                OptionsInstance=HeaterShakerDriver.GetShakingSpeed.Options(
                    HandleID=int(self.HandleID),
                ),
                CustomErrorHandling=self.GetErrorHandlingSetting(),
            )
            self.GetBackend().ExecuteCommand(CommandInstance)
            self.GetBackend().WaitForResponseBlocking(CommandInstance)
            ResponseInstance = self.GetBackend().GetResponse(
                CommandInstance, CommandInstance.Response
            )

            self.CurrentShakingSpeed = ResponseInstance.GetShakingSpeed()
        except:
            ...
