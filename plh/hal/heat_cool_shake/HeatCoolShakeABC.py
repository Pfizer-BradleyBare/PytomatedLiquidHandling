from abc import abstractmethod
from dataclasses import field

from pydantic import dataclasses, field_validator

from plh.hal import Labware, LayoutItem
from plh.hal.tools import HALDevice

from ...Tools.BaseClasses import Interface


@dataclasses.dataclass(kw_only=True)
class HeatCoolShakeABC(Interface, HALDevice):
    ComPort: str | int
    Plates: list[LayoutItem.CoverablePlate | LayoutItem.Plate]
    _HandleID: int | str = field(init=False)

    @field_validator("Plates", mode="before")
    def __SupportedPlatesValidate(cls, v):
        SupportedObjects = list()

        Objects = LayoutItem.Devices

        for Identifier in v:
            if Identifier not in Objects:
                raise ValueError(
                    Identifier
                    + " is not found in "
                    + LayoutItem.Base.LayoutItemBase.__name__
                    + " objects.",
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
            LayoutItem.Labware.Identifier for LayoutItem in self.Plates
        ]

        if LayoutItem.Labware not in SupportedLabwares:
            Exceptions.append(
                Labware.Base.Exceptions.LabwareNotSupportedError([LayoutItem.Labware]),
            )

        if len(Exceptions) > 0:
            raise ExceptionGroup("HeatCoolShakeDevice Options Exceptions", Exceptions)

    def GetLayoutItem(
        self,
        LayoutItemInstance: LayoutItem.CoverablePlate | LayoutItem.Plate,
    ) -> LayoutItem.CoverablePlate | LayoutItem.Plate:
        for SupportedLayoutItemInstance in self.Plates:
            if SupportedLayoutItemInstance.Labware == LayoutItemInstance.Labware:
                if isinstance(SupportedLayoutItemInstance, LayoutItem.CoverablePlate):
                    if isinstance(LayoutItemInstance, LayoutItem.CoverablePlate):
                        SupportedLayoutItemInstance.IsCovered = (
                            LayoutItemInstance.IsCovered
                        )
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
