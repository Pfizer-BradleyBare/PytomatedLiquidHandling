from ...AbstractClasses import TrackerABC
from .Labware import Labware

#
#
# Class Definitions
#
#


class LabwareTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[Labware] = dict()

    def LoadManual(self, LabwareInstance: Labware):
        Name = LabwareInstance.GetName()

        if Name in self.Collection:
            raise Exception("Labware Already Exists")

        self.Collection[Name] = LabwareInstance

    def GetLoadedObjectsAsDictionary(self) -> dict[str, Labware]:
        return self.Collection

    def GetLoadedObjectsAsList(self) -> list[Labware]:
        return [self.Collection[key] for key in self.Collection]

    def GetObjectByName(self, Name: str) -> Labware:
        return self.Collection[Name]


#
#
# End Class Definitions
#
#
