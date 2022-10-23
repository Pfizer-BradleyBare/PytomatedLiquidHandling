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

    def ManualLoad(self, ObjectABCInstance: TempControlDevice) -> None:

        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is already tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: TempControlDevice) -> None:
        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is not yet tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def IsTracked(self, ObjectABCInstance: TempControlDevice) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[TempControlDevice]:
        return list(self.Collection.items())

    def GetObjectsAsDictionary(self) -> dict[str, TempControlDevice]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> TempControlDevice:
        return self.Collection[Name]
