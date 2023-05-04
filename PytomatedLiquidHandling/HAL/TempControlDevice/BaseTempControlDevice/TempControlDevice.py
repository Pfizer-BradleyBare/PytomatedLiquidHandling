from enum import Enum

from ....Tools.AbstractClasses import UniqueObjectABC
from ...LayoutItem import LayoutItemTracker
from .Interface.TempControlDeviceInterface import TempControlDeviceInterface
from .TempLimits.TempLimits import TempLimits


class DeviceTypes(Enum):
    HamiltonHeaterShaker = "Hamilton Heater Shaker"
    HamiltonHeaterCooler = "Hamilton Heater Cooler"


class TempControlDevice(UniqueObjectABC, TempControlDeviceInterface):
    def __init__(
        self,
        UniqueIdentifier: str,
        ComPort: str | int,
        ShakingSupported: bool,
        TempLimitsInstance: TempLimits,
        SupportedLayoutItemTrackerInstance: LayoutItemTracker,
    ):
        UniqueObjectABC.__init__(self, UniqueIdentifier)
        self.ComPort: str | int = ComPort
        self.ShakingSupported: bool = ShakingSupported
        self.TempLimitsInstance: TempLimits = TempLimitsInstance
        self.SupportedLayoutItemTrackerInstance: LayoutItemTracker = (
            SupportedLayoutItemTrackerInstance
        )
