from ....AbstractClasses import TrackerABC
from .WellFactor import WellFactor


class WellFactorTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[int, WellFactor] = dict()

    def LoadManual(self, WellFactorInstance: WellFactor):
        Name = WellFactorInstance.GetName()

        if Name in self.Collection:
            raise Exception("Well Already Exists")

        self.Collection[Name] = WellFactorInstance

    def GetObjectsAsList(self) -> list[WellFactor]:
        return self.Collection.items()

    def GetObjectsAsDictionary(self) -> dict[int, WellFactor]:
        return self.Collection

    def GetObjectByName(self, Name: int) -> WellFactor:
        return self.Collection[Name]
