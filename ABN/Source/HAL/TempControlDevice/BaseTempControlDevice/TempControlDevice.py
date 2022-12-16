from enum import Enum

from ....Tools.AbstractClasses import ObjectABC
from ...Layout import LayoutTracker
from .Interface.TempControlDeviceInterface import TempControlDeviceInterface
from .TempLimits.TempLimits import TempLimits


class DeviceTypes(Enum):
    HamiltonHeaterShaker = "Hamilton Heater Shaker"
    HamiltonHeaterCooler = "Hamilton Heater Cooler"


class TempControlDevice(ObjectABC, TempControlDeviceInterface):
    def __init__(
        self,
        Name: str,
        ComPort: str,
        ShakingSupported: bool,
        TempLimitsInstance: TempLimits,
        LayoutTrackerInstance: LayoutTracker,
    ):
        self.Name: str = Name
        self.ComPort: str = ComPort
        self.ShakingSupported: bool = ShakingSupported
        self.TempLimitsInstance: TempLimits = TempLimitsInstance
        self.LayoutTrackerInstance: LayoutTracker = LayoutTrackerInstance

    def GetName(self) -> str:
        return self.Name
