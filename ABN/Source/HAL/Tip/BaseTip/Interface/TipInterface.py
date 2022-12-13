from abc import abstractmethod

from .....Tools.AbstractClasses import InterfaceABC


class TipInterface(InterfaceABC):
    @abstractmethod
    def Reload(self):
        raise NotImplementedError

    @abstractmethod
    def GetNextAvailableTipPosition(self, NumTips: int):
        raise NotImplementedError

    @abstractmethod
    def GetRemainingTips(self):
        raise NotImplementedError
