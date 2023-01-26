from ...HAL.TempControlDevice.BaseTempControlDevice import TempControlDevice
from ...Server.Globals.HandlerRegistry import GetAPIHandler
from ..Tools.ResourceLock.ResourceLockTracker import ResourceLockTracker


def Release(TempControlDeviceInstance: TempControlDevice, Simulate: bool):

    ResourceLockTrackerInstance: ResourceLockTracker = (
        GetAPIHandler().ResourceLockTrackerInstance  # type:ignore
    )

    ResourceLockTrackerInstance.ManualUnload(TempControlDeviceInstance)
