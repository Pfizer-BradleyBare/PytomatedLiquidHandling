from ...HAL.TempControlDevice.BaseTempControlDevice import TempControlDevice
from ...Server.Globals.HandlerRegistry import HandlerRegistry
from ..Tools.Labware.BaseLabware import Labware as APILabware
from ..Tools.LoadedLabware.LoadedLabwareTracker import LoadedLabwareTracker
from ..Tools.ResourceLock.ResourceLockTracker import ResourceLockTracker
from ..Transport.Transport import Transport


def Start(
    APILabwareInstance: APILabware,
    TempControlDeviceInstance: TempControlDevice,
    Temperature: float,
    ShakingSpeed: float,
):

    LoadedLabwareTrackerInstance: LoadedLabwareTracker = (
        HandlerRegistry.GetObjectByName(
            "API"
        ).LoadedLabwareTrackerInstance  # type:ignore
    )

    ResourceLockTrackerInstance: ResourceLockTracker = HandlerRegistry.GetObjectByName(
        "API"
    ).ResourceLockTrackerInstance  # type:ignore

    LoadedLabwareAssignmentInstances = (
        LoadedLabwareTrackerInstance.GetLabwareAssignments(APILabwareInstance)
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
    )
    ResourceLockTrackerInstance.ManualUnload(
        SourceLayoutItemGroupingInstance.GetDeckLocation()
    )
    ResourceLockTrackerInstance.ManualLoad(
        DestinationLayoutItemGroupingInstance.GetDeckLocation()
    )
    LoadedLabwareInstance.LayoutItemGroupingInstance = (
        DestinationLayoutItemGroupingInstance
    )
    # Move first.

    TempControlDeviceInstance.SetTemperature(Temperature)

    if ShakingSpeed != 0:
        TempControlDeviceInstance.StartShaking(ShakingSpeed)
