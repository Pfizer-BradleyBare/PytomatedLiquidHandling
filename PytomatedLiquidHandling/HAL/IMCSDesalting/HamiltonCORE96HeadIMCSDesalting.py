from dataclasses import dataclass

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from .BaseIMCSDesalting import IMCSDesaltingABC, IMCSDesaltingOptions


@dataclass
class HamiltonCORE96HeadIMCSDesalting(IMCSDesaltingABC):
    BackendInstance: HamiltonBackendABC

    def Initialize(self):
        ...

    def Deinitialize(self):
        ...

    def Equilibrate(self, OptionsTrackerInstance: IMCSDesaltingOptions.OptionsTracker):
        ...

    def Desalt(self, OptionsTrackerInstance: IMCSDesaltingOptions.OptionsTracker):
        ...
