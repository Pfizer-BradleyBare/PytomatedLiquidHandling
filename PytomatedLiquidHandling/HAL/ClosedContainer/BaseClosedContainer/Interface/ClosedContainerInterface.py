from abc import abstractmethod

from ....LayoutItem.BaseLayoutItem import LayoutItem
from ....Tools import InterfaceABC
from .....Driver.Tools.AbstractOptions import AdvancedOptionsABC


class ClosedContainerInterface(InterfaceABC):
    @abstractmethod
    def Open(
        self,
        LayoutItemInstances: list[LayoutItem],
        Positions: list[int],
        AdvancedOptionsInstance: AdvancedOptionsABC = AdvancedOptionsABC(),
    ):
        ...

    @abstractmethod
    def Close(
        self,
        LayoutItemInstances: list[LayoutItem],
        Positions: list[int],
        AdvancedOptionsInstance: AdvancedOptionsABC = AdvancedOptionsABC(),
    ):
        ...
