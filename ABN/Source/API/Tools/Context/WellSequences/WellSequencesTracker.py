from .....AbstractClasses import TrackerABC
from .WellSequences import WellSequences


class WellSequencesTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[int, WellSequences] = dict()

    def ManualLoad(self, ObjectABCInstance: WellSequences) -> None:

        if self.IsTracked(ObjectABCInstance) is True:
            raise (str(type(ObjectABCInstance).__name__)) + " is already tracked"

        self.Collection[ObjectABCInstance.GetName()] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: WellSequences) -> None:
        if self.IsTracked(ObjectABCInstance) is False:
            raise (str(type(ObjectABCInstance).__name__)) + " is not yet tracked"

        del self.Collection[ObjectABCInstance.GetName()]

    def IsTracked(self, ObjectABCInstance: WellSequences) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[WellSequences]:
        return self.Collection.items()

    def GetObjectsAsDictionary(self) -> dict[int, WellSequences]:
        return self.Collection

    def GetObjectByName(self, Name: int) -> WellSequences:
        return self.Collection[Name]
