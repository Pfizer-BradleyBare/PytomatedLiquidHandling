from abc import abstractmethod

from pydantic import PrivateAttr, field_validator

from PytomatedLiquidHandling.HAL import Labware, LayoutItem
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALDevice

from ...Tools.AbstractClasses import Interface
from .FilterPlateConfiguration import FilterPlateConfiguration


class VacuumABC(Interface, HALDevice):
    ComPort: str
    ManifoldPark: LayoutItem.VacuumManifold
    ManifoldProcessing: LayoutItem.VacuumManifold
    SupportedFilterPlateConfigurations: dict[str, FilterPlateConfiguration]

    @field_validator("CoverableLayoutItems", mode="before")
    def __SupportedCoverableLayoutItemsValidate(cls, v):
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
        """TODO

        Must called before calling SetTemperature, SetTemperatureTime, or SetShakingSpeed.

        If any exceptions are thrown then you are trying to use an incompatible device.

        Raises ExceptionGroup of the following:
            Labware.Base.LabwareNotSupportedError

            HeatCoolShakeDevice.Base.CoolingNotSupportedError

            HeatCoolShakeDevice.Base.HeatingNotSupportedError

            HeatCoolShakeDevice.Base.ShakingNotSupportedError
        """

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
