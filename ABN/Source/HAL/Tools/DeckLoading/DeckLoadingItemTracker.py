from ....AbstractClasses import TrackerABC
from .DeckLoadingItem import DeckLoadingItem


class DeckLoadingItemTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[str, DeckLoadingItem] = dict()

    def ManualLoad(self, ObjectABCInstance: DeckLoadingItem) -> None:

        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is already tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: DeckLoadingItem) -> None:
        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is not yet tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def IsTracked(self, ObjectABCInstance: DeckLoadingItem) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[DeckLoadingItem]:
        return list(self.Collection.items())

    def GetObjectsAsDictionary(self) -> dict[str, DeckLoadingItem]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> DeckLoadingItem:
        return self.Collection[Name]
