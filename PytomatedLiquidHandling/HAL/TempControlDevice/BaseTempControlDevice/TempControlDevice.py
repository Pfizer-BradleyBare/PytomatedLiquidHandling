from abc import abstractmethod
from ....Tools.AbstractClasses import UniqueObjectABC
from ...LayoutItem import LayoutItemTracker, CoverablePosition, NonCoverablePosition
from ...TransportDevice import TransportDeviceTracker, TransportOptions
from .TempLimits.TempLimits import TempLimits
from ...Tools.AbstractClasses import InterfaceABC
from dataclasses import dataclass, field


@dataclass
class TempControlDevice(InterfaceABC, UniqueObjectABC):
    ComPort: str | int
    ShakingSupported: bool
    TempLimitsInstance: TempLimits
    SupportedLayoutItemTrackerInstance: LayoutItemTracker
    TransportDeviceTrackerInstance: TransportDeviceTracker

    HandleID: int | str = field(init=False)
    Temperature: float = field(init=False, default=0)
    ShakingSpeed: int = field(init=False, default=0)

    def GetCompatibleLayoutItem(
        self, LayoutItemInstance: CoverablePosition | NonCoverablePosition
    ) -> CoverablePosition | None:
        for (
            SupportedLayoutItemInstance
        ) in self.SupportedLayoutItemTrackerInstance.GetObjectsAsList():
            if (
                SupportedLayoutItemInstance.LabwareInstance
                == LayoutItemInstance.LabwareInstance
            ):
                if not isinstance(SupportedLayoutItemInstance, CoverablePosition):
                    raise Exception("This should never happen")
                return SupportedLayoutItemInstance

        return None

    def MoveToDevice(self, SourceLayoutItem: CoverablePosition | NonCoverablePosition):
        OptionsTrackerInstance = TransportOptions.OptionsTracker()

        DestinationLayoutItem = self.GetCompatibleLayoutItem(SourceLayoutItem)
        if DestinationLayoutItem == None:
            raise Exception(
                "This heater is not compatible with your layout item labware"
            )

        OptionsTrackerInstance.LoadSingle(
            TransportOptions.Options(
                SourceLayoutItem=SourceLayoutItem,
                DestinationLayoutItem=DestinationLayoutItem,
            )
        )
        self.TransportDeviceTrackerInstance.Transport(OptionsTrackerInstance)

    def MoveFromDevice(
        self, DestinationLayoutItem: CoverablePosition | NonCoverablePosition
    ):
        OptionsTrackerInstance = TransportOptions.OptionsTracker()

        SourceLayoutItem = self.GetCompatibleLayoutItem(DestinationLayoutItem)
        if SourceLayoutItem == None:
            raise Exception(
                "This heater is not compatible with your layout item labware"
            )

        OptionsTrackerInstance.LoadSingle(
            TransportOptions.Options(
                SourceLayoutItem=SourceLayoutItem,
                DestinationLayoutItem=DestinationLayoutItem,
            )
        )
        self.TransportDeviceTrackerInstance.Transport(OptionsTrackerInstance)

    @abstractmethod
    def SetTemperature(
        self,
        Temperature: float,
    ):
        ...

    @abstractmethod
    def UpdateTemperature(
        self,
    ):
        ...

    @abstractmethod
    def StartShaking(
        self,
        RPM: float,
    ):
        ...

    @abstractmethod
    def StopShaking(
        self,
    ):
        ...

    @abstractmethod
    def UpdateShakingSpeed(
        self,
    ):
        ...
