from .Block import Block
from ....AbstractClasses import TrackerABC


class BlockTracker(TrackerABC):
    def __init__(self):
        self.Collection: dict[str, Block] = dict()

    def ManualLoad(self, ObjectABCInstance: Block) -> None:

        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is already tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: Block) -> None:
        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is not yet tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    def IsTracked(self, ObjectABCInstance: Block) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetObjectsAsList(self) -> list[Block]:
        return [self.Collection[Key] for Key in self.Collection]

    def GetObjectsAsDictionary(self) -> dict[str, Block]:
        return self.Collection

    def GetObjectByName(self, Name: str) -> Block:
        return self.Collection[Name]
