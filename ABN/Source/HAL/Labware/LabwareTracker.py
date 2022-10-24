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

        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is already tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: Labware) -> None:
        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is not yet tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def IsTracked(self, ObjectABCInstance: Labware) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[Labware]:
        return [self.Collection[Key] for Key in self.Collection]

    def GetObjectsAsDictionary(self) -> dict[str, Labware]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> Labware:
        return self.Collection[Name]


#
#
# End Class Definitions
#
#
