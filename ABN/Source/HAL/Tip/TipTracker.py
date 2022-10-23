from ...AbstractClasses import TrackerABC
from .Tip import Tip


class TipTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[str, Tip] = dict()

    def ManualLoad(self, ObjectABCInstance: Tip) -> None:

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__) + " is already tracked"
            )

        self.Collection[ObjectABCInstance.GetName()] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: Tip) -> None:
        if self.IsTracked(ObjectABCInstance) is False:
            raise Exception(
                str(type(ObjectABCInstance).__name__) + " is not yet tracked"
            )

        del self.Collection[ObjectABCInstance.GetName()]

    def IsTracked(self, ObjectABCInstance: Tip) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[Tip]:
        return list(self.Collection.items())

    def GetObjectsAsDictionary(self) -> dict[str, Tip]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> Tip:
        return self.Collection[Name]
