from .Workbook import Workbook
from ...AbstractClasses import TrackerABC


class WorkbookTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[str, Workbook] = dict()

    def ManualLoad(self, ObjectABCInstance: Workbook) -> None:

        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is already tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: Workbook) -> None:
        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is not yet tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def IsTracked(self, ObjectABCInstance: Workbook) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[Workbook]:
        return list(self.Collection.items())

    def GetObjectsAsDictionary(self) -> dict[str, Workbook]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> Workbook:
        return self.Collection[Name]
