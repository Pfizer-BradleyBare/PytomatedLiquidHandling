from ...HAL.TempControlDevice.BaseTempControlDevice import TempControlDevice
from ..Handler import GetHandler
from ..Tools.ResourceLock.ResourceLockTracker import ResourceLockTracker
from ..Tools.RunTypes import RunTypes


def Release(TempControlDeviceInstance: TempControlDevice, RunType: RunTypes):

    HandlerInstance = GetHandler()
    ResourceLockTrackerInstance = HandlerInstance.ResourceLockTrackerInstance

    if RunType is RunTypes.Run:
        ResourceLockTrackerInstance.ManualUnload(TempControlDeviceInstance)
