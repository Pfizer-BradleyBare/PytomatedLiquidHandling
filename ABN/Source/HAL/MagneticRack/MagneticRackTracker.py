from ...AbstractClasses import TrackerABC
from ..Labware import LabwareTracker
from ..DeckLocation import DeckLocationTracker
from ..Pipette import PipetteTracker
from ..Tip import TipTracker
from .MagneticRack import MagneticRack


class MagneticRackTracker(TrackerABC):
    def __init__(
        self,
        LabwareTrackerInstance: LabwareTracker,
        DeckLocationTrackerInstance: DeckLocationTracker,
        PipetteDeviceTrackerInstance: PipetteTracker,
        TipTrackerInstance: TipTracker,
    ):
        self.Collection: dict[str, MagneticRack] = dict()
        self.LabwareTrackerInstance: LabwareTracker = LabwareTrackerInstance
        self.DeckLocationTrackerInstance: DeckLocationTracker = (
            DeckLocationTrackerInstance
        )
        self.PipetteDeviceTrackerInstance: PipetteTracker = PipetteDeviceTrackerInstance
        self.TipTrackerInstance: TipTracker = TipTrackerInstance

    def LoadManual(self, InputMagneticRack: MagneticRack):
        Name = InputMagneticRack.GetName()

        if Name in self.Collection:
            raise Exception("Lid Already Exists")

        self.Collection[Name] = InputMagneticRack

    def GetLoadedObjectsAsDictionary(self) -> dict[str, MagneticRack]:
        return self.Collection

    def GetLoadedObjectsAsList(self) -> list[MagneticRack]:
        return [self.Collection[key] for key in self.Collection]

    def GetObjectByName(self, Name: str) -> MagneticRack:
        return self.Collection[Name]


#
#
# End Class Definitions
#
#
