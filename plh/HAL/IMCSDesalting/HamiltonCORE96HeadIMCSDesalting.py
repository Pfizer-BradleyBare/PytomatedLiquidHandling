from dataclasses import dataclass

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from .Base import IMCSDesaltingABC, IMCSDesaltingOptions


@dataclass
class HamiltonCORE96HeadIMCSDesalting(IMCSDesaltingABC):
    Backend: HamiltonBackendABC

    def Equilibrate(self, Options: IMCSDesaltingOptions.OptionsList):
        ...

    def Desalt(self, Options: IMCSDesaltingOptions.OptionsList):
        ...
