from abc import abstractmethod

from pydantic import PrivateAttr, field_validator

from PytomatedLiquidHandling.HAL import Labware, LayoutItem
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALDevice

from ...Tools.AbstractClasses import Interface
from .Exceptions import (
    CoolingNotSupportedError,
    HeatingNotSupportedError,
    ShakingNotSupportedError,
)
from .TempLimits.TempLimits import TempLimits


class HeatCoolShakeABC(Interface, HALDevice):
    ComPort: str | int
    TempLimits: TempLimits
    CoverablePlates: list[LayoutItem.CoverablePlate]

    _HeatingSupported: bool = PrivateAttr(False)
    _CoolingSupported: bool = PrivateAttr(False)
    _ShakingSupported: bool = PrivateAttr(False)
    _HandleID: int | str = PrivateAttr()

    @field_validator("CoverablePlates", mode="before")
    def __SupportedCoverablePlatesValidate(cls, v):
        SupportedObjects = list()

        Objects = LayoutItem.Devices

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

    def AssertOptions(
        self,
        LayoutItem: LayoutItem.CoverablePlate | LayoutItem.Plate,
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
            LayoutItem.Labware.Identifier for LayoutItem in self.CoverablePlates
        ]

        if LayoutItem.Labware not in SupportedLabwares:
            Exceptions.append(
                Labware.Base.Exceptions.LabwareNotSupportedError([LayoutItem.Labware])
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
        self,
        LayoutItemInstance: LayoutItem.CoverablePlate | LayoutItem.Plate,
    ) -> LayoutItem.CoverablePlate:
        for SupportedLayoutItemInstance in self.CoverablePlates:
            if SupportedLayoutItemInstance.Labware == LayoutItemInstance.Labware:
                if isinstance(LayoutItemInstance, LayoutItem.CoverablePlate):
                    SupportedLayoutItemInstance.IsCovered = LayoutItemInstance.IsCovered
                else:
                    SupportedLayoutItemInstance.IsCovered = False

                return SupportedLayoutItemInstance

        raise Exception([LayoutItemInstance.Labware])

    @abstractmethod
    def SetTemperature(self, Temperature: float):
        ...

    @abstractmethod
    def TimeToTemperature(self, Temperature: float) -> float:
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