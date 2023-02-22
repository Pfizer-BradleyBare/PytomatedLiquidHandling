from ...HAL.TempControlDevice.BaseTempControlDevice import TempControlDevice
from ..Handler import GetHandler
from ..Tools.Container.BaseContainer import Container
from ..Tools.RunTypes import RunTypes
from ..Transport.Transport import Transport


def Start(
    ContainerInstance: Container,
    TempControlDeviceInstance: TempControlDevice,
    Temperature: float,
    ShakingSpeed: float,
    RunType: RunTypes,
):
    HandlerInstance = GetHandler()
    LoadedLabwareTrackerInstance = HandlerInstance.LoadedLabwareTrackerInstance

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
        RunType,
    )

    LoadedLabwareInstance.LayoutItemGroupingInstance = (
        DestinationLayoutItemGroupingInstance
    )
    # Move first.

    if RunType is RunTypes.Run:
        TempControlDeviceInstance.SetTemperature(Temperature)

        if ShakingSpeed != 0:
            TempControlDeviceInstance.StartShaking(ShakingSpeed)
