from enum import Enum
from ..Layout import CoveredLayoutItem
from ...AbstractClasses import ObjectABC


class TempConfig:
    def __init__(
        self,
        AmbientTemp: float,
        StableTempDelta: float,
        MinimumTemp: float,
        MaximumTemp: float,
    ):
        self.AmbientTemp: float = AmbientTemp
        self.StableTempDelta: float = StableTempDelta
        self.MinimumTemp: float = MinimumTemp
        self.MaximumTemp: float = MaximumTemp


class DeviceTypes(Enum):
    HamiltonHeaterShaker = "Hamilton Heater Shaker"
    HamiltonHeaterCooler = "Hamilton Heater Cooler"


class TempControlDevice(ObjectABC):
    def __init__(
        self,
        Name: str,
        ComPort: str,
        DeviceType: DeviceTypes,
        Config: TempConfig,
        LayoutItems: list[CoveredLayoutItem],
    ):
        self.Name: str = Name
        self.ComPort: str = ComPort
        self.DeviceType: DeviceTypes = DeviceType
        self.Config: TempConfig = Config
        self.LayoutItems: list[CoveredLayoutItem] = LayoutItems

    def GetName(self) -> str:
        return self.Name

    def GetComPort(self) -> str:
        return self.ComPort

    def GetDeviceType(self) -> DeviceTypes:
        return self.DeviceType

    def GetTempConfig(self) -> TempConfig:
        return self.Config

    def GetLayoutItems(self) -> list[CoveredLayoutItem]:
        return self.LayoutItems
