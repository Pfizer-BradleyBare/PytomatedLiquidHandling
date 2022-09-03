from .Workbook import Workbook
from ...AbstractClasses import TrackerABC


class WorkbookTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[str, Workbook] = dict()

    def LoadManual(self, MethodInstance: Workbook):
        Name = MethodInstance.GetName()

        if Name in self.Collection:
            raise Exception("Workbook Already Exists")

        self.Collection[Name] = MethodInstance

    def GetObjectsAsList(self) -> list[Workbook]:
        return [self.Collection[key] for key in self.Collection]

    def GetObjectsAsDictionary(self) -> dict[str, Workbook]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> Workbook:
        return self.Collection[Name]
