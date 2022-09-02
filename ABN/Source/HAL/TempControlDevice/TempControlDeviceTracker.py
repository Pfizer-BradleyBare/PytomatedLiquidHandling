from ...AbstractClasses import TrackerABC
from ..Labware import LabwareTracker
from ..DeckLocation import DeckLocationTracker
from .TempControlDevice import TempControlDevice


class TempControlDeviceTracker(TrackerABC):
    def __init__(
        self,
        LabwareTrackerInstance: LabwareTracker,
        DeckLocationTrackerInstance: DeckLocationTracker,
    ):
        self.Collection: dict[str, TempControlDevice] = dict()
        self.LabwareTrackerInstance: LabwareTracker = LabwareTrackerInstance
        self.DeckLocationTrackerInstance: DeckLocationTracker = (
            DeckLocationTrackerInstance
        )

    def LoadManual(self, InputDevice: TempControlDevice):
        Name = InputDevice.GetName()

        if Name in self.Collection:
            raise Exception("Temp Control Devvice Already Exists")

        self.Collection[Name] = InputDevice

    def GetLoadedObjectsAsList(self) -> list[TempControlDevice]:
        return [self.Collection[key] for key in self.Collection]

    def GetLoadedObjectsAsDictionary(self) -> dict[str, TempControlDevice]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> TempControlDevice:
        return self.Collection[Name]
