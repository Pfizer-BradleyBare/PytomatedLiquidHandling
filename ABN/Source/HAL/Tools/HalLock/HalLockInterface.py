from .HalLockTracker import HalLockTracker


class HalLockInterface:
    def __init__(self, HalLockTrackerInstance: HalLockTracker):
        self.HalLockTrackerInstance: HalLockTracker = HalLockTrackerInstance
