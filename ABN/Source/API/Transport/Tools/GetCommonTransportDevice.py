from ....HAL.Layout import LayoutItem
from ....HAL.TransportDevice.BaseTransportDevice import TransportDevice
from ....Server.Globals.HandlerRegistry import HandlerRegistry
from ...Tools.HALLayer.HALLayer import HALLayer


def GetCommonTransportDevice(
    SourceLayoutItemInstance: LayoutItem, DestinationLayoutItemInstance: LayoutItem
) -> TransportDevice:

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

    raise Exception(
        "A common transport device was not found. This should not happen, please fix."
    )
