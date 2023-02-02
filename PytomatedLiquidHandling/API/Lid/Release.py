from ...HAL.Lid.Lid import Lid
from ..Handler import GetHandler


def Release(LidInstance: Lid, Simulate: bool):

    HandlerInstance = GetHandler()
    ResourceLockTrackerInstance = HandlerInstance.ResourceLockTrackerInstance

    ResourceLockTrackerInstance.ManualUnload(LidInstance)
