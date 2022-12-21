from ...HAL.Layout import LayoutItem
from ...Server.Globals.HandlerRegistry import HandlerRegistry
from ..Tools.Labware.BaseLabware import Labware as APILabware
from ..Tools.LoadedLabware.LoadedLabwareTracker import LoadedLabwareTracker


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

        if not any(
            Device in DestinationTransportDevices for Device in SourceTransportDevices
        ):
            LayoutItemInstancePathway = list()
            # TODO
            ...
            # We need to find a pathway then...
        else:
            LayoutItemInstancePathway = [
                SourceLayoutItemInstance,
                DestinationLayoutItemInstance,
            ]
        # Is source and destination use the same transport devices?

        for i in range(0, len(LayoutItemInstancePathway) - 1):
            # TODO
            ...
        # Do the transports

        # Done
