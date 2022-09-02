from ...AbstractClasses import ObjectABC
from ..Block import Block, BlockTracker
import os


class Method(ObjectABC):
    def __init__(self, MethodPath: str, BlockTrackers: list[BlockTracker]):
        self.MethodPath: str = MethodPath
        self.MethodName: str = os.path.basename(MethodPath)
        self.BlockTrackers: list[BlockTracker] = BlockTrackers
        self.ExecutedBlocks: list[Block] = list()

    def GetName(self) -> str:
        return self.MethodName

    def GetMethodPath(self) -> str:
        return self.MethodPath
