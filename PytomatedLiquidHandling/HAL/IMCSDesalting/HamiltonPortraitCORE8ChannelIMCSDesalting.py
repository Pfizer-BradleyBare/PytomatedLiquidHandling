from dataclasses import dataclass

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from .Base import IMCSDesaltingABC, IMCSDesaltingOptions


@dataclass
class HamiltonPortraitCORE8ChannelIMCSDesalting(IMCSDesaltingABC):
    BackendInstance: HamiltonBackendABC

    def Equilibrate(self, Options: IMCSDesaltingOptions.ListedOptions):
        ...

    def Desalt(self, Options: IMCSDesaltingOptions.ListedOptions):
        ...
