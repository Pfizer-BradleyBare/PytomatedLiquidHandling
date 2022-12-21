from ...HAL.Lid import Lid
from ...Server.Globals.HandlerRegistry import HandlerRegistry
from ..Tools.Labware.BaseLabware import Labware as APILabware
from ..Tools.LoadedLabware.LoadedLabwareTracker import LoadedLabwareTracker
from ..Transport.Transport import Transport


def Uncover(
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
    SourceLayoutItemInstance = (
        LoadedLabwareInstance.LayoutItemGroupingInstance.LidLayoutItemInstance
    )

    DestinationLayoutItemInstance = LidInstance.LidLayoutItem

    Transport(SourceLayoutItemInstance, DestinationLayoutItemInstance)  # type:ignore
    # Do the transfer
