from abc import abstractmethod

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
