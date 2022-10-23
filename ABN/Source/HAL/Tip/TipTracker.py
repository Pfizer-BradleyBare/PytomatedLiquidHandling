from ...AbstractClasses import TrackerABC
from .Tip import Tip


class TipTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[str, Tip] = dict()

    def ManualLoad(self, ObjectABCInstance: Tip) -> None:

        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is already tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: Tip) -> None:
        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is not yet tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def IsTracked(self, ObjectABCInstance: Tip) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[Tip]:
        return list(self.Collection.items())

    def GetObjectsAsDictionary(self) -> dict[str, Tip]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> Tip:
        return self.Collection[Name]
