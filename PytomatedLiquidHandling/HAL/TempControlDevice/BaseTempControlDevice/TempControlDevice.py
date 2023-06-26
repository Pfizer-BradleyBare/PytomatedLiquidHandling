from abc import abstractmethod
from ....Tools.AbstractClasses import UniqueObjectABC
from ...LayoutItem import LayoutItemTracker, CoverablePosition, NonCoverablePosition
from ...TransportDevice import TransportDeviceTracker, TransportOptions
from .TempLimits.TempLimits import TempLimits
from ...Tools.AbstractClasses import InterfaceABC
from dataclasses import dataclass, field


@dataclass
class TempControlDevice(InterfaceABC, UniqueObjectABC):
    ComPort: str | int
    ShakingSupported: bool
    TempLimitsInstance: TempLimits
    SupportedLayoutItemTrackerInstance: LayoutItemTracker

    HandleID: int | str = field(init=False)
    Temperature: float = field(init=False, default=0)
    ShakingSpeed: int = field(init=False, default=0)

    def GetLayoutItem(
        self, LayoutItemInstance: CoverablePosition | NonCoverablePosition
    ) -> CoverablePosition:
        for (
            SupportedLayoutItemInstance
        ) in self.SupportedLayoutItemTrackerInstance.GetObjectsAsList():
            if (
                SupportedLayoutItemInstance.LabwareInstance
                == LayoutItemInstance.LabwareInstance
            ):
                if not isinstance(SupportedLayoutItemInstance, CoverablePosition):
                    raise Exception("This should never happen")

                if isinstance(LayoutItemInstance, CoverablePosition):
                    SupportedLayoutItemInstance.IsCovered = LayoutItemInstance.IsCovered
                else:
                    SupportedLayoutItemInstance.IsCovered = False

                return SupportedLayoutItemInstance

        raise Exception("This heater does not support your layout item")

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
