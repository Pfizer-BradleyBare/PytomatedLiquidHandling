from abc import abstractmethod
from ....Tools.AbstractClasses import UniqueObjectABC
from ...LayoutItem import LayoutItemTracker, CoverablePosition, NonCoverablePosition
from ...TransportDevice import TransportDeviceTracker
from .TempLimits.TempLimits import TempLimits
from ...Tools.AbstractClasses import InterfaceABC
from dataclasses import dataclass, field


@dataclass
class TempControlDevice(InterfaceABC, UniqueObjectABC):
    ComPort: str | int
    ShakingSupported: bool
    TempLimitsInstance: TempLimits
    SupportedLayoutItemTrackerInstance: LayoutItemTracker
    TransportDeviceTrackerInstance: TransportDeviceTracker

    HandleID: int | str = field(init=False)
    Temperature: float = field(init=False, default=0)
    ShakingSpeed: int = field(init=False, default=0)

    @abstractmethod
    def MoveToDevice(self, SourceLayoutItem: CoverablePosition | NonCoverablePosition):
        ...

    @abstractmethod
    def MoveFromDevice(
        self, DestinationLayoutItem: CoverablePosition | NonCoverablePosition
    ):
        ...

    @abstractmethod
    def SetTemperature(
        self,
        Temperature: float,
    ):
        ...

    @abstractmethod
    def UpdateTemperature(
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
    def UpdateShakingSpeed(
        self,
    ):
        ...
