from ...HAL.Lid import Lid
from ..Handler import GetHandler
from ..Tools.Container.BaseContainer import Container
from ..Tools.LoadedLabware.LoadedLabwareTracker import LoadedLabwareTracker
from ..Tools.RunTypes import RunTypes
from ..Transport.Transport import Transport


def Uncover(ContainerInstance: Container, LidInstance: Lid, RunType: RunTypes):

    HandlerInstance = GetHandler()
    LoadedLabwareTrackerInstance = HandlerInstance.LoadedLabwareTrackerInstance

    LoadedLabwareAssignmentInstances = (
        LoadedLabwareTrackerInstance.GetLabwareAssignments(ContainerInstance)
    )

    LoadedLabwareInstance = LoadedLabwareAssignmentInstances.GetObjectsAsList()[0]
    SourceLayoutItemInstance = (
        LoadedLabwareInstance.LayoutItemGroupingInstance.LidLayoutItemInstance
    )

    if SourceLayoutItemInstance is None:
        raise Exception("This should never happen...")

    DestinationLayoutItemInstance = LidInstance.LidLayoutItem

    Transport(SourceLayoutItemInstance, DestinationLayoutItemInstance, RunType)
    # Do the transfer
