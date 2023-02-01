from ...Globals import GetCommunicationServer
from ...HAL.Lid.Lid import Lid


def Release(LidInstance: Lid, Simulate: bool):

    CommunicationServerInstance = GetCommunicationServer()
    APIHandlerInstance = CommunicationServerInstance.APIHandlerInstance
    ResourceLockTrackerInstance = APIHandlerInstance.ResourceLockTrackerInstance

    ResourceLockTrackerInstance.ManualUnload(LidInstance)
