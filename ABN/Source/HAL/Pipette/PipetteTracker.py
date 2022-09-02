from ...AbstractClasses import TrackerABC
from .Pipette import PipettingDevice
from ..Tip import TipTracker


class PipetteTracker(TrackerABC):
    def __init__(
        self,
        TipTrackerInstance: TipTracker,
    ):
        self.Collection: dict[str, PipettingDevice] = dict()
        self.TipTrackerInstance: TipTracker = TipTrackerInstance

    def LoadManual(self, InputPipettingDevice: PipettingDevice):
        Name = InputPipettingDevice.GetPipettingChannel().GetName()

        if Name in self.Collection:
            raise Exception("Pipette Device Already Exists")

        self.Collection[Name] = InputPipettingDevice

    def GetLoadedObjectsAsDictionary(self) -> dict[str, PipettingDevice]:
        return self.Collection

    def GetLoadedObjectsAsList(self) -> list[PipettingDevice]:
        return [self.Collection[key] for key in self.Collection]

    def GetObjectByName(self, Name: str) -> PipettingDevice:
        return self.Collection[Name]
