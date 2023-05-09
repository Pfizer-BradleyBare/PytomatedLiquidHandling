from abc import abstractmethod

from ....Tools import InterfaceABC


class TipInterface(InterfaceABC):
    def __init__(self, CustomErrorHandling: bool):
        InterfaceABC.__init__(self, CustomErrorHandling)
        self.TipPosition: int = 0
        self.RemainingTips: int = 0

    def GetCurrentTipPosition(self) -> int:
        if self.TipPosition == 0:
            raise Exception("The tip position is zero. This should never happen...")

        return self.TipPosition

    def GetRemainingTips(self) -> int:
        return self.RemainingTips

    @abstractmethod
    def Reload(
        self,
    ):
        ...

    @abstractmethod
    def UpdateTipPosition(
        self,
        NumTips: int,
    ):
        ...

    @abstractmethod
    def UpdateRemainingTips(
        self,
    ):
        ...
