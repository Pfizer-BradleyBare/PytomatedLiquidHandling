import time
from abc import abstractmethod
from typing import Callable

from ....Tools.AbstractClasses import ObjectABC


class Timer(ObjectABC):
    def __init__(
        self,
        WaitTimeSeconds: float,
        WaitReason: str,
        CallbackFunction: Callable,
        CallbackArgs: tuple,
    ):
        self.WaitTimeSeconds: float = WaitTimeSeconds
        self.WaitTimeEnd: float = time.time() + WaitTimeSeconds
        self.WaitReason: str = WaitReason
        self.CallbackFunction: Callable = CallbackFunction
        self.CallbackArgs: tuple = CallbackArgs

    def GetWaitTime(self) -> float:
        return self.WaitTimeSeconds

    def GetRemainingWaitTime(self) -> float:
        return self.WaitTimeEnd - time.time()

    def GetWaitReason(self) -> str:
        return self.WaitReason

    @abstractmethod
    def ExecuteCallback(self):
        ...
