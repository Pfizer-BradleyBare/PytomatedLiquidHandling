from ....Tools.AbstractClasses import UniqueObjectTrackerABC
from .TransportDevice import TransportDevice
from .Interface import TransportOptions
from ...LayoutItem import LayoutItemTracker


class TransportDeviceTracker(UniqueObjectTrackerABC[TransportDevice]):
    def __init__(self, TransitionPointsTrackerInstance: LayoutItemTracker):
        UniqueObjectTrackerABC.__init__(self)
        self.TransitionPointsTrackerInstance: LayoutItemTracker = (
            TransitionPointsTrackerInstance
        )

    def Transport(
        self, TransportOptionsTrackerInstance: TransportOptions.OptionsTracker
    ):
        DeviceLastUseIndices: dict[str, int] = dict()

        for Device in self.GetObjectsAsList():
            DeviceLastUseIndices[str(Device.GetUniqueIdentifier())] = 0
            Device._LastTransportFlag = False
        # Setup the devices

        for Index, Options in enumerate(
            TransportOptionsTrackerInstance.GetObjectsAsList()
        ):
            DeviceLastUseIndices[
                str(
                    Options.SourceLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.GetUniqueIdentifier()
                )
            ] = Index
            DeviceLastUseIndices[
                str(
                    Options.DestinationLayoutItem.DeckLocationInstance.TransportDeviceConfigInstance.GetUniqueIdentifier()
                )
            ] = Index
        # Figure out the last time each device is used to I can reset the last transport flag

        for Index, Options in enumerate(
            TransportOptionsTrackerInstance.GetObjectsAsList()
        ):
            ...
