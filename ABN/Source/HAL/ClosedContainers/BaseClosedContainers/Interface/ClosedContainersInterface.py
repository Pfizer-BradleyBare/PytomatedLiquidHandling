from abc import abstractmethod
from typing import Callable

from .....Driver.Tools import Command, CommandTracker
from .....Tools.AbstractClasses import InterfaceABC
from ....Layout import LayoutItem


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
