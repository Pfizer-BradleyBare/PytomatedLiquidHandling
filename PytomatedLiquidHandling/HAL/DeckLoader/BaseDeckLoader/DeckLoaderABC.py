from abc import abstractmethod
from dataclasses import dataclass


from ...Tools.AbstractClasses import InterfaceABC
from .Interface import LoadUnloadOptions


@dataclass
class DeckLoaderABC(InterfaceABC):
    @abstractmethod
    def Load(self, Options: list[LoadUnloadOptions.Options]):
        ...

    @abstractmethod
    def Unload(self, Options: list[LoadUnloadOptions.Options]):
        ...
