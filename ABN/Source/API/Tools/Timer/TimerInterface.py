from .TimerTracker import TimerTracker
from .Timer import Timer


class TimerInterface:
    def __init__(self, TimerTrackerInstance: TimerTracker):
        self.TimerTrackerInstance: TimerTracker = TimerTrackerInstance

    def ProcessExpiredTimers(self) -> dict[str, Timer]:
        Tracker = self.TimerTrackerInstance
        TimerCollection = Tracker.GetObjectsAsDictionary()
        ExpiredTimers = dict()

        for TimerKey in TimerCollection:
            TimerInstance = TimerCollection[TimerKey]

            if TimerInstance.GetRemainingWaitTime() <= 0:
                TimerInstance.GetCallbackFunction()(TimerInstance.GetBlock())
                ExpiredTimers[TimerKey] = TimerInstance
                del Tracker.Collection[TimerKey]

        return ExpiredTimers
