import time
from ....Tools.AbstractClasses import ObjectABC
from ...Workbook import Block, Workbook

from typing import Callable


class Timer(ObjectABC):
    def __init__(
        self,
        WaitTimeSeconds: float,
        WaitReason: str,
        BlockInstance: Block,
        WorkbookInstance: Workbook,
        CallbackFunction: Callable[[Block, Workbook], None],
    ):
        self.WaitTimeSeconds: float = WaitTimeSeconds
        self.WaitTimeEnd: float = time.time() + WaitTimeSeconds
        self.WaitReason: str = WaitReason
        self.BlockInstance: Block = BlockInstance
        self.WorkbookInstance: Workbook = WorkbookInstance
        self.CallbackFunction: Callable[[Block, Workbook], None] = CallbackFunction

    def GetName(self) -> str:
        return "Timer: " + str(self.BlockInstance.GetName())

    def GetWaitTime(self) -> float:
        return self.WaitTimeSeconds

    def GetRemainingWaitTime(self) -> float:
        return self.WaitTimeEnd - time.time()

    def GetWaitReason(self) -> str:
        return self.WaitReason

    def ExecuteCallbackFunction(self) -> None:
        self.CallbackFunction(self.BlockInstance, self.WorkbookInstance)
