from PytomatedLiquidHandling.HAL.IMCSDesalting.BaseIMCSDesalting.Interface import (
    IMCSDesaltingOptions,
)
from .BaseIMCSDesalting import IMCSDesaltingABC
from dataclasses import dataclass
from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC


@dataclass
class HamiltonPortraitCORE8ChannelIMCSDesalting(IMCSDesaltingABC):
    BackendInstance: HamiltonBackendABC

    def Initialize(self):
        ...

    def Deinitialize(self):
        ...

    def Equilibrate(self, OptionsTrackerInstance: IMCSDesaltingOptions.OptionsTracker):
        ...

    def Desalt(self, OptionsTrackerInstance: IMCSDesaltingOptions.OptionsTracker):
        ...
