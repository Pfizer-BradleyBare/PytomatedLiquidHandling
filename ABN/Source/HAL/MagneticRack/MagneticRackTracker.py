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

        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is already tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: MagneticRack) -> None:
        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is not yet tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def IsTracked(self, ObjectABCInstance: MagneticRack) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[MagneticRack]:
        return list(self.Collection.items())

    def GetObjectsAsDictionary(self) -> dict[str, MagneticRack]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> MagneticRack:
        return self.Collection[Name]


#
#
# End Class Definitions
#
#
