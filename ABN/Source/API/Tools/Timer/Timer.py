import time
from ....AbstractClasses import ObjectABC
from ...Workbook import Block


class Timer(ObjectABC):
    def __init__(
        self,
        WaitTimeSeconds: float,
        WaitReason: str,
        BlockInstance: Block,
        CallbackFunction: callable,
    ):
        self.WaitTimeSeconds: float = WaitTimeSeconds
        self.WaitTimeEnd: float = time.time() + WaitTimeSeconds
        self.WaitReason: str = WaitReason
        self.BlockInstance: Block = BlockInstance
        self.CallbackFunction: callable = CallbackFunction

    def GetName(self) -> str:
        return "Timer: " + self.BlockInstance.GetName()

    def GetWaitTime(self) -> float:
        return self.WaitTimeSeconds

    def GetRemainingWaitTime(self) -> float:
        return self.WaitTimeEnd - time.time()

    def GetWaitReason(self) -> str:
        return self.WaitReason

    def GetBlock(self) -> Block:
        return self.BlockInstance

    def GetCallbackFunction(self) -> callable:
        return self.CallbackFunction
