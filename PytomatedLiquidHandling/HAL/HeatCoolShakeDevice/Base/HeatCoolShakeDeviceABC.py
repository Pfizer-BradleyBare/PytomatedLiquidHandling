from abc import abstractmethod
from dataclasses import dataclass, field

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC
from PytomatedLiquidHandling.HAL import Labware, LayoutItem
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject

from ...Tools.AbstractClasses import InterfaceABC
from .TempLimits.TempLimits import TempLimits


@dataclass
class HeatCoolShakeDeviceABC(InterfaceABC, HALObject):
    @dataclass
    class SetTemperatureOptions(OptionsABC):
        Temperature: float

    @dataclass
    class SetShakingSpeedOptions(OptionsABC):
        ShakingSpeed: int

    ComPort: str | int
    HeatingSupported: bool
    CoolingSupported: bool
    ShakingSupported: bool
    TempLimitsInstance: TempLimits
    SupportedLayoutItems: list[LayoutItem.Base.LayoutItemABC]

    HandleID: int | str = field(init=False)

    def IsLabwareSupported(self, LabwareInstance: Labware.PipettableLabware) -> bool:
        Labwares = [
            LayoutItem.Labware.Identifier for LayoutItem in self.SupportedLayoutItems
        ]

        if LabwareInstance.Identifier in Labwares:
            return True
        else:
            return False

    def GetLayoutItem(
        self, LayoutItemInstance: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
    ) -> LayoutItem.CoverableItem:
        for SupportedLayoutItemInstance in self.SupportedLayoutItems:
            if SupportedLayoutItemInstance.Labware == LayoutItemInstance.Labware:
                if not isinstance(
                    SupportedLayoutItemInstance, LayoutItem.CoverableItem
                ):
                    raise Exception("This should never happen")

                if isinstance(LayoutItemInstance, LayoutItem.CoverableItem):
                    SupportedLayoutItemInstance.IsCovered = LayoutItemInstance.IsCovered
                else:
                    SupportedLayoutItemInstance.IsCovered = False

                return SupportedLayoutItemInstance

        raise Exception("This heater does not support your layout item")

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
    def GetTemperatureTime(self) -> float:
        ...

    @abstractmethod
    def SetShakingSpeed(self, OptionsInstance: SetShakingSpeedOptions):
        ...

    @abstractmethod
    def SetShakingSpeedTime(self, OptionsInstance: SetShakingSpeedOptions) -> float:
        ...

    @abstractmethod
    def GetShakingSpeed(self) -> int:
        ...

    @abstractmethod
    def GetShakingSpeedTime(self) -> float:
        ...
