from abc import abstractmethod
from dataclasses import dataclass

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from ...Tools.AbstractClasses import InterfaceABC
from .Interface import LoadUnloadOptions


@dataclass
class DeckLoaderABC(InterfaceABC, UniqueObjectABC):
    @abstractmethod
    def Load(self, OptionsTrackerInstance: LoadUnloadOptions.OptionsTracker):
        ...

    @abstractmethod
    def Unload(self, OptionsTrackerInstance: LoadUnloadOptions.OptionsTracker):
        ...
