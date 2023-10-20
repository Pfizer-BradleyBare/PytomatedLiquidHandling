from abc import abstractmethod
from dataclasses import dataclass, field

from pydantic import PrivateAttr, field_validator

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC
from PytomatedLiquidHandling.HAL import Labware, LayoutItem
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject

from ...Tools.AbstractClasses import Interface
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


class HeatCoolShakeDeviceABC(Interface, HALObject):
    ComPort: str | int
    TempLimits: TempLimits
    CoverableLayoutItems: list[LayoutItem.CoverableItem]

    _HeatingSupported: bool = PrivateAttr(False)
    _CoolingSupported: bool = PrivateAttr(False)
    _ShakingSupported: bool = PrivateAttr(False)
    _HandleID: int | str = PrivateAttr()

    @field_validator("CoverableLayoutItems", mode="before")
    def __SupportedCoverableLayoutItemsValidate(cls, v):
        SupportedObjects = list()

        Objects = LayoutItem.GetObjects()

        for Identifier in v:
            if Identifier not in Objects:
                raise ValueError(
                    Identifier
                    + " is not found in "
                    + LayoutItem.Base.LayoutItemABC.__name__
                    + " objects."
                )

            SupportedObjects.append(Objects[Identifier])

        return SupportedObjects

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
            LayoutItem.Labware.Identifier for LayoutItem in self.CoverableLayoutItems
        ]

        if LayoutItem.Labware not in SupportedLabwares:
            Exceptions.append(
                Labware.Base.LabwareNotSupportedError([LayoutItem.Labware])
            )

        if Temperature is not None:
            if Temperature < 25 and not self._CoolingSupported:
                Exceptions.append(CoolingNotSupportedError)
            if Temperature > 25 and not self._HeatingSupported:
                Exceptions.append(HeatingNotSupportedError)

        if RPM is not None:
            if not self._ShakingSupported:
                Exceptions.append(ShakingNotSupportedError)

        if len(Exceptions) > 0:
            raise ExceptionGroup("HeatCoolShakeDevice Options Exceptions", Exceptions)

    def GetLayoutItem(
        self, LayoutItemInstance: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
    ) -> LayoutItem.CoverableItem:
        for SupportedLayoutItemInstance in self.CoverableLayoutItems:
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
