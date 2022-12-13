from abc import abstractmethod

from ....Tools.AbstractClasses import InterfaceABC


class TipInterface(InterfaceABC):
    @abstractmethod
    def Load(self):
        raise NotImplementedError

    @abstractmethod
    def GetNextAvailableTipPosition(self):
        raise NotImplementedError

    @abstractmethod
    def GetRemainingTips(self):
        raise NotImplementedError
