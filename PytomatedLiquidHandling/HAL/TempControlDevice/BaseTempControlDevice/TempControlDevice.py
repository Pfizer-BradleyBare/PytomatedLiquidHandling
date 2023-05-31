from abc import abstractmethod
from ....Tools.AbstractClasses import UniqueObjectABC
from ...LayoutItem import LayoutItemTracker
from .TempLimits.TempLimits import TempLimits
from ...Tools.AbstractClasses import InterfaceABC
from ....Driver.Tools.AbstractClasses import BackendABC


class TempControlDevice(UniqueObjectABC, InterfaceABC):
    def __init__(
        self,
        UniqueIdentifier: str,
        BackendInstance: BackendABC,
        CustomErrorHandling: bool,
        ComPort: str | int,
        ShakingSupported: bool,
        TempLimitsInstance: TempLimits,
        SupportedLayoutItemTrackerInstance: LayoutItemTracker,
    ):
        UniqueObjectABC.__init__(self, UniqueIdentifier)
        InterfaceABC.__init__(self, BackendInstance, CustomErrorHandling)
        self.ComPort: str | int = ComPort
        self.ShakingSupported: bool = ShakingSupported
        self.TempLimitsInstance: TempLimits = TempLimitsInstance
        self.SupportedLayoutItemTrackerInstance: LayoutItemTracker = (
            SupportedLayoutItemTrackerInstance
        )

        self.HandleID: int | str
        self.CurrentTemperature: float = 0
        self.CurrentShakingSpeed: int = 0

    def GetCurrentShakingSpeed(self) -> int:
        return self.CurrentShakingSpeed

    def GetCurrentTemperature(self) -> float:
        return self.CurrentTemperature

    @abstractmethod
    def SetTemperature(
        self,
        Temperature: float,
    ):
        ...

    @abstractmethod
    def UpdateCurrentTemperature(
        self,
    ):
        ...

    @abstractmethod
    def StartShaking(
        self,
        RPM: float,
    ):
        ...

    @abstractmethod
    def StopShaking(
        self,
    ):
        ...

    @abstractmethod
    def UpdateCurrentShakingSpeed(
        self,
    ):
        ...
