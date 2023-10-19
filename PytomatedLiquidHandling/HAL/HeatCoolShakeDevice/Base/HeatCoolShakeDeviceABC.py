from abc import abstractmethod
from dataclasses import dataclass, field
from pydantic.dataclasses import dataclass as PydanticDataclass
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


@PydanticDataclass
class HeatCoolShakeDeviceABC(InterfaceABC, HALObject):
    ComPort: str | int
    HeatingSupported: bool
    CoolingSupported: bool
    ShakingSupported: bool
    TempLimits: TempLimits
    SupportedCoverableLayoutItems: list[LayoutItem.CoverableItem]

    HandleID: int | str = field(init=False, default="")

    def ValidateOptions(
        self,
        LayoutItem: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem,
        Temperature: None | float = None,
        RPM: None | int = None,
    ):
        """Must called before calling SetTemperature, SetTemperatureTime, or SetShakingSpeed.

        If any exceptions are thrown then you are trying to use an incompatible device.

        Raises ExceptionGroup of the following:
            Labware.Base.LabwareNotSupportedError

            HeatCoolShakeDevice.Base.CoolingNotSupportedError

            HeatCoolShakeDevice.Base.HeatingNotSupportedError

            HeatCoolShakeDevice.Base.ShakingNotSupportedError
        """
        Exceptions = list()

        SupportedLabwares = [
            LayoutItem.Labware.Identifier
            for LayoutItem in self.SupportedCoverableLayoutItems
        ]

        if LayoutItem.Labware not in SupportedLabwares:
            Exceptions.append(
                Labware.Base.LabwareNotSupportedError([LayoutItem.Labware])
            )

        if Temperature is not None:
            if Temperature < 25 and not self.CoolingSupported:
                Exceptions.append(CoolingNotSupportedError)
            if Temperature > 25 and not self.HeatingSupported:
                Exceptions.append(HeatingNotSupportedError)

        if RPM is not None:
            if not self.ShakingSupported:
                Exceptions.append(ShakingNotSupportedError)

        if len(Exceptions) > 0:
            raise ExceptionGroup("HeatCoolShakeDevice Options Exceptions", Exceptions)

    def GetLayoutItem(
        self, LayoutItemInstance: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
    ) -> LayoutItem.CoverableItem:
        for SupportedLayoutItemInstance in self.SupportedCoverableLayoutItems:
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
