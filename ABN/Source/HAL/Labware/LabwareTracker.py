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

    def ManualLoad(self, ObjectABCInstance: Labware) -> None:

        if self.IsTracked(ObjectABCInstance) is True:
            raise (str(type(ObjectABCInstance).__name__)) + " is already tracked"

        self.Collection[ObjectABCInstance.GetName()] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: Labware) -> None:
        if self.IsTracked(ObjectABCInstance) is False:
            raise (str(type(ObjectABCInstance).__name__)) + " is not yet tracked"

        del self.Collection[ObjectABCInstance.GetName()]

    def IsTracked(self, ObjectABCInstance: Labware) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[Labware]:
        return self.Collection.items()

    def GetObjectsAsDictionary(self) -> dict[str, Labware]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> Labware:
        return self.Collection[Name]


#
#
# End Class Definitions
#
#
