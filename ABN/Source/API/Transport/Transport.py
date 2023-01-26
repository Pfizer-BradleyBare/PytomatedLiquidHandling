from ...API.Tools.HALLayer.HALLayer import HALLayer
from ...HAL.Layout import LayoutItem
from ...Server.Globals import GetAPIHandler
from .Tools.GetCommonTransportDevice import GetCommonTransportDevice
from .Tools.GetLayoutItem import GetLayoutItem


def Transport(
    SourceLayoutItemInstance: LayoutItem, DestinationLayoutItemInstance: LayoutItem
):

    LayoutItemInstancePathway = list()
    if (
        GetCommonTransportDevice(
            SourceLayoutItemInstance, DestinationLayoutItemInstance
        )
        is None
    ):
        HALLayerInstance: HALLayer = GetAPIHandler().HALLayerInstance  # type:ignore
        DeckLocationTrackerInstance = HALLayerInstance.DeckLocationTrackerInstance

        SourceTransportDevices = (
            SourceLayoutItemInstance.DeckLocationInstance.SupportedLocationTransportDeviceTrackerInstance.GetObjectsAsList()
        )
        DestinationTransportDevices = (
            DestinationLayoutItemInstance.DeckLocationInstance.SupportedLocationTransportDeviceTrackerInstance.GetObjectsAsList()
        )

        SupportedTransportDevicesList = (
            SourceTransportDevices + DestinationTransportDevices
        )

        for DeckLocationInstance in DeckLocationTrackerInstance.GetObjectsAsList():
            DeckLocationTransportDeviceInstances = (
                DeckLocationInstance.SupportedLocationTransportDeviceTrackerInstance.GetObjectsAsList()
            )
            if all(
                DeckLocationTransportDeviceInstance in SupportedTransportDevicesList
                for DeckLocationTransportDeviceInstance in DeckLocationTransportDeviceInstances
            ):

                LayoutItemInstancePathway.append(SourceLayoutItemInstance)
                LayoutItemInstancePathway.append(
                    GetLayoutItem(
                        DeckLocationInstance, SourceLayoutItemInstance.GetLabware()
                    )
                )
                LayoutItemInstancePathway.append(DestinationLayoutItemInstance)

                break
                # Found our intermediate location. Break

        if len(LayoutItemInstancePathway) == 0:
            raise Exception(
                "Could not find handoff position... This should never happen"
            )
        # Ok so we will make it a requirement that there has to be an intermediate transport location. This facilitates handoff between different devices.
        # There cannot be a transport that requires two intermediate positions. That would be unreasonable and slow.

    else:
        LayoutItemInstancePathway.append(SourceLayoutItemInstance)
        LayoutItemInstancePathway.append(DestinationLayoutItemInstance)
    # Does source and destination use the same transport devices?

    for Index in range(0, len(LayoutItemInstancePathway) - 1):
        SourceLayoutItemInstance = LayoutItemInstancePathway[Index]
        DestinationLayoutItemInstance = LayoutItemInstancePathway[Index + 1]

        TransportDeviceInstance = GetCommonTransportDevice(
            SourceLayoutItemInstance, DestinationLayoutItemInstance
        )

        if TransportDeviceInstance is None:
            raise Exception(
                "A common transport device was not found. This should not happen, please fix."
            )

        TransportDeviceInstance.Transport(
            SourceLayoutItemInstance, DestinationLayoutItemInstance
        )
    # Do the transports

    # Done
