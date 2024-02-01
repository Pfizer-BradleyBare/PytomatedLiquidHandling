from abc import abstractmethod
from dataclasses import dataclass

from ...Tools.BaseClasses import Interface
from .Interface import LoadUnloadOptions


@dataclass
class DeckLoaderABC(Interface):
    @abstractmethod
    def Load(self, Options: list[LoadUnloadOptions.Options]):
        ...

    @abstractmethod
    def Unload(self, Options: list[LoadUnloadOptions.Options]):
        ...
