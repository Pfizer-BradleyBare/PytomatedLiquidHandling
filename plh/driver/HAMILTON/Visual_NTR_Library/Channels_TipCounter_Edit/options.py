from pydantic import dataclasses

from plh.driver.HAMILTON.complex_inputs import SortingOptions
from plh.driver.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    LabwareID: str


@dataclasses.dataclass(kw_only=True, frozen=True)
class OptionsList(list[Options]):
    TipCounter: str
    DialogTitle: str
    Sorting: SortingOptions = SortingOptions.RackColumns
    Timeout: int = 1000
