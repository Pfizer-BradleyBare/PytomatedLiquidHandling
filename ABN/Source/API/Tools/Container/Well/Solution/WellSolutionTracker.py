from ......AbstractClasses import TrackerABC, ObjectABC
from .WellSolution import WellSolution


class WellSolutionTracker(TrackerABC, ObjectABC):
    def __init__(self, WellNumber: int):
        self.WellNumber: int = WellNumber
        self.Collection: dict[str, WellSolution] = dict()

    def GetName(self) -> str:
        return str(self.WellNumber)

    def LoadManual(self, WellSolutionInstance: WellSolution):
        Name = WellSolutionInstance.GetName()

        if str(Name) in self.Collection:
            raise Exception("Solution Already Exists")

        self.Collection[Name] = WellSolutionInstance

    def GetObjectsAsList(self) -> list[WellSolution]:
        return self.Collection.items()

    def GetObjectsAsDictionary(self) -> dict[str, WellSolution]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> WellSolution:
        return self.Collection[Name]
