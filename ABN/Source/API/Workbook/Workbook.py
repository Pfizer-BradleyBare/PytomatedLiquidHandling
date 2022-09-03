from ...AbstractClasses import ObjectABC
from .Block import Block, BlockTracker
from .Worklist import Worklist
from .Solution import SolutionTracker


class Workbook(ObjectABC):
    def __init__(
        self,
        MethodName: str,
        BlockTrackerInstances: list[BlockTracker],
        WorklistInstance: Worklist,
        SolutionTrackerInstance: SolutionTracker,
    ):
        self.MethodName: str = MethodName
        self.BlockTrackerInstances: list[BlockTracker] = BlockTrackerInstances
        self.WorklistInstance: Worklist = WorklistInstance
        self.SolutionTrackerInstance: SolutionTracker = SolutionTrackerInstance
        self.ExecutedBlocks: list[Block] = list()

    def GetName(self) -> str:
        return self.MethodName

    def GetBlockTrackers(self) -> list[BlockTracker]:
        return self.BlockTrackerInstances

    def GetWorklist(self) -> Worklist:
        return self.WorklistInstance

    def GetSolutionTracker(self) -> SolutionTracker:
        return self.SolutionTrackerInstance

    def IsStepAlreadyExecuted(self, BlockInstance: Block) -> bool:
        if BlockInstance in self.ExecutedBlocks:
            return True
        else:
            self.ExecutedBlocks.append(BlockInstance)
            return False
