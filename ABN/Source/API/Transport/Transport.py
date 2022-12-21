from ...HAL.Layout import LayoutItem
from ...Server.Globals.HandlerRegistry import HandlerRegistry
from ..Tools.Labware.BaseLabware import Labware as APILabware
from ..Tools.LoadedLabware.LoadedLabwareTracker import LoadedLabwareTracker
from .Tools.GetCommonTransportDevice import GetCommonTransportDevice


def Transport(
    APILabwareInstance: APILabware, DestinationLayoutItemInstance: LayoutItem
):

    LoadedLabwareTrackerInstance: LoadedLabwareTracker = (
        HandlerRegistry.GetObjectByName(
            "API"
        ).LoadedLabwareTrackerInstance  # type:ignore
    )

    LoadedLabwareAssignmentInstances = (
        LoadedLabwareTrackerInstance.GetLabwareAssignments(APILabwareInstance)
    )

    for (
        LoadedLabwareAssignmentInstance
    ) in LoadedLabwareAssignmentInstances.GetObjectsAsList():

        SourceLayoutItemInstance = LoadedLabwareAssignmentInstance.LayoutItemInstance
        SourceDeckLocationInstance = SourceLayoutItemInstance.DeckLocationInstance

        DestinationDeckLocationInstance = (
            DestinationLayoutItemInstance.DeckLocationInstance
        )

        SourceLocationTransportDevices = (
            SourceDeckLocationInstance.SupportedLocationTransportDeviceTrackerInstance
        )
        DestinationLocationTransportDevices = (
            DestinationDeckLocationInstance.SupportedLocationTransportDeviceTrackerInstance
        )

        SourceTransportDevices = [
            Device.TransportDeviceInstance
            for Device in SourceLocationTransportDevices.GetObjectsAsList()
        ]
        DestinationTransportDevices = [
            Device.TransportDeviceInstance
            for Device in DestinationLocationTransportDevices.GetObjectsAsList()
        ]
        # Pull just the transport devices

        LayoutItemInstancePathway = list()
        if not any(
            Device in DestinationTransportDevices for Device in SourceTransportDevices
        ):

            # TODO This is the hard part. I have literally no clue. Recursion here I come?
            ...
            # We need to find a pathway then...
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

            TransportDeviceInstance.Transport(
                SourceLayoutItemInstance, DestinationLayoutItemInstance
            )
        # Do the transports

        # Done
