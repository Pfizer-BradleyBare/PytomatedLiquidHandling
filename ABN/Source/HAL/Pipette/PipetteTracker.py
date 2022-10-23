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

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__) + " is already tracked"
            )

        self.Collection[ObjectABCInstance.GetName()] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: PipettingDevice) -> None:
        if self.IsTracked(ObjectABCInstance) is False:
            raise Exception(
                str(type(ObjectABCInstance).__name__) + " is not yet tracked"
            )

        del self.Collection[ObjectABCInstance.GetName()]

    def IsTracked(self, ObjectABCInstance: PipettingDevice) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[PipettingDevice]:
        return list(self.Collection.items())

    def GetObjectsAsDictionary(self) -> dict[str, PipettingDevice]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> PipettingDevice:
        return self.Collection[Name]
