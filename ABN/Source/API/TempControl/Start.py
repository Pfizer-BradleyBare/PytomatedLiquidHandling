from ...Globals import GetCommunicationServer
from ...HAL.TempControlDevice.BaseTempControlDevice import TempControlDevice
from ..Tools.Container.BaseContainer import Container
from ..Tools.LoadedLabware.LoadedLabwareTracker import LoadedLabwareTracker
from ..Transport.Transport import Transport


def Start(
    ContainerInstance: Container,
    TempControlDeviceInstance: TempControlDevice,
    Temperature: float,
    ShakingSpeed: float,
    Simulate: bool,
):
    CommunicationServerInstance = GetCommunicationServer()
    APIHandlerInstance = CommunicationServerInstance.GetAPIHandler()
    LoadedLabwareTrackerInstance = APIHandlerInstance.LoadedLabwareTrackerInstance

    LoadedLabwareAssignmentInstances = (
        LoadedLabwareTrackerInstance.GetLabwareAssignments(ContainerInstance)
    )

    LoadedLabwareInstance = LoadedLabwareAssignmentInstances.GetObjectsAsList()[0]
    SourceLayoutItemGroupingInstance = LoadedLabwareInstance.LayoutItemGroupingInstance

    DestinationLayoutItemGroupingInstance = [
        LayoutItem
        for LayoutItem in TempControlDeviceInstance.SupportedLayoutItemGroupingTrackerInstance.GetObjectsAsList()
        if LayoutItem.PlateLayoutItemInstance.LabwareInstance
        == SourceLayoutItemGroupingInstance.PlateLayoutItemInstance.LabwareInstance
    ][0]

    Transport(
        SourceLayoutItemGroupingInstance.PlateLayoutItemInstance,
        DestinationLayoutItemGroupingInstance.PlateLayoutItemInstance,
        Simulate,
    )

    LoadedLabwareInstance.LayoutItemGroupingInstance = (
        DestinationLayoutItemGroupingInstance
    )
    # Move first.

    if Simulate is True:
        return

    TempControlDeviceInstance.SetTemperature(Temperature)

    if ShakingSpeed != 0:
        TempControlDeviceInstance.StartShaking(ShakingSpeed)
