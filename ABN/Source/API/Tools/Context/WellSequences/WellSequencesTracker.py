from .....AbstractClasses import TrackerABC
from .WellSequences import WellSequences


class WellSequencesTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[int, WellSequences] = dict()

    def ManualLoad(self, ObjectABCInstance: WellSequences) -> None:

        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is already tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: WellSequences) -> None:
        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is not yet tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def IsTracked(self, ObjectABCInstance: WellSequences) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[WellSequences]:
        return [self.Collection[Key] for Key in self.Collection]

    def GetObjectsAsDictionary(self) -> dict[int, WellSequences]:
        return self.Collection

    def GetObjectByName(self, Name: int) -> WellSequences:
        return self.Collection[Name]
