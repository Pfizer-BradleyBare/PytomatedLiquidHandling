from abc import abstractmethod
from typing import Callable

from .....Driver.Tools import Command, CommandTracker
from ....Layout import LayoutItem
from ....Tools import InterfaceABC


class ClosedContainersInterface(InterfaceABC):
    @abstractmethod
    def Open(
        self,
        LayoutItemInstances: list[LayoutItem],
        Positions: list[int],
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:
        ...

    @abstractmethod
    def Close(
        self,
        LayoutItemInstances: list[LayoutItem],
        Positions: list[int],
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:
        ...
