from abc import abstractmethod
from dataclasses import dataclass, field

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC
from PytomatedLiquidHandling.HAL import Labware, LayoutItem
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from ...Tools.AbstractClasses import (
    InterfaceABC,
    InterfaceCommandABC,
    OptionsInterfaceCommandABC,
)
from .TempLimits.TempLimits import TempLimits


@dataclass
class TempControlDevice(InterfaceABC, UniqueObjectABC):
    class SetTemperatureInterfaceCommand(OptionsInterfaceCommandABC[None]):
        @dataclass
        class Options(OptionsABC):
            Temperature: float

    class GetTemperatureInterfaceCommand(InterfaceCommandABC[float]):
        ...

    class SetShakingSpeedInterfaceCommand(OptionsInterfaceCommandABC[None]):
        @dataclass
        class Options(OptionsABC):
            ShakingSpeed: int

    class GetShakingSpeedInterfaceCommand(InterfaceCommandABC[int]):
        ...

    ComPort: str | int
    HeatingSupported: bool
    CoolingSupported: bool
    ShakingSupported: bool
    TempLimitsInstance: TempLimits
    SupportedLayoutItemTrackerInstance: LayoutItem.LayoutItemTracker

    HandleID: int | str = field(init=False)

    SetTemperature: SetTemperatureInterfaceCommand = field(init=False)
    GetTemperature: GetTemperatureInterfaceCommand = field(init=False)
    SetShakingSpeed: SetShakingSpeedInterfaceCommand = field(init=False)
    GetShakingSpeed: GetShakingSpeedInterfaceCommand = field(init=False)

    def IsLabwareSupported(self, LabwareInstance: Labware.PipettableLabware) -> bool:
        Labwares = [
            LayoutItem.LabwareInstance.UniqueIdentifier
            for LayoutItem in self.SupportedLayoutItemTrackerInstance.GetObjectsAsList()
        ]

        if LabwareInstance.UniqueIdentifier in Labwares:
            return True
        else:
            return False

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

    @abstractmethod
    def _SetTemperature(self, OptionsInstance: SetTemperatureInterfaceCommand.Options):
        ...

    @abstractmethod
    def _SetTemperatureTime(
        self, OptionsInstance: SetTemperatureInterfaceCommand.Options
    ) -> float:
        ...

    @abstractmethod
    def _GetTemperature(self) -> float:
        ...

    @abstractmethod
    def _GetTemperatureTime(self) -> float:
        ...

    @abstractmethod
    def _SetShakingSpeed(self, OptionsInstance: SetTemperatureInterfaceCommand.Options):
        ...

    @abstractmethod
    def _SetShakingSpeedTime(
        self, OptionsInstance: SetTemperatureInterfaceCommand.Options
    ) -> float:
        ...

    @abstractmethod
    def _GetShakingSpeed(self) -> int:
        ...

    @abstractmethod
    def _GetShakingSpeedTime(self) -> float:
        ...

    def __post_init__(self):
        self.SetTemperature = TempControlDevice.SetTemperatureInterfaceCommand(
            self._SetTemperature, self._SetTemperatureTime
        )
        self.GetTemperature = TempControlDevice.GetTemperatureInterfaceCommand(
            self._GetTemperature, self._GetTemperatureTime
        )
        self.SetShakingSpeed = TempControlDevice.SetShakingSpeedInterfaceCommand(
            self._SetShakingSpeed, self._SetShakingSpeedTime
        )
        self.GetShakingSpeed = TempControlDevice.GetShakingSpeedInterfaceCommand(
            self._GetShakingSpeed, self._GetShakingSpeedTime
        )
