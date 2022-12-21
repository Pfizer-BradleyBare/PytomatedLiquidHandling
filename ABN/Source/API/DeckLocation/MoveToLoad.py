from ...Server.Globals.HandlerRegistry import HandlerRegistry
from ..Tools.HALLayer.HALLayer import HALLayer
from ..Tools.Labware.BaseLabware import Labware as APILabware
from ..Tools.LoadedLabware.LoadedLabwareTracker import LoadedLabwareTracker


def MoveToLoad(APILabwareInstance: APILabware):

    LoadedLabwareTrackerInstance: LoadedLabwareTracker = (
        HandlerRegistry.GetObjectByName(
            "API"
        ).LoadedLabwareTrackerInstance  # type:ignore
    )

    HALLayerInstance: HALLayer = HandlerRegistry.GetObjectByName(
        "API"
    ).HALLayerInstance  # type:ignore

    LoadedLabwareAssignmentInstances = (
        LoadedLabwareTrackerInstance.GetLabwareAssignments(APILabwareInstance)
    )
