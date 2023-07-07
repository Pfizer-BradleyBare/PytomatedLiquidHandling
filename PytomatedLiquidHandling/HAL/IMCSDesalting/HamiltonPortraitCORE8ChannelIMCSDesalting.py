from dataclasses import dataclass

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from .BaseIMCSDesalting import IMCSDesaltingABC, IMCSDesaltingOptions


@dataclass
class HamiltonPortraitCORE8ChannelIMCSDesalting(IMCSDesaltingABC):
    BackendInstance: HamiltonBackendABC

    def Equilibrate(self, OptionsTrackerInstance: IMCSDesaltingOptions.OptionsTracker):
        ...

    def Desalt(self, OptionsTrackerInstance: IMCSDesaltingOptions.OptionsTracker):
        ...
