from pydantic import dataclasses

from plh.hamilton_venus.complex_inputs import SortingOptions
from plh.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    LabwareID: str


@dataclasses.dataclass(kw_only=True, frozen=True)
class OptionsList(list[Options]):
    TipCounter: str
    DialogTitle: str
    Sorting: SortingOptions = SortingOptions.RackColumns
    Timeout: int = 1000
