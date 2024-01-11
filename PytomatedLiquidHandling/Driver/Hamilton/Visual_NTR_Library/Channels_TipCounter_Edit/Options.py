from enum import Enum

import dataclasses

from ....Tools.BaseClasses import OptionsABC


@dataclasses.dataclass(kw_only=True)
class Options(OptionsABC):
    LabwareID: str


@dataclasses.dataclass(kw_only=True)
class ListedOptions(list[Options]):
    class SortingOptions(Enum):
        RackColumns = 0
        TierColumns = 1

    TipCounter: str
    DialogTitle: str
    Sorting: SortingOptions = SortingOptions.RackColumns
    Timeout: int = 1000
