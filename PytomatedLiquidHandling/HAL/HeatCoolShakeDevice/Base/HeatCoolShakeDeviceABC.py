from abc import abstractmethod
from dataclasses import dataclass, field

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC
from PytomatedLiquidHandling.HAL import Labware, LayoutItem
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject

from ...Tools.AbstractClasses import InterfaceABC
from .TempLimits.TempLimits import TempLimits


@dataclass
class HeatingNotSupportedError(BaseException):
    """Selected HeatCoolShakeDevice does not support heating.

    Attributes:
    None
    """


@dataclass
class CoolingNotSupportedError(BaseException):
    """Selected HeatCoolShakeDevice does not support cooling.

    Attributes:
    None
    """


@dataclass
class ShakingNotSupportedError(BaseException):
    """Selected HeatCoolShakeDevice does not support shaking.

    Attributes:
    None
    """


@dataclass
class HeatCoolShakeDeviceABC(InterfaceABC, HALObject):
    ComPort: str | int
    HeatingSupported: bool
    CoolingSupported: bool
    ShakingSupported: bool
    TempLimitsInstance: TempLimits
    SupportedLayoutItems: list[LayoutItem.CoverableItem]

    HandleID: int | str = field(init=False)

    def ValidateOptions(
        self,
        LayoutItem: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem,
        Temperature: None | float = None,
        RPM: None | int = None,
    ):
        """Must called before calling SetTemperature, SetTemperatureTime, or SetShakingSpeed.

        If any exceptions are thrown then you are trying to use an incompatible device.

        Raises:
            Labware.Base.LabwareNotSupportedError

            HeatCoolShakeDevice.Base.CoolingNotSupportedError

            HeatCoolShakeDevice.Base.HeatingNotSupportedError

            HeatCoolShakeDevice.Base.ShakingNotSupportedError
        """
        SupportedLabwares = [
            LayoutItem.Labware.Identifier for LayoutItem in self.SupportedLayoutItems
        ]

        if LayoutItem.Labware not in SupportedLabwares:
            raise Labware.Base.LabwareNotSupportedError([LayoutItem.Labware])

        if Temperature is not None:
            if Temperature < 25 and not self.CoolingSupported:
                raise CoolingNotSupportedError
            if Temperature > 25 and not self.HeatingSupported:
                raise HeatingNotSupportedError

        if RPM is not None:
            if not self.ShakingSupported:
                raise ShakingNotSupportedError

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
