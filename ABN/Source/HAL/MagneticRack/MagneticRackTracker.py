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

    def ManualLoad(self, ObjectABCInstance: MagneticRack) -> None:

        if self.IsTracked(ObjectABCInstance) is True:
            raise (str(type(ObjectABCInstance).__name__)) + " is already tracked"

        self.Collection[ObjectABCInstance.GetName()] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: MagneticRack) -> None:
        if self.IsTracked(ObjectABCInstance) is False:
            raise (str(type(ObjectABCInstance).__name__)) + " is not yet tracked"

        del self.Collection[ObjectABCInstance.GetName()]

    def IsTracked(self, ObjectABCInstance: MagneticRack) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[MagneticRack]:
        return self.Collection.items()

    def GetObjectsAsDictionary(self) -> dict[str, MagneticRack]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> MagneticRack:
        return self.Collection[Name]


#
#
# End Class Definitions
#
#
