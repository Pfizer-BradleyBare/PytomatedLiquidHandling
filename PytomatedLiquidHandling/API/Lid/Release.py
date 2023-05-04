from ...HAL.Lid.Lid import Lid
from ..Handler import GetHandler
from ..Tools.RunTypes import RunTypes


def Release(LidInstance: Lid, RunType: RunTypes):

    HandlerInstance = GetHandler()
    ResourceLockTrackerInstance = HandlerInstance.ResourceLockTrackerInstance

    if RunType is RunTypes.Run:
        ResourceLockTrackerInstance.UnloadSingle(LidInstance)
