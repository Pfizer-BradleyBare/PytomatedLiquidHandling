from .....AbstractClasses import TrackerABC
from .WellFactor import WellFactor


class WellFactorTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[int, WellFactor] = dict()

    def ManualLoad(self, ObjectABCInstance: WellFactor) -> None:

        if self.IsTracked(ObjectABCInstance) is True:
            raise (str(type(ObjectABCInstance).__name__)) + " is already tracked"

        self.Collection[ObjectABCInstance.GetName()] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: WellFactor) -> None:
        if self.IsTracked(ObjectABCInstance) is False:
            raise (str(type(ObjectABCInstance).__name__)) + " is not yet tracked"

        del self.Collection[ObjectABCInstance.GetName()]

    def IsTracked(self, ObjectABCInstance: WellFactor) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[WellFactor]:
        return list(self.Collection.items())

    def GetObjectsAsDictionary(self) -> dict[int, WellFactor]:
        return self.Collection

    def GetObjectByName(self, Name: int) -> WellFactor:
        return self.Collection[Name]
