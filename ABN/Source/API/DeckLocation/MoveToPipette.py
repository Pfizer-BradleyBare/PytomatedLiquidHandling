from ...Server.Globals.HandlerRegistry import GetAPIHandler
from ..Tools.Container.BaseContainer import Container
from ..Tools.HALLayer.HALLayer import HALLayer
from ..Tools.LoadedLabware.LoadedLabwareTracker import LoadedLabwareTracker
from ..Tools.ResourceLock.ResourceLockTracker import ResourceLockTracker
from ..Transport import GetLayoutItem, Transport


def MoveToPipette(ContainerInstance: Container, Simulate: bool) -> bool:

    LoadedLabwareTrackerInstance: LoadedLabwareTracker = (
        GetAPIHandler().LoadedLabwareTrackerInstance  # type:ignore
    )

    ResourceLockTrackerInstance: ResourceLockTracker = (
        GetAPIHandler().ResourceLockTrackerInstance  # type:ignore
    )

    HALLayerInstance: HALLayer = GetAPIHandler().HALLayerInstance  # type:ignore
    # Get our API objects

    DeckLocationTrackerInstance = HALLayerInstance.DeckLocationTrackerInstance

    LoadedLabwareAssignmentInstances = (
        LoadedLabwareTrackerInstance.GetLabwareAssignments(ContainerInstance)
    )

    for (
        LoadedLabwareAssignmentInstance
    ) in LoadedLabwareAssignmentInstances.GetObjectsAsList():

        if (
            LoadedLabwareAssignmentInstance.LayoutItemGroupingInstance.GetDeckLocation().IsPipettableLocation()
        ):
            continue
        # Is it already in the appropriate location?

        PossibleDeckLocationInstances = [
            Location
            for Location in DeckLocationTrackerInstance.GetObjectsAsList()
            if not ResourceLockTrackerInstance.IsTracked(Location.GetName())
            and Location.IsPipettableLocation()
        ]
        # Use filtering to get the possible deck locations

        if len(PossibleDeckLocationInstances) == 0:
            return False

        for PossibleDeckLocationInstance in PossibleDeckLocationInstances:
            DestinationLayoutItemGroupingInstance = GetLayoutItem(
                PossibleDeckLocationInstance,
                LoadedLabwareAssignmentInstance.LayoutItemGroupingInstance.PlateLayoutItemInstance.LabwareInstance,
            )
            # Try to get the layout item for this deck location

            if DestinationLayoutItemGroupingInstance is None:
                continue
            # If there isn't a valid item then we will try the next location

            Transport(
                LoadedLabwareAssignmentInstance.LayoutItemGroupingInstance.PlateLayoutItemInstance,
                DestinationLayoutItemGroupingInstance.PlateLayoutItemInstance,
                Simulate,
            )

            break
            # We moved it! Done with this loop!

    return True
