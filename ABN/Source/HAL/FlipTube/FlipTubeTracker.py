from .FlipTube import FlipTube
from ...AbstractClasses import TrackerABC
from ..Labware import LabwareTracker


class FlipTubeTracker(TrackerABC):
    def __init__(self, LabwareTrackerInstance: LabwareTracker):
        self.Collection: dict[str, FlipTube] = dict()
        self.LabwareTrackerInstance: LabwareTracker = LabwareTrackerInstance

    def ManualLoad(self, ObjectABCInstance: FlipTube) -> None:

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__) + " is already tracked"
            )

        self.Collection[ObjectABCInstance.GetName()] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: FlipTube) -> None:
        if self.IsTracked(ObjectABCInstance) is False:
            raise Exception(
                str(type(ObjectABCInstance).__name__) + " is not yet tracked"
            )

        del self.Collection[ObjectABCInstance.GetName()]

    def IsTracked(self, ObjectABCInstance: FlipTube) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[FlipTube]:
        return list(self.Collection.items())

    def GetObjectsAsDictionary(self) -> dict[str, FlipTube]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> FlipTube:
        return self.Collection[Name]
