from ...Globals import GetCommunicationServer
from ...HAL.TempControlDevice.BaseTempControlDevice import TempControlDevice
from ..Tools.ResourceLock.ResourceLockTracker import ResourceLockTracker


def Release(TempControlDeviceInstance: TempControlDevice, Simulate: bool):

    CommunicationServerInstance = GetCommunicationServer()
    APIHandlerInstance = CommunicationServerInstance.GetAPIHandler()
    ResourceLockTrackerInstance = APIHandlerInstance.ResourceLockTrackerInstance

    ResourceLockTrackerInstance.ManualUnload(TempControlDeviceInstance)
