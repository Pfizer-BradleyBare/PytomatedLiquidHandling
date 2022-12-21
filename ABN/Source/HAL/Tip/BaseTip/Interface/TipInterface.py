from abc import abstractmethod

from .....Tools.AbstractClasses import InterfaceABC


class TipInterface(InterfaceABC):
    def __init__(self):
        self.TipPosition: int = 0

    def GetCurrentTipPosition(self) -> int:
        if self.TipPosition == 0:
            raise Exception("The tip position is zero. This should never happen...")

        return self.TipPosition

    @abstractmethod
    def Reload(self):
        ...

    @abstractmethod
    def UpdateTipPosition(self, NumTips: int):
        ...

    @abstractmethod
    def GetRemainingTips(self):
        ...
