from abc import abstractmethod

from ....LayoutItem.BaseLayoutItem import LayoutItem
from ....Tools.AbstractClasses import InterfaceABC
from .OpenCloseOptions import OpenCloseOptionsTracker


class ClosedContainerInterface(InterfaceABC):
    @abstractmethod
    def Open(self, *, OpenCloseOptionsTrackerInstance: OpenCloseOptionsTracker):
        ...

    @abstractmethod
    def Close(self, *, OpenCloseOptionsTrackerInstance: OpenCloseOptionsTracker):
        ...
