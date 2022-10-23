from ....AbstractClasses import TrackerABC
from .Container import Container


class ContainerTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[str, Container] = dict()

    def ManualLoad(self, ObjectABCInstance: Container) -> None:

        if self.IsTracked(ObjectABCInstance) is True:
            raise (str(type(ObjectABCInstance).__name__)) + " is already tracked"

        self.Collection[ObjectABCInstance.GetName()] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: Container) -> None:
        if self.IsTracked(ObjectABCInstance) is False:
            raise (str(type(ObjectABCInstance).__name__)) + " is not yet tracked"

        del self.Collection[ObjectABCInstance.GetName()]

    def IsTracked(self, ObjectABCInstance: Container) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[Container]:
        return list(self.Collection.items())

    def GetObjectsAsDictionary(self) -> dict[str, Container]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> Container:
        return self.Collection[Name]
