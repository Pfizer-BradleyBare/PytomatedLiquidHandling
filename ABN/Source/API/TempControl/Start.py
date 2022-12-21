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
    SourceLayoutItemInstance = LoadedLabwareInstance.LayoutItemInstance

    DestinationLayoutItemInstance = [
        LayoutItem
        for LayoutItem in TempControlDeviceInstance.SupportedLayoutItemTrackerInstance.GetObjectsAsList()
        if LayoutItem.LabwareInstance == SourceLayoutItemInstance.LabwareInstance
    ][0]

    Transport(SourceLayoutItemInstance, DestinationLayoutItemInstance)
    ResourceLockTrackerInstance.ManualUnload(
        SourceLayoutItemInstance.DeckLocationInstance
    )
    ResourceLockTrackerInstance.ManualLoad(
        DestinationLayoutItemInstance.DeckLocationInstance
    )
    LoadedLabwareInstance.LayoutItemInstance = DestinationLayoutItemInstance
    # Move first.

    TempControlDeviceInstance.SetTemperature(Temperature)

    if ShakingSpeed != 0:
        TempControlDeviceInstance.StartShaking(ShakingSpeed)
