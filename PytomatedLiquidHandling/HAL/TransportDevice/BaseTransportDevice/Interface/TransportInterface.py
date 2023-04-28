from abc import abstractmethod

from ....LayoutItem.BaseLayoutItem import LayoutItem
from ....Tools import InterfaceABC


class TransportInterface(InterfaceABC):
    @abstractmethod
    def Transport(
        self,
        SourceLayoutItem: LayoutItem,
        DestinationLayoutItem: LayoutItem,
    ):
        ...
