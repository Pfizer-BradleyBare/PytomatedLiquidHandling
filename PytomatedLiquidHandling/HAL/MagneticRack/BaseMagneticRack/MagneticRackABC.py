from ....Tools.AbstractClasses import UniqueObjectABC
from ...LayoutItem import LayoutItemTracker, CoverablePosition, NonCoverablePosition
from ...Pipette import PipetteTracker, TransferOptions
from dataclasses import dataclass, field
from ...TransportDevice import TransportDeviceTracker, TransportOptions
from abc import abstractmethod
from ...Tools.AbstractClasses import InterfaceABC
from ...Backend import NullBackend


@dataclass
class MagneticRackABC(InterfaceABC, UniqueObjectABC):
    BackendInstance: NullBackend
    CustomErrorHandling: bool = field(init=False, default=False)
    SupportedLayoutItemTrackerInstance: LayoutItemTracker
    TransportDeviceTrackerInstance: TransportDeviceTracker
    PipetteTrackerInstance: PipetteTracker

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

    @abstractmethod
    def MoveToDevice(self, SourceLayoutItem: CoverablePosition | NonCoverablePosition):
        ...

    @abstractmethod
    def MoveFromDevice(
        self, DestinationLayoutItem: CoverablePosition | NonCoverablePosition
    ):
        ...

    @abstractmethod
    def RemoveStorageBuffer(self, OptionsTracker: TransferOptions.OptionsTracker):
        ...

    @abstractmethod
    def AddStorageBuffer(self, OptionsTracker: TransferOptions.OptionsTracker):
        ...
