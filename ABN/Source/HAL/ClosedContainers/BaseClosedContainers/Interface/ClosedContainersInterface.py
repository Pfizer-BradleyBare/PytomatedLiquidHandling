from abc import abstractmethod

from .....Tools.AbstractClasses import InterfaceABC
from ....Layout import LayoutItem


class ClosedContainersInterface(InterfaceABC):
    @abstractmethod
    def Open(self, LayoutItemInstance: LayoutItem, Position: int):
        raise NotImplementedError

    @abstractmethod
    def Close(self, LayoutItemInstance: LayoutItem, Position: int):
        raise NotImplementedError
