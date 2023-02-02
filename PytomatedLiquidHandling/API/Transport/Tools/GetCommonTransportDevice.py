from ....HAL.Layout import LayoutItem
from ....HAL.TransportDevice.BaseTransportDevice import TransportDevice


def GetCommonTransportDevice(
    SourceLayoutItemInstance: LayoutItem, DestinationLayoutItemInstance: LayoutItem
) -> TransportDevice | None:

    SourceTransportDevices = [
        LocationDevice.TransportDeviceInstance
        for LocationDevice in SourceLayoutItemInstance.DeckLocationInstance.SupportedLocationTransportDeviceTrackerInstance.GetObjectsAsList()
    ]

    DestinationTransportDevices = [
        LocationDevice.TransportDeviceInstance
        for LocationDevice in DestinationLayoutItemInstance.DeckLocationInstance.SupportedLocationTransportDeviceTrackerInstance.GetObjectsAsList()
    ]

    for SourceTransportDevice in SourceTransportDevices:
        for DestinationTransportDevice in DestinationTransportDevices:
            if DestinationTransportDevice == SourceTransportDevice:
                return SourceTransportDevice

    return None
