from pydantic import dataclasses

from plh.device.HAMILTON.complex_inputs import SortingOptions
from plh.device.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    LabwareID: str


@dataclasses.dataclass(kw_only=True, frozen=True)
class OptionsList(list[Options]):
    TipCounter: str
    DialogTitle: str
    Sorting: SortingOptions = SortingOptions.RackColumns
    Timeout: int = 1000
