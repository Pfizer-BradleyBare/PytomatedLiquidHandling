from ...HAL.Lid.Lid import Lid
from ...Server.Globals.HandlerRegistry import HandlerRegistry
from ..Tools.ResourceLock.ResourceLockTracker import ResourceLockTracker


def Release(LidInstance: Lid):

    ResourceLockTrackerInstance: ResourceLockTracker = HandlerRegistry.GetObjectByName(
        "API"
    ).ResourceLockTrackerInstance  # type:ignore

    ResourceLockTrackerInstance.ManualUnload(LidInstance)
