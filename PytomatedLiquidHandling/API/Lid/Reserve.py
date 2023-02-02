from ...Globals import GetCommunicationServer
from ...HAL.Lid.Lid import Lid
from ..Tools.Container.BaseContainer import Container


def Reserve(ContainerInstance: Container, Simulate: bool) -> Lid | None:

    CommunicationServerInstance = GetCommunicationServer()
    APIHandlerInstance = CommunicationServerInstance.GetAPIHandler()
    LoadedLabwareTrackerInstance = APIHandlerInstance.LoadedLabwareTrackerInstance
    ResourceLockTrackerInstance = APIHandlerInstance.ResourceLockTrackerInstance
    HALLayerInstance = APIHandlerInstance.HALLayerInstance

    LoadedLabwareAssignmentInstances = (
        LoadedLabwareTrackerInstance.GetLabwareAssignments(ContainerInstance)
    )

    if len(LoadedLabwareAssignmentInstances.GetObjectsAsList()) > 1:
        raise Exception(
            "There is more than one labware assignment for this Container. This must mean this is not a plate. Please Correct"
        )

    LabwareInstance = LoadedLabwareAssignmentInstances.GetObjectsAsList()[
        0
    ].LayoutItemGroupingInstance.PlateLayoutItemInstance.LabwareInstance
    # Here we are getting the HAL labware of the plate we need to incubate/cool etc.

    LidInstances = [
        Lid
        for Lid in HALLayerInstance.LidTrackerInstance.GetObjectsAsList()
        if not ResourceLockTrackerInstance.IsTracked(Lid.GetName())
        and Lid.SupportedLabwareTrackerInstance.IsTracked(LabwareInstance.GetName())
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
