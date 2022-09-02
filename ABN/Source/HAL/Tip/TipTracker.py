from ...AbstractClasses import TrackerABC
from .Tip import Tip


class TipTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[str, Tip] = dict()

    def LoadManual(self, InputTip: Tip):
        Name = InputTip.GetName()

        if Name in self.Collection:
            raise Exception("Lid Already Exists")

        self.Collection[Name] = InputTip

    def GetLoadedObjectsAsDictionary(self) -> dict[str, Tip]:
        return self.Collection

    def GetLoadedObjectsAsList(self) -> list[Tip]:
        return [self.Collection[key] for key in self.Collection]

    def GetObjectByName(self, Name: str) -> Tip:
        return self.Collection[Name]
