from .Solution import Solution
from ....AbstractClasses import TrackerABC
from ....Tools import Excel


class SolutionTracker(TrackerABC):
    def __init__(self, ExcelInstance: Excel):
        self.ExcelInstance: Excel = ExcelInstance
        self.Collection: dict[str, Solution] = dict()

    def LoadManual(self, SolutionInstance: Solution):
        Name = SolutionInstance.GetName()

        if Name in self.Collection:
            raise Exception("Solution Already Exists")

        self.Collection[Name] = SolutionInstance

    def GetObjectsAsDictionary(self) -> dict[str, Solution]:
        return self.Collection

    def GetObjectsAsList(self) -> list[Solution]:
        return [self.Collection[key] for key in self.Collection]

    def GetObjectByName(self, Name: str) -> Solution:
        return self.Collection[Name]
