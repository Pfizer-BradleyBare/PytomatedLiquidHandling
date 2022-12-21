from ...HAL.TempControlDevice.BaseTempControlDevice import TempControlDevice
from ...Server.Globals.HandlerRegistry import HandlerRegistry
from ..Tools.ResourceLock.ResourceLockTracker import ResourceLockTracker


def Release(TempControlDeviceInstance: TempControlDevice):

    ResourceLockTrackerInstance: ResourceLockTracker = HandlerRegistry.GetObjectByName(
        "API"
    ).ResourceLockTrackerInstance  # type:ignore

    ResourceLockTrackerInstance.ManualUnload(TempControlDeviceInstance)
