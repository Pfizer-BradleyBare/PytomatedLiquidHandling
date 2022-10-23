from ...AbstractClasses import TrackerABC
from ..Labware import LabwareTracker
from .Transport import TransportDevice


class TransportTracker(TrackerABC):
    def __init__(self, LabwareTrackerInstance: LabwareTracker):
        self.Collection: dict[str, TransportDevice] = dict()
        self.LabwareTrackerInstance: LabwareTracker = LabwareTrackerInstance

    def ManualLoad(self, ObjectABCInstance: TransportDevice) -> None:

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__) + " is already tracked"
            )

        self.Collection[ObjectABCInstance.GetName()] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: TransportDevice) -> None:
        if self.IsTracked(ObjectABCInstance) is False:
            raise Exception(
                str(type(ObjectABCInstance).__name__) + " is not yet tracked"
            )

        del self.Collection[ObjectABCInstance.GetName()]

    def IsTracked(self, ObjectABCInstance: TransportDevice) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[TransportDevice]:
        return list(self.Collection.items())

    def GetObjectsAsDictionary(self) -> dict[str, TransportDevice]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> TransportDevice:
        return self.Collection[Name]
