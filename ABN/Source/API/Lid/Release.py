from ...HAL.Lid.Lid import Lid
from ...Server.Globals.HandlerRegistry import GetAPIHandler
from ..Tools.ResourceLock.ResourceLockTracker import ResourceLockTracker


def Release(LidInstance: Lid, Simulate: bool):

    ResourceLockTrackerInstance: ResourceLockTracker = (
        GetAPIHandler().ResourceLockTrackerInstance  # type:ignore
    )

    ResourceLockTrackerInstance.ManualUnload(LidInstance)
