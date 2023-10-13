from abc import abstractmethod
from dataclasses import dataclass, field

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC
from PytomatedLiquidHandling.HAL import LayoutItem, LabwareNotSupportedError, Labware
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
class SetTemperatureOptions(OptionsABC):
    Temperature: float


@dataclass
class SetShakingSpeedOptions(OptionsABC):
    ShakingSpeed: int


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

        raise LabwareNotSupportedError([LayoutItemInstance.Labware])

    @abstractmethod
    def SetTemperature(self, OptionsInstance: SetTemperatureOptions):
        ...

    @abstractmethod
    def SetTemperatureTime(self, OptionsInstance: SetTemperatureOptions) -> float:
        ...

    @abstractmethod
    def GetTemperature(self) -> float:
        ...

    @abstractmethod
    def SetShakingSpeed(self, OptionsInstance: SetShakingSpeedOptions):
        ...

    @abstractmethod
    def GetShakingSpeed(self) -> int:
        ...
