from abc import abstractmethod

from .....Driver.Tools import CommandTracker
from .....Tools.AbstractClasses import InterfaceABC
from ....Layout import LayoutItem


class ClosedContainersInterface(InterfaceABC):
    @abstractmethod
    def Open(self, LayoutItemInstance: LayoutItem, Position: int) -> CommandTracker:
        ...

    @abstractmethod
    def Close(self, LayoutItemInstance: LayoutItem, Position: int) -> CommandTracker:
        ...
