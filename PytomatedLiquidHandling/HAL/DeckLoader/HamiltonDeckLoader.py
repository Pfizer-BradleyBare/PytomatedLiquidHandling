from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from .BaseDeckLoader import DeckLoaderABC, LoadUnloadOptions


class HamiltonDeckLoader(DeckLoaderABC):
    BackendInstance: HamiltonBackendABC

    def Load(self, OptionsTrackerInstance: list[LoadUnloadOptions.Options]):
        ...

    def Unload(self, OptionsTrackerInstance: list[LoadUnloadOptions.Options]):
        ...
