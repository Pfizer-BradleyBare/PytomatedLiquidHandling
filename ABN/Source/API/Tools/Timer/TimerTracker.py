from ....AbstractClasses import TrackerABC
from .Timer import Timer


class TimerTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[str, Timer] = dict()

    def ManualLoad(self, ObjectABCInstance: Timer) -> None:

        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is already tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: Timer) -> None:
        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is not yet tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def IsTracked(self, ObjectABCInstance: Timer) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[Timer]:
        return list(self.Collection.items())

    def GetObjectsAsDictionary(self) -> dict[str, Timer]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> Timer:
        return self.Collection[Name]
