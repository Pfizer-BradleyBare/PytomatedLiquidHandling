from .Block import Block
from ....AbstractClasses import TrackerABC


class BlockTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[str, Block] = dict()

    def ManualLoad(self, ObjectABCInstance: Block) -> None:

        if self.IsTracked(ObjectABCInstance) is True:
            raise (str(type(ObjectABCInstance).__name__)) + " is already tracked"

        self.Collection[ObjectABCInstance.GetName()] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: Block) -> None:
        if self.IsTracked(ObjectABCInstance) is False:
            raise (str(type(ObjectABCInstance).__name__)) + " is not yet tracked"

        del self.Collection[ObjectABCInstance.GetName()]

    def IsTracked(self, ObjectABCInstance: Block) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[Block]:
        return self.Collection.items()

    def GetObjectsAsDictionary(self) -> dict[str, Block]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> Block:
        return self.Collection[Name]
