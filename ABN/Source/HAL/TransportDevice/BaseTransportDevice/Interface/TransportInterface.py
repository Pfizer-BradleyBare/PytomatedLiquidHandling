from abc import abstractmethod
from typing import Callable

from .....Driver.Tools import Command, CommandTracker
from ....Layout import LayoutItem
from ....Tools import InterfaceABC


class TransportInterface(InterfaceABC):
    @abstractmethod
    def Transport(
        self,
        SourceLayoutItem: LayoutItem,
        DestinationLayoutItem: LayoutItem,
    ):
        ...
