from abc import abstractmethod

from .....Driver.Tools import CommandTracker
from .....Tools.AbstractClasses import InterfaceABC


class TipInterface(InterfaceABC):
    def __init__(self):
        self.TipPosition: int = 0
        self.RemainingTips: int = 0

    def GetCurrentTipPosition(self) -> int:
        if self.TipPosition == 0:
            raise Exception("The tip position is zero. This should never happen...")

        return self.TipPosition

    def GetRemainingTips(self) -> int:
        return self.RemainingTips

    @abstractmethod
    def Reload(self) -> CommandTracker:
        ...

    @abstractmethod
    def UpdateTipPosition(self, NumTips: int) -> CommandTracker:
        ...

    @abstractmethod
    def UpdateRemainingTips(self) -> CommandTracker:
        ...
