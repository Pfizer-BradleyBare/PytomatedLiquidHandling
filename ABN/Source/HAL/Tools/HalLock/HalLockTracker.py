from ....AbstractClasses import TrackerABC, ObjectABC


class HalLockTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[str, ObjectABC] = dict()

    def ManualLoad(self, ObjectABCInstance: ObjectABC) -> None:

        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is already tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: ObjectABC) -> None:
        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is not yet tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def IsTracked(self, ObjectABCInstance: ObjectABC) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[ObjectABC]:
        return [self.Collection[Key] for Key in self.Collection]

    def GetObjectsAsDictionary(self) -> dict[str, ObjectABC]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> ObjectABC:
        return self.Collection[Name]
