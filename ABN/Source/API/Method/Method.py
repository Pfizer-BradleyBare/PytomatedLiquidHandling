from ...AbstractClasses import ObjectABC
from ..Block import Block, BlockTracker


class Method(ObjectABC):
    def __init__(self, MethodPath: str, BlockTrackers: list[BlockTracker]):
        self.MethodPath: str = MethodPath
        self.BlockTrackers: list[BlockTracker] = BlockTrackers
        self.ExecutedBlocks: list[Block] = list()

    def GetName(self) -> str:
        return self.MethodPath

    def GetMethodPath(self) -> str:
        return self.MethodPath
