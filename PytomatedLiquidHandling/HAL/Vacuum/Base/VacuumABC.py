from abc import abstractmethod

from pydantic import PrivateAttr, field_validator

from PytomatedLiquidHandling.HAL import LayoutItem
from PytomatedLiquidHandling.HAL.Tools.BaseClasses import HALDevice

from ...Tools.BaseClasses import Interface
from .FilterPlateConfiguration import FilterPlateConfiguration


class VacuumABC(Interface, HALDevice):
    ComPort: str
    ManifoldPark: LayoutItem.VacuumManifold
    ManifoldProcessing: LayoutItem.VacuumManifold
    SupportedFilterPlateConfigurations: dict[str, FilterPlateConfiguration]
    _HandleID: int = PrivateAttr()

    @field_validator("ManifoldPark", "ManifoldProcessing", mode="before")
    def __ManifoldsValidate(cls, v):
        Identifier = v

        Objects = LayoutItem.Devices

        if Identifier not in Objects:
            raise ValueError(
                Identifier
                + " is not found in "
                + LayoutItem.Base.LayoutItemABC.__name__
                + " objects."
            )

        return Objects[Identifier]

    def AssertOptions(
        self,
        LayoutItem: LayoutItem.CoverablePlate | LayoutItem.Plate,
        Pressure: None | float = None,
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
    def SetVacuumPressure(self, Pressure: float):
        ...
