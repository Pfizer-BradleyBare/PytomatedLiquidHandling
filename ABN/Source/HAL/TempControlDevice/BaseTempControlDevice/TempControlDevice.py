from enum import Enum

from ....Tools.AbstractClasses import ObjectABC
from ...Layout import LayoutItemTracker
from .Interface.TempControlDeviceInterface import TempControlDeviceInterface
from .TempLimits.TempLimits import TempLimits


class DeviceTypes(Enum):
    HamiltonHeaterShaker = "Hamilton Heater Shaker"
    HamiltonHeaterCooler = "Hamilton Heater Cooler"


class TempControlDevice(ObjectABC, TempControlDeviceInterface):
    def __init__(
        self,
        Name: str,
        ComPort: str | int,
        ShakingSupported: bool,
        TempLimitsInstance: TempLimits,
        SupportedLayoutItemTrackerInstance: LayoutItemTracker,
    ):
        self.Name: str = Name
        self.ComPort: str | int = ComPort
        self.ShakingSupported: bool = ShakingSupported
        self.TempLimitsInstance: TempLimits = TempLimitsInstance
        self.SupportedLayoutItemTrackerInstance: LayoutItemTracker = (
            SupportedLayoutItemTrackerInstance
        )

    def GetName(self) -> str:
        return self.Name
