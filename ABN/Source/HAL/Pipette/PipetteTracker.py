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

    def ManualLoad(self, ObjectABCInstance: PipettingDevice) -> None:

        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is already tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: PipettingDevice) -> None:
        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is not yet tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def IsTracked(self, ObjectABCInstance: PipettingDevice) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[PipettingDevice]:
        return list(self.Collection.items())

    def GetObjectsAsDictionary(self) -> dict[str, PipettingDevice]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> PipettingDevice:
        return self.Collection[Name]
