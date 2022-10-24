from .....AbstractClasses import TrackerABC
from .Solution.WellSolutionTracker import WellSolutionTracker


class WellTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[int, WellSolutionTracker] = dict()

    def ManualLoad(self, ObjectABCInstance: WellSolutionTracker) -> None:

        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is already tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: WellSolutionTracker) -> None:
        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is not yet tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def IsTracked(self, ObjectABCInstance: WellSolutionTracker) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[WellSolutionTracker]:
        return [self.Collection[Key] for Key in self.Collection]

    def GetObjectsAsDictionary(self) -> dict[str, WellSolutionTracker]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> WellSolutionTracker:
        return self.Collection[Name]
