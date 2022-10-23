from .Solution import Solution
from ....AbstractClasses import TrackerABC


class SolutionTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[str, Solution] = dict()

    def ManualLoad(self, ObjectABCInstance: Solution) -> None:

        if self.IsTracked(ObjectABCInstance) is True:
            raise (str(type(ObjectABCInstance).__name__)) + " is already tracked"

        self.Collection[ObjectABCInstance.GetName()] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: Solution) -> None:
        if self.IsTracked(ObjectABCInstance) is False:
            raise (str(type(ObjectABCInstance).__name__)) + " is not yet tracked"

        del self.Collection[ObjectABCInstance.GetName()]

    def IsTracked(self, ObjectABCInstance: Solution) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[Solution]:
        return list(self.Collection.items())

    def GetObjectsAsDictionary(self) -> dict[str, Solution]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> Solution:
        return self.Collection[Name]
