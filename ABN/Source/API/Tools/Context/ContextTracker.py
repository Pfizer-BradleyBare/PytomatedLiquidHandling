from ....AbstractClasses import TrackerABC
from .Context import Context


class ContextTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[str, Context] = dict()

    def LoadManual(self, ContextInstance: Context):
        Name = ContextInstance.GetName()

        if str(Name) in self.Collection:
            raise Exception("Context Already Exists")

        self.Collection[Name] = ContextInstance

    def GetObjectsAsList(self) -> list[Context]:
        return self.Collection.items()

    def GetObjectsAsDictionary(self) -> dict[Context]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> Context:
        return self.Collection[Name]
