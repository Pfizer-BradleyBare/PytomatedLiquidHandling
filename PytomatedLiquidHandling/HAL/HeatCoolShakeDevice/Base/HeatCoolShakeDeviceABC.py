from abc import abstractmethod
from dataclasses import dataclass, field

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC
from PytomatedLiquidHandling.HAL import Labware, LayoutItem
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject

from ...Tools.AbstractClasses import InterfaceABC
from .TempLimits.TempLimits import TempLimits


@dataclass
class HeatingNotSupportedError(BaseException):
    ...


@dataclass
class CoolingNotSupportedError(BaseException):
    ...


@dataclass
class ShakingNotSupportedError(BaseException):
    ...


@dataclass
class HeatCoolShakeDeviceABC(InterfaceABC, HALObject):
    ComPort: str | int
    HeatingSupported: bool
    CoolingSupported: bool
    ShakingSupported: bool
    TempLimitsInstance: TempLimits
    SupportedLayoutItems: list[LayoutItem.CoverableItem]

    HandleID: int | str = field(init=False)

    def IsLayoutItemSupported(
        self, LayoutItem: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
    ) -> bool:
        Labwares = [
            LayoutItem.Labware.Identifier for LayoutItem in self.SupportedLayoutItems
        ]

        if LayoutItem.Labware.Identifier in Labwares:
            return True
        else:
            return False

    def GetLayoutItem(
        self, LayoutItemInstance: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
    ) -> LayoutItem.CoverableItem:
        for SupportedLayoutItemInstance in self.SupportedLayoutItems:
            if SupportedLayoutItemInstance.Labware == LayoutItemInstance.Labware:
                if isinstance(LayoutItemInstance, LayoutItem.CoverableItem):
                    SupportedLayoutItemInstance.IsCovered = LayoutItemInstance.IsCovered
                else:
                    SupportedLayoutItemInstance.IsCovered = False

                return SupportedLayoutItemInstance

        raise Exception([LayoutItemInstance.Labware])

    @abstractmethod
    def SetTemperature(self, Temperature: float):
        ...

    @abstractmethod
    def SetTemperatureTime(self, Temperature: float) -> float:
        ...

    @abstractmethod
    def GetTemperature(self) -> float:
        ...

    @abstractmethod
    def SetShakingSpeed(self, RPM: int):
        ...

    @abstractmethod
    def GetShakingSpeed(self) -> int:
        ...
