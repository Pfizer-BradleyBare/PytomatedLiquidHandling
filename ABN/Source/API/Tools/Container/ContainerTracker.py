from ....AbstractClasses import TrackerABC
from .Container import Container


class ContainerTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[str, Container] = dict()

    def LoadManual(self, ContainerInstance: Container):
        Name = ContainerInstance.GetName()

        if str(Name) in self.Collection:
            raise Exception("Container Already Exists")

        self.Collection[Name] = ContainerInstance

    def GetObjectsAsList(self) -> list[Container]:
        return self.Collection.items()

    def GetObjectsAsDictionary(self) -> dict[Container]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> Container:
        return self.Collection[Name]
