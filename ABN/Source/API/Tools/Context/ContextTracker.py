from ....AbstractClasses import TrackerABC
from .Context import Context


class ContextTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[str, Context] = dict()

    def ManualLoad(self, ObjectABCInstance: Context) -> None:

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__) + " is already tracked"
            )

        self.Collection[ObjectABCInstance.GetName()] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: Context) -> None:
        if self.IsTracked(ObjectABCInstance) is False:
            raise Exception(
                str(type(ObjectABCInstance).__name__) + " is not yet tracked"
            )

        del self.Collection[ObjectABCInstance.GetName()]

    def IsTracked(self, ObjectABCInstance: Context) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[Context]:
        return list(self.Collection.items())

    def GetObjectsAsDictionary(self) -> dict[str, Context]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> Context:
        return self.Collection[Name]
