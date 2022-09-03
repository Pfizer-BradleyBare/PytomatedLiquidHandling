from .Block import Block
from ....AbstractClasses import TrackerABC
from ....Tools import Excel


class BlockTracker(TrackerABC):
    def __init__(self, ExcelInstance: Excel):
        self.Collection: dict[str, Block] = dict()
        self.ExcelInstance: Excel = ExcelInstance

    def LoadManual(self, BlockInstance: Block):
        Name = BlockInstance.GetName()

        if Name in self.Collection:
            raise Exception("Block Already Exists")

        self.Collection[Name] = BlockInstance

    def GetObjectsAsDictionary(self) -> dict[str, Block]:
        return self.Collection

    def GetObjectsAsList(self) -> list[Block]:
        return [self.Collection[key] for key in self.Collection]

    def GetObjectByName(self, Name: str) -> Block:
        return self.Collection[Name]
