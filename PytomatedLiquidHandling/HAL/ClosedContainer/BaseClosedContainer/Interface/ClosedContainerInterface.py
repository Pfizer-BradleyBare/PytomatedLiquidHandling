from abc import abstractmethod

from ....LayoutItem.BaseLayoutItem import LayoutItem
from ....Tools import InterfaceABC


class ClosedContainerInterface(InterfaceABC):
    @abstractmethod
    def Open(
        self,
        LayoutItemInstances: list[LayoutItem],
        Positions: list[int],
    ):
        ...

    @abstractmethod
    def Close(
        self,
        LayoutItemInstances: list[LayoutItem],
        Positions: list[int],
    ):
        ...
