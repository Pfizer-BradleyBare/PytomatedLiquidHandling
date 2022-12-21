from ...HAL.Lid import Lid
from ...Server.Globals.HandlerRegistry import HandlerRegistry
from ..Tools.Labware.BaseLabware import Labware as APILabware
from ..Tools.LoadedLabware.LoadedLabwareTracker import LoadedLabwareTracker
from ..Transport.Transport import Transport


def Cover(
    APILabwareInstance: APILabware,
    LidInstance: Lid,
):

    LoadedLabwareTrackerInstance: LoadedLabwareTracker = (
        HandlerRegistry.GetObjectByName(
            "API"
        ).LoadedLabwareTrackerInstance  # type:ignore
    )

    LoadedLabwareAssignmentInstances = (
        LoadedLabwareTrackerInstance.GetLabwareAssignments(APILabwareInstance)
    )

    LoadedLabwareInstance = LoadedLabwareAssignmentInstances.GetObjectsAsList()[0]
    DestinationLayoutItemInstance = (
        LoadedLabwareInstance.LayoutItemGroupingInstance.LidLayoutItemInstance
    )
    if DestinationLayoutItemInstance is None:
        raise Exception(
            "There is not a lid at this location. This is incorrect. Please fix."
        )

    SourceLayoutItemInstance = LidInstance.LidLayoutItem

    Transport(SourceLayoutItemInstance, DestinationLayoutItemInstance)
    # Do the transfer
