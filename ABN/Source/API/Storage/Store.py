from ...Server.Globals.HandlerRegistry import HandlerRegistry
from ..Tools.HALLayer.HALLayer import HALLayer
from ..Tools.Labware.BaseLabware import Labware as APILabware
from ..Tools.LoadedLabware.LoadedLabwareTracker import LoadedLabwareTracker


def Store(APILabwareInstance: APILabware):

    LoadedLabwareTrackerInstance: LoadedLabwareTracker = (
        HandlerRegistry.GetObjectByName(
            "API"
        ).LoadedLabwareTrackerInstance  # type:ignore
    )

    HALLayerInstance: HALLayer = HandlerRegistry.GetObjectByName(
        "API"
    ).HALLayerInstance  # type:ignore

    LoadedLabwareAssignments = LoadedLabwareTrackerInstance.GetLabwareAssignments(
        APILabwareInstance
    )

    DeckLocationTrackerInstance = HALLayerInstance.DeckLocationTrackerInstance

    StorageLocations = [
        DeckLocation
        for DeckLocation in DeckLocationTrackerInstance.GetObjectsAsList()
        if DeckLocation.IsStorageLocation()
    ]

    StorageLocations = [
        DeckLocation
        for DeckLocation in DeckLocationTrackerInstance.GetObjectsAsList()
        if DeckLocation.IsStorageLocation()
    ]
