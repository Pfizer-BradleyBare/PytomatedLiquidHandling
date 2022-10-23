from ....AbstractClasses import TrackerABC
from .Timer import Timer


class TimerTracker(TrackerABC):
    def __init__(self):
        self.Collection[str, Timer] = dict()

    def LoadManual(self, TimerInstance: Timer):
        Name = TimerInstance.GetName()

        if Name in self.Collection:
            raise Exception("Timer Already Exists")

        self.Collection[Name] = TimerInstance

    def GetObjectsAsList(self) -> list[Timer]:
        return self.Collection.items()

    def GetObjectsAsDictionary(self) -> dict[str, Timer]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> Timer:
        return self.Collection[Name]
