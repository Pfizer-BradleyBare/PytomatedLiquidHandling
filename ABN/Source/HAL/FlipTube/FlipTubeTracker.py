from .FlipTube import FlipTube
from ...AbstractClasses import TrackerABC
from ..Labware import LabwareTracker


class FlipTubeTracker(TrackerABC):
    def __init__(self, LabwareTrackerInstance: LabwareTracker):
        self.Collection: dict[str, FlipTube] = dict()
        self.LabwareTrackerInstance: LabwareTracker = LabwareTrackerInstance

    def LoadManual(self, FlipTubeInstance: FlipTube):
        Name = FlipTubeInstance.GetName()

        if Name in self.Collection:
            raise Exception("FlipTube Already Exists")

        self.Collection[Name] = FlipTubeInstance

    def GetLoadedObjectsAsDictionary(self) -> dict[str, FlipTube]:
        return self.Collection

    def GetLoadedObjectsAsList(self) -> list[FlipTube]:
        return [self.Collection[key] for key in self.Collection]

    def GetObjectByName(self, Name: str) -> FlipTube:
        return self.Collection[Name]
