from abc import abstractmethod

from ....LayoutItem.BaseLayoutItem import LayoutItem
from ....Tools import InterfaceABC
from .....Driver.Tools.AbstractOptions import (
    AdvancedMultiOptionsABC,
    AdvancedMultiOptionsTrackerABC,
)


class ClosedContainerInterface(InterfaceABC):
    @abstractmethod
    def Open(
        self,
        LayoutItemInstances: list[LayoutItem],
        Positions: list[int],
        *,
        AdvancedOptionsInstance: AdvancedMultiOptionsABC | None = None,
        AdvancedOptionsTrackerInstance: AdvancedMultiOptionsTrackerABC | None = None,
    ):
        ...

    @abstractmethod
    def Close(
        self,
        LayoutItemInstances: list[LayoutItem],
        Positions: list[int],
        *,
        AdvancedOptionsInstance: AdvancedMultiOptionsABC | None = None,
        AdvancedOptionsTrackerInstance: AdvancedMultiOptionsTrackerABC | None = None,
    ):
        ...
