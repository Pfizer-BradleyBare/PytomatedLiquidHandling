from PytomatedLiquidHandling.HAL.DeckLoader.BaseDeckLoader.Interface import (
    LoadUnloadOptions,
)

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from .BaseDeckLoader import DeckLoaderABC, LoadUnloadOptions


class HamiltonDeckLoader(DeckLoaderABC):
    BackendInstance: HamiltonBackendABC

    def Load(self, OptionsTrackerInstance: LoadUnloadOptions.OptionsTracker):
        ...

    def Unload(self, OptionsTrackerInstance: LoadUnloadOptions.OptionsTracker):
        ...
