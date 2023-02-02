from ...HAL.TempControlDevice.BaseTempControlDevice import TempControlDevice
from ..Handler import GetHandler
from ..Tools.ResourceLock.ResourceLockTracker import ResourceLockTracker


def Release(TempControlDeviceInstance: TempControlDevice, Simulate: bool):

    HandlerInstance = GetHandler()
    ResourceLockTrackerInstance = HandlerInstance.ResourceLockTrackerInstance

    ResourceLockTrackerInstance.ManualUnload(TempControlDeviceInstance)
