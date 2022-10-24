from .Solution import Solution
from ....AbstractClasses import TrackerABC


class SolutionTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[str, Solution] = dict()

    def ManualLoad(self, ObjectABCInstance: Solution) -> None:

        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is already tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: Solution) -> None:
        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is not yet tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def IsTracked(self, ObjectABCInstance: Solution) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[Solution]:
        return [self.Collection[Key] for Key in self.Collection]

    def GetObjectsAsDictionary(self) -> dict[str, Solution]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> Solution:
        return self.Collection[Name]
