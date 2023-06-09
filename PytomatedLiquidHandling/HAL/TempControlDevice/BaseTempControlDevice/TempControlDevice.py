from abc import abstractmethod
from dataclasses import dataclass, field

from PytomatedLiquidHandling.HAL import LayoutItem

from ....Tools.AbstractClasses import UniqueObjectABC
from ...Tools.AbstractClasses import InterfaceABC
from .TempLimits.TempLimits import TempLimits


@dataclass
class TempControlDevice(InterfaceABC, UniqueObjectABC):
    ComPort: str | int
    ShakingSupported: bool
    TempLimitsInstance: TempLimits
    SupportedLayoutItemTrackerInstance: LayoutItem.LayoutItemTracker

    HandleID: int | str = field(init=False)
    _ActualTemperature: float = field(init=False, default=0)
    _ActualShakingSpeed: int = field(init=False, default=0)
    _SetTemperature: float = field(init=False, default=0)
    _SetShakingSpeed: int = field(init=False, default=0)

    def GetLayoutItem(
        self, LayoutItemInstance: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
    ) -> LayoutItem.CoverableItem:
        for (
            SupportedLayoutItemInstance
        ) in self.SupportedLayoutItemTrackerInstance.GetObjectsAsList():
            if (
                SupportedLayoutItemInstance.LabwareInstance
                == LayoutItemInstance.LabwareInstance
            ):
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

    @property
    def SetTemperature(self) -> float:
        return self._SetTemperature

    @SetTemperature.setter
    @abstractmethod
    def SetTemperature(self, NewTemperature: float):
        ...

    @property
    def ActualTemperature(self) -> float:
        self._UpdateActualTemperature()
        return self._ActualTemperature

    @abstractmethod
    def _UpdateActualTemperature(
        self,
    ):
        ...

    @property
    def SetShakingSpeed(self) -> int:
        return self._SetShakingSpeed

    @SetShakingSpeed.setter
    @abstractmethod
    def SetShakingSpeed(self, NewRPM: int):
        ...

    @property
    def ActualShakingSpeed(self) -> int:
        self._UpdateActualShakingSpeed()
        return self._ActualShakingSpeed

    @abstractmethod
    def _UpdateActualShakingSpeed(
        self,
    ):
        ...
