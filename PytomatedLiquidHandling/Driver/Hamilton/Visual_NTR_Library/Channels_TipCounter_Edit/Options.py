from enum import Enum

from pydantic import BaseModel

from ....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    LabwareID: str


class ListedOptions(list[Options], BaseModel):
    class SortingOptions(Enum):
        RackColumns = 0
        TierColumns = 1

    TipCounter: str
    DialogTitle: str
    Sorting: SortingOptions = SortingOptions.RackColumns
    Timeout: int = 1000
