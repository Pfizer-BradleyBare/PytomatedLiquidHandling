import time
from typing import Callable

from PytomatedLiquidHandling.API.Tools.Timer import Timer as APITimer

from ...Workbook import Block, Workbook


class Timer(APITimer):
    def __init__(
        self,
        WaitTimeSeconds: float,
        WaitReason: str,
        WorkbookInstance: Workbook,
        BlockInstance: Block,
        CallbackFunction: Callable[[Workbook, Block, tuple], None],
        CallbackArgs: tuple,
    ):
        APITimer.__init__(
            self, WaitTimeSeconds, WaitReason, CallbackFunction, CallbackArgs
        )

        self.BlockInstance: Block = BlockInstance
        self.WorkbookInstance: Workbook = WorkbookInstance

    def GetName(self) -> str:
        return self.WorkbookInstance.GetName() + " :: " + self.BlockInstance.GetName()

    def ExecuteCallback(self):
        self.CallbackFunction(
            self.WorkbookInstance, self.BlockInstance, self.CallbackArgs
        )
