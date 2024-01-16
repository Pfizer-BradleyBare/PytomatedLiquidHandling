import dataclasses
from enum import Enum

from plh.driver.tools import OptionsBase


class SortingOptions(Enum):
    RackColumns = 0
    TierColumns = 1


@dataclasses.dataclass(kw_only=True)
class Options(OptionsBase):
    LabwareID: str


@dataclasses.dataclass(kw_only=True)
class OptionsList(list[Options]):
    TipCounter: str
    DialogTitle: str
    Sorting: SortingOptions = SortingOptions.RackColumns
    Timeout: int = 1000
