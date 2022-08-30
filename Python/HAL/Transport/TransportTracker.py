from ..BaseConfiguration import BaseTracker
from ..Labware import LabwareTracker
from .Transport import TransportDevice


class TransportTracker(BaseTracker):
    def __init__(self, LabwareTrackerInstance: LabwareTracker):
        self.Collection: dict[str, TransportDevice] = dict()
        self.LabwareTrackerInstance: LabwareTracker = LabwareTrackerInstance

    def LoadManual(self, InputDevice: TransportDevice):
        Name = InputDevice.GetName()

        if Name in self.Collection:
            raise Exception("Transport Device Already Exists")

        self.Collection[Name] = InputDevice

    def GetLoadedObjectsAsDictionary(self) -> dict[str, TransportDevice]:
        return self.Collection

    def GetLoadedObjectsAsList(self) -> list[TransportDevice]:
        return [self.Collection[key] for key in self.Collection]

    def GetObjectByName(self, Name: str) -> TransportDevice:
        return self.Collection[Name]
