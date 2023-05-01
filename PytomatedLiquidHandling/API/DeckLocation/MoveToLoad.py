from ..Handler import GetHandler
from ..Tools.Container.BaseContainer import Container
from ..Tools.RunTypes import RunTypes
from ..Transport import GetLayoutItem, Transport


def MoveToLoad(ContainerInstance: Container, RunType: RunTypes) -> bool:
    HandlerInstance = GetHandler()
    LoadedLabwareTrackerInstance = HandlerInstance.LoadedLabwareTrackerInstance
    ResourceLockTrackerInstance = HandlerInstance.ResourceLockTrackerInstance
    HALLayerInstance = HandlerInstance.HALLayerInstance

    DeckLocationTrackerInstance = HALLayerInstance.DeckLocationTrackerInstance

    LoadedLabwareAssignmentInstances = (
        LoadedLabwareTrackerInstance.GetLabwareAssignments(ContainerInstance)
    )

    for (
        LoadedLabwareAssignmentInstance
    ) in LoadedLabwareAssignmentInstances.GetObjectsAsList():
        if (
            LoadedLabwareAssignmentInstance.LayoutItemGroupingInstance.GetDeckLocation().IsLoadableLocation()
        ):
            continue
        # Is it already in the appropriate location?

        PossibleDeckLocationInstances = [
            Location
            for Location in DeckLocationTrackerInstance.GetObjectsAsList()
            if (
                not ResourceLockTrackerInstance.IsTracked(
                    Location.GetUniqueIdentifier()
                )
                or not RunType is RunTypes.Run
            )
            and Location.IsLoadableLocation()
        ]
        # Use filtering to get the possible deck locations
        # Note that only if we are actually running do we take into consideration the resource locker.

        if len(PossibleDeckLocationInstances) == 0:
            return False

        for PossibleDeckLocationInstance in PossibleDeckLocationInstances:
            DestinationLayoutGroupingItemInstance = GetLayoutItem(
                PossibleDeckLocationInstance,
                LoadedLabwareAssignmentInstance.LayoutItemGroupingInstance.PlateLayoutItemInstance.LabwareInstance,
            )
            # Try to get the layout item for this deck location

            if DestinationLayoutGroupingItemInstance is None:
                continue
            # If there isn't a valid item then we will try the next location

            Transport(
                LoadedLabwareAssignmentInstance.LayoutItemGroupingInstance.PlateLayoutItemInstance,
                DestinationLayoutGroupingItemInstance.PlateLayoutItemInstance,
                RunType,
            )

            break
            # We moved it! Done with this loop!

    return True
