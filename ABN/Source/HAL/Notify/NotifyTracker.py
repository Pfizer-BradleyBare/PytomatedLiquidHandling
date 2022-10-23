from ...AbstractClasses import TrackerABC
from .Notify import Notify


class NotifyTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[str, Notify] = dict()

    def ManualLoad(self, ObjectABCInstance: Notify) -> None:

        if self.IsTracked(ObjectABCInstance) is True:
            raise (str(type(ObjectABCInstance).__name__)) + " is already tracked"

        self.Collection[ObjectABCInstance.GetName()] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: Notify) -> None:
        if self.IsTracked(ObjectABCInstance) is False:
            raise (str(type(ObjectABCInstance).__name__)) + " is not yet tracked"

        del self.Collection[ObjectABCInstance.GetName()]

    def IsTracked(self, ObjectABCInstance: Notify) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[Notify]:
        return list(self.Collection.items())

    def GetObjectsAsDictionary(self) -> dict[str, Notify]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> Notify:
        return self.Collection[Name]
