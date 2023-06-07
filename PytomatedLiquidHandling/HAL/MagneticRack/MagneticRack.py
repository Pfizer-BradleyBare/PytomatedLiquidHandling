from dataclasses import dataclass
from .BaseMagneticRack import MagneticRackABC
from ..Pipette import TransferOptions
from ..LayoutItem import NonCoverablePosition, CoverablePosition
from ..TransportDevice import TransportOptions


@dataclass
class MagneticRack(MagneticRackABC):
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

    def Initialize(self):
        return super().Initialize()

    def Deinitialize(self):
        return super().Deinitialize()

    def RemoveStorageBuffer(self, OptionsTracker: TransferOptions.OptionsTracker):
        ...

    def AddStorageBuffer(self, OptionsTracker: TransferOptions.OptionsTracker):
        ...
