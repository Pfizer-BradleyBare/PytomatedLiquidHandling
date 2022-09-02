from .Block import Block
from ...AbstractClasses import TrackerABC


class BlockTracker(TrackerABC):
    def __init__(self):
        self.Blocks: list[Block] = list()

    def LoadManual(self, BlockInstance: Block):
        self.Blocks.append(BlockInstance)

    def GetObjectsAsList(self) -> list[Block]:
        return self.Blocks

    def GetObjectsAsDictionary(self) -> dict[str, Block]:
        return {
            Block.GetTitle() + " " + str(Block.GetCoordinates()): Block
            for Block in self.Blocks
        }

    def GetObjectByName(self, Name: str) -> Block:
        return self.GetObjectsAsDictionary()[Name]
