from abc import abstractmethod

from .....Tools.AbstractClasses import InterfaceABC
from ....Layout import LayoutItem


class TransportInterface(InterfaceABC):
    @abstractmethod
    def Transport(
        self, SourceLayoutItem: LayoutItem, DestinationLayoutItem: LayoutItem
    ):
        ...
