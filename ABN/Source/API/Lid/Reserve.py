from ...HAL.Lid.Lid import Lid
from ...Server.Globals.HandlerRegistry import HandlerRegistry
from ..Tools.HALLayer.HALLayer import HALLayer
from ..Tools.Labware.BaseLabware import Labware as APILabware
from ..Tools.LoadedLabware.LoadedLabwareTracker import LoadedLabwareTracker
from ..Tools.ResourceLock.ResourceLockTracker import ResourceLockTracker


def Reserve(APILabwareInstance: APILabware) -> Lid | None:

    LoadedLabwareTrackerInstance: LoadedLabwareTracker = (
        HandlerRegistry.GetObjectByName(
            "API"
        ).LoadedLabwareTrackerInstance  # type:ignore
    )

    HALLayerInstance: HALLayer = HandlerRegistry.GetObjectByName(
        "API"
    ).HALLayerInstance  # type:ignore

    ResourceLockTrackerInstance: ResourceLockTracker = HandlerRegistry.GetObjectByName(
        "API"
    ).ResourceLockTrackerInstance  # type:ignore

    LoadedLabwareAssignmentInstances = (
        LoadedLabwareTrackerInstance.GetLabwareAssignments(APILabwareInstance)
    )

    if len(LoadedLabwareAssignmentInstances.GetObjectsAsList()) > 1:
        raise Exception(
            "There is more than one labware assignment for this APILabware. This must mean this is not a plate. Please Correct"
        )

    HALLabwareInstance = LoadedLabwareAssignmentInstances.GetObjectsAsList()[
        0
    ].LayoutItemGroupingInstance.PlateLayoutItemInstance.LabwareInstance
    # Here we are getting the HAL labware of the plate we need to incubate/cool etc.

    LidInstances = [
        Lid
        for Lid in HALLayerInstance.LidTrackerInstance.GetObjectsAsList()
        if not ResourceLockTrackerInstance.IsTracked(Lid.GetName())
        and Lid.SupportedLabwareTrackerInstance.IsTracked(HALLabwareInstance.GetName())
    ]
    # This is a big one. Not as complex as it looks:
    # 1. The Lid must not be tracked
    # 2. The Labware instance must be supported by that lid

    if len(LidInstances) == 0:
        return None
    # Nothing is available right now :(

    BestFitLid = LidInstances[0]
    # Just take the first available one

    ResourceLockTrackerInstance.ManualLoad(BestFitLid)

    return BestFitLid
