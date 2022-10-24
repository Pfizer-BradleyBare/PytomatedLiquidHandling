from .....AbstractClasses import TrackerABC
from .WellFactor import WellFactor


class WellFactorTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[int, WellFactor] = dict()

    def ManualLoad(self, ObjectABCInstance: WellFactor) -> None:

        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is already tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: WellFactor) -> None:
        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is not yet tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def IsTracked(self, ObjectABCInstance: WellFactor) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[WellFactor]:
        return [self.Collection[Key] for Key in self.Collection]

    def GetObjectsAsDictionary(self) -> dict[int, WellFactor]:
        return self.Collection

    def GetObjectByName(self, Name: int) -> WellFactor:
        return self.Collection[Name]
