from ....AbstractClasses import TrackerABC, ObjectABC


class HalLockTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[str, ObjectABC] = dict()

    def LoadManual(self, HalResourceInstance: ObjectABC):
        Name = HalResourceInstance.GetName()

        if Name in self.Collection:
            raise Exception("Hal Resource Already Exists")

        self.Collection[Name] = HalResourceInstance

    def GetLoadedObjectsAsDictionary(self) -> dict[str, ObjectABC]:
        return self.Collection

    def GetLoadedObjectsAsList(self) -> list[ObjectABC]:
        return self.Collection.items()

    def GetObjectByName(self, Name: str) -> ObjectABC:
        return self.Collection[Name]
