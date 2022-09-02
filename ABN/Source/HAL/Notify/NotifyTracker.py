from ...AbstractClasses import TrackerABC
from .Notify import Notify


class NotifyTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[str, Notify] = dict()

    def LoadManual(self, NotifyInstance: Notify):
        Name = NotifyInstance.GetName()

        if Name in self.Collection:
            raise Exception("Lid Already Exists")

        self.Collection[Name] = NotifyInstance

    def GetLoadedObjectsAsDictionary(self) -> dict[str, Notify]:
        return self.Collection

    def GetLoadedObjectsAsList(self) -> list[Notify]:
        return [self.Collection[key] for key in self.Collection]

    def GetObjectByName(self, Name: str) -> Notify:
        return self.Collection[Name]
