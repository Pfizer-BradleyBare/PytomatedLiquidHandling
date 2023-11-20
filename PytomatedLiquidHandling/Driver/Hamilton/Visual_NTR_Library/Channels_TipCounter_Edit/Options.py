from dataclasses import dataclass, field
from enum import Enum

from ....Tools.AbstractClasses import OptionsABC


@dataclass
class Options(OptionsABC):
    LabwareID: str


@dataclass
class ListedOptions(list[Options]):
    class SortingOptions(Enum):
        RackColumns = 0
        TierColumns = 1

    TipCounter: str
    DialogTitle: str
    Sorting: SortingOptions = SortingOptions.RackColumns
    Timeout: int = 1000
