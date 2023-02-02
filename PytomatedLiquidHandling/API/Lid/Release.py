from ...Globals import GetCommunicationServer
from ...HAL.Lid.Lid import Lid


def Release(LidInstance: Lid, Simulate: bool):

    CommunicationServerInstance = GetCommunicationServer()
    APIHandlerInstance = CommunicationServerInstance.GetAPIHandler()
    ResourceLockTrackerInstance = APIHandlerInstance.ResourceLockTrackerInstance

    ResourceLockTrackerInstance.ManualUnload(LidInstance)
