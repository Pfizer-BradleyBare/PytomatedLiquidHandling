from abc import abstractmethod
from typing import Callable

from .....Driver.Tools import Command, CommandTracker
from .....Tools.AbstractClasses import InterfaceABC
from ....Layout import LayoutItem


class TransportInterface(InterfaceABC):
    @abstractmethod
    def Transport(
        self,
        SourceLayoutItem: LayoutItem,
        DestinationLayoutItem: LayoutItem,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:
        ...
